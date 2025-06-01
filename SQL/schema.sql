-- Base de données pour IA de coaching League of Legends
-- Focalisée sur Yone Mid, patchs 25.07 & 25.08, parties Pro/Challenger

CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    summoner_name TEXT,
    region TEXT,
    tier TEXT
);

CREATE TABLE matches (
    id TEXT PRIMARY KEY,
    patch TEXT,
    duration INT,
    date_played TIMESTAMP
);

CREATE TABLE champions (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE items (
    id INT PRIMARY KEY,
    name TEXT,
    stats JSON,
    description TEXT
);

CREATE TABLE runes (
    id INT PRIMARY KEY,
    name TEXT,
    path TEXT,
    stats JSON
);

CREATE TABLE builds (
    id SERIAL PRIMARY KEY,
    match_id TEXT REFERENCES matches(id),
    player_id INT REFERENCES players(id),
    champion_id INT REFERENCES champions(id),
    lane TEXT,
    opponent_champion_id INT REFERENCES champions(id),
    item_ids INT[],
    rune_ids INT[],
    cs_per_min FLOAT,
    kda_ratio FLOAT,
    win BOOLEAN
);
