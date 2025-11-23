import requests
import json
import time
from typing import Dict, List, Optional
from pathlib import Path
from collections import defaultdict


class RiotAPIClient:
    
    BASE_URLS = {
        'euw1': 'https://euw1.api.riotgames.com',
        'na1': 'https://na1.api.riotgames.com',
        'kr': 'https://kr.api.riotgames.com',
        'eun1': 'https://eun1.api.riotgames.com',
    }
    
    REGIONAL_URLS = {
        'europe': 'https://europe.api.riotgames.com',
        'americas': 'https://americas.api.riotgames.com',
        'asia': 'https://asia.api.riotgames.com',
    }
    
    def __init__(self, api_key: str = None, region: str = 'euw1', cache_dir: str = 'cache'):
        self.api_key = api_key or self._load_api_key()
        self.region = region
        self.regional_route = self._get_regional_route(region)
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.rate_limit_delay = 0.05
        
    def _load_api_key(self) -> Optional[str]:
        key_file = Path('riot_api_key.txt')
        if key_file.exists():
            return key_file.read_text().strip()
        return None
    
    def _get_regional_route(self, region: str) -> str:
        if region in ['euw1', 'eun1', 'tr1', 'ru']:
            return 'europe'
        elif region in ['na1', 'br1', 'lan', 'las']:
            return 'americas'
        elif region in ['kr', 'jp1']:
            return 'asia'
        return 'americas'
    
    def _make_request(self, url: str, params: Dict = None) -> Optional[Dict]:
        if not self.api_key:
            return None
        
        headers = {
            'X-Riot-Token': self.api_key,
            'User-Agent': 'LoL-Build-System/1.0'
        }
        
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                time.sleep(self.rate_limit_delay)
                response = requests.get(url, headers=headers, params=params, timeout=10)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 120))
                    retry_count += 1
                    
                    if retry_count < max_retries:
                        print(f"⏱️  Rate limited. Waiting {retry_after}s (retry {retry_count}/{max_retries})...")
                        time.sleep(retry_after)
                        continue
                    else:
                        print(f"❌ Rate limit exceeded after {max_retries} retries")
                        return None
                else:
                    print(f"API Error {response.status_code}: {response.text[:100]}")
                    return None
                    
            except requests.exceptions.Timeout:
                retry_count += 1
                if retry_count < max_retries:
                    print(f"⏱️  Request timeout, retrying ({retry_count}/{max_retries})...")
                    time.sleep(2)
                    continue
                else:
                    print(f"❌ Request timeout after {max_retries} retries")
                    return None
            except KeyboardInterrupt:
                print(f"\n⚠️  Request interrupted by user")
                raise
            except Exception as e:
                print(f"Request error: {e}")
                return None
        
        return None
    
    def get_challenger_players(self, queue: str = 'RANKED_SOLO_5x5') -> List[Dict]:
        cache_file = self.cache_dir / f'challenger_{queue}.json'
        
        if cache_file.exists():
            mtime = cache_file.stat().st_mtime
            if time.time() - mtime < 86400:
                with open(cache_file, 'r') as f:
                    return json.load(f)
        
        url = f"{self.BASE_URLS[self.region]}/lol/league/v4/challengerleagues/by-queue/{queue}"
        data = self._make_request(url)
        
        if data and 'entries' in data:
            players = data['entries'][:50]
            with open(cache_file, 'w') as f:
                json.dump(players, f, indent=2)
            return players
        
        return []
    
    def get_master_players(self, queue: str = 'RANKED_SOLO_5x5', limit: int = 200) -> List[Dict]:
        """Get Master tier players - more populated than Challenger"""
        cache_file = self.cache_dir / f'master_{queue}.json'
        
        if cache_file.exists():
            mtime = cache_file.stat().st_mtime
            if time.time() - mtime < 86400:
                with open(cache_file, 'r') as f:
                    cached = json.load(f)
                    return cached[:limit]
        
        url = f"{self.BASE_URLS[self.region]}/lol/league/v4/masterleagues/by-queue/{queue}"
        data = self._make_request(url)
        
        if data and 'entries' in data:
            # Cache ALL Master players, then slice
            players = data['entries']
            with open(cache_file, 'w') as f:
                json.dump(players, f, indent=2)
            return players[:limit]
        
        return []
    
    def get_high_elo_players(self, limit: int = 250) -> List[Dict]:
        """Get a large mix of Challenger and Master players for better champion coverage"""
        print("  📊 Fetching high-elo player list...")
        
        # Get Challenger players first (top ~300)
        challenger = self.get_challenger_players()
        print(f"     ✓ {len(challenger)} Challenger players")
        
        # Get Master players to fill up (can be 1000+)
        needed = max(0, limit - len(challenger))
        if needed > 0:
            master = self.get_master_players(limit=needed)
            print(f"     ✓ {len(master)} Master players")
            print(f"     📈 Total pool: {len(challenger) + len(master)} high-elo players")
            return challenger + master
        
        return challenger[:limit]
    
    def get_summoner_by_puuid(self, puuid: str) -> Optional[Dict]:
        url = f"{self.BASE_URLS[self.region]}/lol/summoner/v4/summoners/by-puuid/{puuid}"
        return self._make_request(url)
    
    def get_match_ids(self, puuid: str, count: int = 20) -> List[str]:
        url = f"{self.REGIONAL_URLS[self.regional_route]}/lol/match/v5/matches/by-puuid/{puuid}/ids"
        params = {
            'start': 0,
            'count': count,
            'queue': 420
        }
        
        data = self._make_request(url, params)
        return data if data else []
    
    def get_match_details(self, match_id: str) -> Optional[Dict]:
        cache_file = self.cache_dir / f'match_{match_id}.json'
        
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                return json.load(f)
        
        url = f"{self.REGIONAL_URLS[self.regional_route]}/lol/match/v5/matches/{match_id}"
        data = self._make_request(url)
        
        if data:
            with open(cache_file, 'w') as f:
                json.dump(data, f, indent=2)
        
        return data
    
    def analyze_champion_builds(self, champion_name: str, role: str = None, match_count: int = 100) -> Dict:
        # Map common role names to Riot API teamPosition values
        role_mapping = {
            'top': 'TOP',
            'jungle': 'JUNGLE',
            'mid': 'MIDDLE',
            'middle': 'MIDDLE',
            'adc': 'BOTTOM',
            'bottom': 'BOTTOM',
            'bot': 'BOTTOM',
            'support': 'UTILITY',
            'utility': 'UTILITY',
            'sup': 'UTILITY'
        }
        
        api_role = None
        if role:
            api_role = role_mapping.get(role.lower(), role.upper())

        print(f"\n🔍 Analyzing {champion_name} from high-elo games...")
        print(f"   Target: {match_count} games | Role: {role} (API: {api_role or 'Any'})")
        
        # Get a LARGE pool of high-elo players for better champion coverage
        players = self.get_high_elo_players(limit=250)
        if not players:
            print("❌ Could not fetch high-elo players")
            return {}
        
        builds_data = {
            'items': defaultdict(int),
            'boots': defaultdict(int),
            'starting_items': defaultdict(int),
            'runes': defaultdict(int),
            'summoners': defaultdict(int),
            'total_games': 0,
            'wins': 0
        }
        
        analyzed = 0
        players_checked = 0
        seen_matches = set()  # Track matches we've already processed
        max_players = min(len(players), 100)  # Check up to 100 players for wide coverage
        
        print(f"\n  🎮 Scanning High-Elo Game Pool (Challenger → Master)...")
        print(f"     Strategy: Searching for {champion_name} in matches of {max_players} top players")
        
        for player in players[:max_players]:
            if analyzed >= match_count:
                break
            
            players_checked += 1
            
            # PUUID is directly in the data
            puuid = player.get('puuid')
            if not puuid:
                continue
            
            # Get FEWER matches per player (10) but check MORE players for distribution
            match_ids = self.get_match_ids(puuid, 10)
            
            for match_id in match_ids:
                if analyzed >= match_count:
                    break
                
                # Skip if we've already analyzed this match (from another player)
                if match_id in seen_matches:
                    continue
                
                match_data = self.get_match_details(match_id)
                if not match_data:
                    continue
                
                seen_matches.add(match_id)
                
                # Search ALL participants for our champion
                for participant in match_data['info']['participants']:
                    if participant['championName'].lower() == champion_name.lower():
                        # Check role if specified
                        if api_role:
                            participant_role = participant.get('teamPosition', '').upper()
                            if api_role != participant_role:
                                continue
                        
                        # Found a match!
                        builds_data['total_games'] += 1
                        if participant['win']:
                            builds_data['wins'] += 1
                        
                        # Separate boots from regular items
                        boots_ids = ['1001', '3006', '3009', '3020', '3047', '3111', '3117', '3158']
                        all_items = [participant[f'item{i}'] for i in range(6) if participant.get(f'item{i}', 0) > 0]
                        
                        boots = [item for item in all_items if str(item) in boots_ids]
                        regular_items = [item for item in all_items if str(item) not in boots_ids]
                        
                        for item in regular_items:
                            builds_data['items'][item] += 1
                        
                        for boot in boots:
                            builds_data['boots'][boot] += 1
                        
                        starting = tuple(sorted(all_items[:2])) if len(all_items) >= 2 else tuple(all_items)
                        if starting:
                            builds_data['starting_items'][starting] += 1
                        
                        # Get full rune page (primary + secondary)
                        perks = participant.get('perks', {})
                        styles = perks.get('styles', [])
                        
                        if len(styles) >= 2:
                            rune_primary = styles[0].get('style')
                            rune_keystone = styles[0].get('selections', [{}])[0].get('perk')
                            rune_secondary = styles[1].get('style')
                            
                            if rune_primary and rune_keystone and rune_secondary:
                                builds_data['runes'][(rune_primary, rune_keystone, rune_secondary)] += 1
                        
                        summ_key = tuple(sorted([participant['summoner1Id'], participant['summoner2Id']]))
                        builds_data['summoners'][summ_key] += 1
                        
                        analyzed += 1
                        
                        if analyzed % 5 == 0:
                            print(f"     ✓ {analyzed}/{match_count} games found")
                        
                        break  # Only count once per match
            
            # Progress update
            if players_checked % 10 == 0 and analyzed < match_count:
                print(f"     🔍 Scanned {len(seen_matches)} matches from High-Elo pool, found {analyzed} games...")
        
        if builds_data['total_games'] == 0:
            print(f"\n❌ No games found for {champion_name} ({role or 'any role'})")
            print(f"   Scanned {len(seen_matches)} matches from {players_checked} Challenger/Master players")
            print(f"   This champion might be very rare or the role incorrect")
            return {}
        
        winrate = (builds_data['wins'] / builds_data['total_games']) * 100
        
        most_common_items = sorted(builds_data['items'].items(), key=lambda x: x[1], reverse=True)[:6]
        most_common_boots = max(builds_data['boots'].items(), key=lambda x: x[1])[0] if builds_data['boots'] else None
        most_common_start = max(builds_data['starting_items'].items(), key=lambda x: x[1])[0] if builds_data['starting_items'] else []
        most_common_runes = max(builds_data['runes'].items(), key=lambda x: x[1])[0] if builds_data['runes'] else (None, None, None)
        most_common_summs = max(builds_data['summoners'].items(), key=lambda x: x[1])[0] if builds_data['summoners'] else []
        
        print(f"\n✅ Analysis complete!")
        print(f"   Games analyzed: {builds_data['total_games']}")
        print(f"   Winrate: {winrate:.1f}%")
        
        # Safely extract runes
        rune_primary = most_common_runes[0] if most_common_runes and len(most_common_runes) > 0 else None
        rune_keystone = most_common_runes[1] if most_common_runes and len(most_common_runes) > 1 else None
        rune_secondary = most_common_runes[2] if most_common_runes and len(most_common_runes) > 2 else None
        
        return {
            'champion': champion_name,
            'role': role or 'Any',
            'total_games': builds_data['total_games'],
            'winrate': winrate,
            'core_items': [item[0] for item in most_common_items],
            'boots': most_common_boots,
            'starting_items': list(most_common_start),
            'runes': {
                'primary': rune_primary,
                'keystone': rune_keystone,
                'secondary': rune_secondary
            },
            'summoners': list(most_common_summs)
        }
