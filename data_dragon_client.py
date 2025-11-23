import requests
import json
from typing import Dict, List
from pathlib import Path


class DataDragonClient:
    BASE_URL = "https://ddragon.leagueoflegends.com"
    
    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.version = self._get_latest_version()
        
    def _get_latest_version(self) -> str:
        cache_file = self.cache_dir / "version.json"
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                data = json.load(f)
                return data['version']
        
        url = f"{self.BASE_URL}/api/versions.json"
        response = requests.get(url)
        versions = response.json()
        latest = versions[0]
        
        with open(cache_file, 'w') as f:
            json.dump({'version': latest}, f)
        
        return latest
    
    def get_champions(self) -> Dict:
        cache_file = self.cache_dir / "champions.json"
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        url = f"{self.BASE_URL}/cdn/{self.version}/data/en_US/champion.json"
        response = requests.get(url)
        data = response.json()
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        return data
    
    def get_champion_details(self, champion_key: str) -> Dict:
        cache_file = self.cache_dir / f"champion_{champion_key}.json"
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        url = f"{self.BASE_URL}/cdn/{self.version}/data/en_US/champion/{champion_key}.json"
        response = requests.get(url)
        data = response.json()
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        return data
    
    def get_items(self) -> Dict:
        cache_file = self.cache_dir / "items.json"
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        url = f"{self.BASE_URL}/cdn/{self.version}/data/en_US/item.json"
        response = requests.get(url)
        data = response.json()
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        return data
    
    def get_runes(self) -> List[Dict]:
        cache_file = self.cache_dir / "runes.json"
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        url = f"{self.BASE_URL}/cdn/{self.version}/data/en_US/runesReforged.json"
        response = requests.get(url)
        data = response.json()
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        return data
    
    def clear_cache(self):
        for file in self.cache_dir.glob("*.json"):
            file.unlink()
    
    def refresh_data(self):
        self.clear_cache()
        self.version = self._get_latest_version()
        self.get_champions()
        self.get_items()
        self.get_runes()
