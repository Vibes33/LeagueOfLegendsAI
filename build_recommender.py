"""
Build Recommendation System for League of Legends
Système de recommandation de builds basé sur l'analyse contextuelle
"""

import json
from typing import Dict, List, Tuple


class BuildRecommender:
    """Système de recommandation de builds intelligent"""
    
    def __init__(self):
        self.items_data = self.load_items()
        self.runes_data = self.load_runes()
        self.builds_database = self.load_builds_database()
        
    def load_items(self) -> Dict:
        """Charge les données des items"""
        try:
            with open('items_data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"items": [], "item_categories": {}}
    
    def load_runes(self) -> Dict:
        """Charge les données des runes"""
        try:
            with open('runes_data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"runes": [], "rune_paths": {}}
    
    def load_builds_database(self) -> Dict:
        """Charge la base de données de builds pré-configurés"""
        try:
            with open('builds_database.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"builds": []}
    
    def get_item_by_id(self, item_id: int) -> Dict:
        """Récupère un item par son ID"""
        for item in self.items_data.get('items', []):
            if item['id'] == item_id:
                return item
        return None
    
    def get_item_by_name(self, item_name: str) -> Dict:
        """Récupère un item par son nom"""
        for item in self.items_data.get('items', []):
            if item['name'].lower() == item_name.lower():
                return item
        return None
    
    def get_rune_by_name(self, rune_name: str) -> Dict:
        """Récupère une rune par son nom"""
        for rune in self.runes_data.get('runes', []):
            if rune['name'].lower() == rune_name.lower():
                return rune
        return None
    
    def analyze_enemy_composition(self, enemy_types: List[str]) -> Dict:
        """Analyse la composition ennemie et retourne les menaces"""
        threats = {
            'high_ap': False,
            'high_ad': False,
            'healing': False,
            'tank': False,
            'assassin': False,
            'burst': False,
            'cc_heavy': False
        }
        
        ap_count = enemy_types.count('AP')
        ad_count = enemy_types.count('AD')
        
        if ap_count >= 3:
            threats['high_ap'] = True
        if ad_count >= 3:
            threats['high_ad'] = True
        if 'Tank' in enemy_types:
            threats['tank'] = True
        if 'Assassin' in enemy_types:
            threats['assassin'] = True
        
        return threats
    
    def recommend_items_for_champion(self, champion_name: str, champion_type: str, 
                                    enemy_composition: List[str] = None) -> List[Dict]:
        """Recommande des items basés sur le champion et la composition ennemie"""
        
        # Analyse des menaces
        threats = {'high_ap': False, 'high_ad': False, 'tank': False, 'assassin': False}
        if enemy_composition:
            threats = self.analyze_enemy_composition(enemy_composition)
        
        recommended = []
        items_list = self.items_data.get('items', [])
        
        # 1. Boots appropriés
        if champion_type == 'AP':
            boots = self.get_item_by_id(3020)  # Sorcerer's Shoes
            if boots:
                recommended.append(boots)
        elif champion_type == 'AD':
            boots = self.get_item_by_id(3006)  # Berserker's Greaves
            if boots:
                recommended.append(boots)
        
        # 2. Mythique approprié
        mythic = None
        if champion_type == 'AP':
            if threats['tank']:
                mythic = self.get_item_by_id(6653)  # Liandry's
            else:
                mythic = self.get_item_by_id(6655)  # Luden's
        elif champion_type == 'AD':
            if threats['assassin']:
                mythic = self.get_item_by_id(6673)  # Shieldbow
            elif threats['tank']:
                mythic = self.get_item_by_id(6672)  # Kraken
            else:
                mythic = self.get_item_by_id(6671)  # Galeforce
        
        if mythic:
            recommended.append(mythic)
        
        # 3. Items défensifs si nécessaire
        if threats['assassin'] or threats['high_ad']:
            if champion_type == 'AP':
                defensive = self.get_item_by_id(3157)  # Zhonya's
                if defensive:
                    recommended.append(defensive)
            elif champion_type == 'AD':
                defensive = self.get_item_by_id(3156)  # Maw
                if defensive and threats['high_ap']:
                    recommended.append(defensive)
        
        if threats['high_ap'] and champion_type == 'AP':
            defensive = self.get_item_by_id(3102)  # Banshee's
            if defensive:
                recommended.append(defensive)
        
        # 4. Items offensifs
        if champion_type == 'AP':
            # Void Staff si tanks
            if threats['tank']:
                void_staff = self.get_item_by_id(3135)
                if void_staff:
                    recommended.append(void_staff)
            
            # Rabadon pour damage
            rabadon = self.get_item_by_id(3089)
            if rabadon:
                recommended.append(rabadon)
        
        elif champion_type == 'AD':
            # IE pour crit
            ie = self.get_item_by_id(3031)
            if ie:
                recommended.append(ie)
            
            # Penetration si tanks
            if threats['tank']:
                ldr = self.get_item_by_id(3036)
                if ldr:
                    recommended.append(ldr)
        
        # 5. Items situationnels
        # Anti-heal si nécessaire (à ajouter selon contexte)
        
        # Limite à 6 items
        return recommended[:6]
    
    def recommend_runes_for_champion(self, champion_name: str, 
                                    champion_type: str, role: str = None) -> Dict:
        """Recommande des runes pour un champion"""
        
        runes_list = self.runes_data.get('runes', [])
        
        # Filtre les runes keystones appropriées pour le champion
        suitable_keystones = []
        for rune in runes_list:
            if rune['type'] == 'Keystone':
                if champion_name in rune.get('champions', []):
                    suitable_keystones.append(rune)
                elif champion_type in rune.get('good_for', []):
                    suitable_keystones.append(rune)
        
        # Si aucune rune spécifique, utilise des valeurs par défaut
        if not suitable_keystones:
            if champion_type == 'AP':
                suitable_keystones = [r for r in runes_list if r['name'] in ['Electrocute', 'Arcane Comet']]
            elif champion_type == 'AD':
                suitable_keystones = [r for r in runes_list if r['name'] in ['Conqueror', 'Press the Attack']]
        
        primary_rune = suitable_keystones[0] if suitable_keystones else None
        
        return {
            'keystone': primary_rune,
            'primary_path': primary_rune['path'] if primary_rune else 'Precision',
            'secondary_path': self._get_secondary_path(primary_rune['path'] if primary_rune else 'Precision')
        }
    
    def _get_secondary_path(self, primary_path: str) -> str:
        """Détermine le chemin secondaire optimal"""
        secondary_mapping = {
            'Precision': 'Domination',
            'Domination': 'Precision',
            'Sorcery': 'Inspiration',
            'Resolve': 'Precision',
            'Inspiration': 'Sorcery'
        }
        return secondary_mapping.get(primary_path, 'Precision')
    
    def get_build_for_champion(self, champion_name: str, champion_type: str,
                              role: str = None, enemy_composition: List[str] = None) -> Dict:
        """Génère un build complet pour un champion"""
        
        # Vérifier d'abord si un build pré-configuré existe
        for build in self.builds_database.get('builds', []):
            if build['champion'].lower() == champion_name.lower():
                if not role or build.get('role', '').lower() == role.lower():
                    return build
        
        # Sinon, générer un build automatiquement
        items = self.recommend_items_for_champion(champion_name, champion_type, enemy_composition)
        runes = self.recommend_runes_for_champion(champion_name, champion_type, role)
        
        return {
            'champion': champion_name,
            'type': champion_type,
            'role': role or 'Flexible',
            'runes': runes,
            'items': items,
            'build_path': [item['name'] for item in items],
            'generated': True
        }
    
    def get_all_items_by_category(self, category: str) -> List[Dict]:
        """Retourne tous les items d'une catégorie"""
        return [item for item in self.items_data.get('items', []) 
                if item.get('category') == category]
    
    def get_all_items_by_type(self, item_type: str) -> List[Dict]:
        """Retourne tous les items d'un type (AP, AD, Tank)"""
        return [item for item in self.items_data.get('items', []) 
                if item.get('type') == item_type]
    
    def search_items(self, query: str) -> List[Dict]:
        """Recherche des items par nom"""
        query_lower = query.lower()
        return [item for item in self.items_data.get('items', [])
                if query_lower in item['name'].lower()]
    
    def get_counter_items(self, enemy_threats: List[str]) -> List[Dict]:
        """Retourne les items qui contrent des menaces spécifiques"""
        counter_items = []
        for item in self.items_data.get('items', []):
            item_tags = item.get('tags', [])
            good_against = item.get('good_against', [])
            
            for threat in enemy_threats:
                if threat in good_against or threat in item_tags:
                    if item not in counter_items:
                        counter_items.append(item)
        
        return counter_items
