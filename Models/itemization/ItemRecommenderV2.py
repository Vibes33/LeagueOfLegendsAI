import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pickle

class ItemRecommenderV2:
    def __init__(self):
        self.model = None
        self.trained = False

    def prepare_data(self, data):
        df = pd.DataFrame(data)

        # Préparation des entrées
        df['enemy_tags'] = df['enemy_tags'].apply(lambda tags: ','.join(tags))
        df['ally_tags'] = df['ally_tags'].apply(lambda tags: ','.join(tags))
        X = df[['champion', 'role', 'enemy_tags', 'ally_tags']]

        # Sorties : rune + 6 objets en slot
        y = df[['rune', 'item1', 'item2', 'item3', 'item4', 'item5', 'item6']]

        return train_test_split(X, y, test_size=0.2, random_state=42)

    def build_pipeline(self):
        categorical_features = ['champion', 'role', 'enemy_tags', 'ally_tags']
        transformer = ColumnTransformer([
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])

        base_model = RandomForestClassifier(n_estimators=200, random_state=42)
        multi_model = MultiOutputClassifier(base_model)

        pipeline = Pipeline([
            ('preprocess', transformer),
            ('multi_classifier', multi_model)
        ])

        return pipeline

    def train(self, data):
        X_train, X_test, y_train, y_test = self.prepare_data(data)
        self.model = self.build_pipeline()
        self.model.fit(X_train, y_train)
        accuracy = self.model.score(X_test, y_test)
        self.trained = True
        print(f"✅ Modèle entraîné avec précision moyenne (rune + items) : {accuracy:.2f}")

    def predict(self, input_data):
        if not self.trained:
            raise Exception("❌ Le modèle n'est pas encore entraîné.")

        input_df = pd.DataFrame([input_data])
        input_df['enemy_tags'] = ','.join(input_data['enemy_tags'])
        input_df['ally_tags'] = ','.join(input_data['ally_tags'])

        prediction = self.model.predict(input_df)
        return prediction[0]  # [rune, item1, item2, ..., item6]

    def save_model(self, path='item_model_v2.pkl'):
        with open(path, 'wb') as f:
            pickle.dump(self.model, f)
        print("📦 Modèle sauvegardé.")

    def load_model(self, path='item_model_v2.pkl'):
        with open(path, 'rb') as f:
            self.model = pickle.load(f)
        self.trained = True
        print("📥 Modèle chargé.")
