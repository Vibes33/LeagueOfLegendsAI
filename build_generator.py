from typing import Dict, List, Optional
from data_dragon_client import DataDragonClient
import os


class BuildGenerator:
    
    def __init__(self):
        self.ddragon = DataDragonClient()
        self.items_data = self.ddragon.get_items()
        self.runes_data = self.ddragon.get_runes()
        self._process_items()
        
    def _process_items(self):
        self.items = {}
        for item_id, item_data in self.items_data['data'].items():
            if self._is_valid_item(item_data):
                self.items[item_id] = {
                    'name': item_data['name'],
                    'gold': item_data['gold']['total'],
                    'stats': self._extract_stats(item_data),
                    'tags': item_data.get('tags', []),
                    'description': item_data.get('plaintext', ''),
                    'maps': item_data.get('maps', {})
                }
    
    def _is_valid_item(self, item_data: Dict) -> bool:
        maps = item_data.get('maps', {})
        summoners_rift = maps.get('11', False)
        if not summoners_rift:
            return False
        
        gold = item_data.get('gold', {})
        if not gold.get('purchasable', False):
            return False
        
        into = item_data.get('into', [])
        if into:
            return False
            
        return True
    
    def _extract_stats(self, item_data: Dict) -> Dict:
        stats = item_data.get('stats', {})
        return {
            'ap': stats.get('FlatMagicDamageMod', 0),
            'ad': stats.get('FlatPhysicalDamageMod', 0),
            'health': stats.get('FlatHPPoolMod', 0),
            'armor': stats.get('FlatArmorMod', 0),
            'mr': stats.get('FlatSpellBlockMod', 0),
            'as': stats.get('PercentAttackSpeedMod', 0),
            'crit': stats.get('FlatCritChanceMod', 0),
            'ms': stats.get('PercentMovementSpeedMod', 0),
            'armor_pen': stats.get('FlatArmorPenetration', 0),
            'lethality': stats.get('FlatPhysicalDamage', 0),
            'magic_pen': stats.get('FlatMagicPenetration', 0),
            'lifesteal': stats.get('PercentLifeStealMod', 0),
            'omnivamp': stats.get('PercentOmniVampMod', 0)
        }
    
    def generate_build(self, champion_name: str, role: str = 'mid', use_api: bool = False) -> Optional[Dict]:
        champions_data = self.ddragon.get_champions()
        champion = self._find_champion(champions_data, champion_name)
        
        if not champion:
            return None
        
        champion_details = self.ddragon.get_champion_details(champion['id'])
        champion_info = champion_details['data'][champion['id']]
        
        if use_api and os.path.exists('riot_api_key.txt'):
            try:
                from riot_api_client import RiotAPIClient
                
                with open('riot_api_key.txt', 'r') as f:
                    api_key = f.read().strip()
                
                client = RiotAPIClient(api_key=api_key, region='euw1')
                analysis = client.analyze_champion_builds(champion_name, role, match_count=50)
                
                # Check if analysis actually succeeded (has games)
                if analysis and analysis.get('total_games', 0) > 0:
                    print(f"\n✅ Using API data: {analysis['total_games']} games analyzed")
                    return self._format_api_build(analysis, champion['name'], champion_info)
                else:
                    print(f"\n⚠️  API returned no games, using fallback system")
            except KeyboardInterrupt:
                print(f"\n\n⚠️  Analysis interrupted by user")
                raise
            except Exception as e:
                print(f"\n⚠️  API analysis failed: {e}")
                import traceback
                traceback.print_exc()
        
        print(f"\n📊 Using expert system fallback")
        return self._fallback_build(champion_info, role or 'Mid')
    
    def _format_api_build(self, analysis: Dict, champion_name: str, champion_info: Dict) -> Dict:
        """Format API analysis results into build display format"""
        starting_items = []
        for item_id in analysis.get('starting_items', []):
            if str(item_id) in self.items_data['data']:
                starting_items.append({
                    'name': self.items_data['data'][str(item_id)]['name'],
                    'id': str(item_id)
                })
        
        core_items = []
        for item_id in analysis.get('core_items', []):
            if str(item_id) in self.items_data['data']:
                core_items.append({
                    'name': self.items_data['data'][str(item_id)]['name'],
                    'id': str(item_id)
                })
        
        # Add boots separately
        boots = None
        boots_id = analysis.get('boots')
        if boots_id and str(boots_id) in self.items_data['data']:
            boots = {
                'name': self.items_data['data'][str(boots_id)]['name'],
                'id': str(boots_id)
            }
        
        summoner_names = {
            '1': 'Cleanse', '3': 'Exhaust', '4': 'Flash', '6': 'Ghost',
            '7': 'Heal', '11': 'Smite', '12': 'Teleport', '14': 'Ignite',
            '21': 'Barrier', '32': 'Mark/Dash'
        }
        
        summoners = []
        for summ_id in analysis.get('summoners', []):
            summ_name = summoner_names.get(str(summ_id), f'Spell {summ_id}')
            summoners.append(summ_name)
        
        runes = analysis.get('runes', {})
        rune_trees = {
            '8000': 'Precision', '8100': 'Domination', '8200': 'Sorcery',
            '8300': 'Inspiration', '8400': 'Resolve'
        }
        keystones = {
            '8005': 'Press the Attack', '8008': 'Lethal Tempo', '8021': 'Fleet Footwork',
            '8010': 'Conqueror', '8112': 'Electrocute', '8124': 'Predator',
            '8128': 'Dark Harvest', '9923': 'Hail of Blades', '8214': 'Summon Aery',
            '8229': 'Arcane Comet', '8230': 'Phase Rush', '8437': 'Grasp of the Undying',
            '8439': 'Aftershock', '8465': 'Guardian', '8351': 'Glacial Augment',
            '8360': 'Unsealed Spellbook', '8369': 'First Strike'
        }
        
        primary = rune_trees.get(str(runes.get('primary')), 'Unknown')
        secondary = rune_trees.get(str(runes.get('secondary')), 'Unknown')
        keystone = keystones.get(str(runes.get('keystone')), 'Unknown')
        
        is_ap = self._determine_damage_type(champion_info)
        
        return {
            'champion': champion_name,
            'role': analysis.get('role', 'mid').capitalize(),
            'type': 'AP' if is_ap else 'AD',
            'summoner_spells': summoners,
            'runes': {
                'keystone': keystone,
                'primary_path': primary,
                'secondary_path': secondary
            },
            'starting_items': starting_items,
            'core_items': core_items,
            'boots': boots,
            'situational_items': [],
            'source': 'riot_api',
            'stats': {
                'winrate': analysis.get('winrate', 0),
                'matches': analysis.get('total_games', 0)
            }
        }
    
    def _format_preset_build(self, preset: Dict, champion_name: str, champion_info: Dict, role: str) -> Dict:
        starting_items = []
        for item_id in preset.get('starting', []):
            if str(item_id) in self.items_data['data']:
                starting_items.append({
                    'name': self.items_data['data'][str(item_id)]['name'],
                    'id': str(item_id)
                })
        
        core_items = []
        for item_id in preset.get('core', []):
            if str(item_id) in self.items_data['data']:
                core_items.append({
                    'name': self.items_data['data'][str(item_id)]['name'],
                    'id': str(item_id)
                })
        
        situational = []
        for item_id in preset.get('situational', []):
            if str(item_id) in self.items_data['data']:
                situational.append({
                    'name': self.items_data['data'][str(item_id)]['name'],
                    'context': 'Situational option',
                    'id': str(item_id)
                })
        
        summoner_names = {
            '1': 'Cleanse', '3': 'Exhaust', '4': 'Flash', '6': 'Ghost',
            '7': 'Heal', '11': 'Smite', '12': 'Teleport', '14': 'Ignite',
            '21': 'Barrier', '32': 'Mark/Dash'
        }
        
        summoners = []
        for summ_id in preset.get('summoners', []):
            summ_name = summoner_names.get(str(summ_id), f'Spell {summ_id}')
            summoners.append(summ_name)
        
        runes = preset.get('runes', {})
        rune_trees = {
            '8000': 'Precision', '8100': 'Domination', '8200': 'Sorcery',
            '8300': 'Inspiration', '8400': 'Resolve'
        }
        keystones = {
            '8005': 'Press the Attack', '8008': 'Lethal Tempo', '8021': 'Fleet Footwork',
            '8010': 'Conqueror', '8112': 'Electrocute', '8124': 'Predator',
            '8128': 'Dark Harvest', '9923': 'Hail of Blades', '8214': 'Summon Aery',
            '8229': 'Arcane Comet', '8230': 'Phase Rush', '8437': 'Grasp of the Undying',
            '8439': 'Aftershock', '8465': 'Guardian', '8351': 'Glacial Augment',
            '8360': 'Unsealed Spellbook', '8369': 'First Strike'
        }
        
        primary = rune_trees.get(str(runes.get('primary')), 'Unknown')
        secondary = rune_trees.get(str(runes.get('secondary')), 'Unknown')
        keystone = keystones.get(str(runes.get('keystone')), 'Unknown')
        
        is_ap = self._determine_damage_type(champion_info)
        
        return {
            'champion': champion_name,
            'role': role.capitalize(),
            'type': 'AP' if is_ap else 'AD',
            'starting_items': starting_items,
            'core_items': core_items,
            'boots': core_items[0] if core_items and 'Boot' in core_items[0]['name'] else None,
            'situational_items': situational,
            'summoner_spells': summoners,
            'runes': {
                'primary_path': primary,
                'secondary_path': secondary,
                'keystone': keystone
            },
            'stats': {
                'winrate': 0,
                'matches': 0
            },
            'source': 'curated_database'
        }
    
    def _format_build_display(self, build_data: Dict, champion_name: str, champion_info: Dict) -> Dict:
        starting_items = []
        for item_id in build_data.get('starting_items', []):
            item_id_str = str(item_id)
            if item_id_str in self.items_data['data']:
                starting_items.append({
                    'name': self.items_data['data'][item_id_str]['name'],
                    'id': item_id_str
                })
        
        core_items = []
        for item_id in build_data.get('core_items', []):
            item_id_str = str(item_id)
            if item_id_str in self.items_data['data']:
                core_items.append({
                    'name': self.items_data['data'][item_id_str]['name'],
                    'id': item_id_str
                })
        
        boots = None
        boots_id = build_data.get('boots')
        if boots_id and str(boots_id) in self.items_data['data']:
            boots = {
                'name': self.items_data['data'][str(boots_id)]['name'],
                'id': str(boots_id)
            }
        
        situational = []
        for sit_item in build_data.get('situational_items', [])[:5]:
            item_id_str = str(sit_item.get('id'))
            if item_id_str in self.items_data['data']:
                situational.append({
                    'name': self.items_data['data'][item_id_str]['name'],
                    'context': sit_item.get('context', 'Situational'),
                    'id': item_id_str
                })
        
        summoner_names = {
            '1': 'Cleanse',
            '3': 'Exhaust',
            '4': 'Flash',
            '6': 'Ghost',
            '7': 'Heal',
            '11': 'Smite',
            '12': 'Teleport',
            '14': 'Ignite',
            '21': 'Barrier',
            '32': 'Mark/Dash'
        }
        
        summoners = []
        for summ_id in build_data.get('summoner_spells', []):
            summ_name = summoner_names.get(str(summ_id), f'Spell {summ_id}')
            summoners.append(summ_name)
        
        rune_data = build_data.get('runes', {})
        
        rune_trees = {
            '8000': 'Precision',
            '8100': 'Domination',
            '8200': 'Sorcery',
            '8300': 'Inspiration',
            '8400': 'Resolve'
        }
        
        keystones = {
            '8005': 'Press the Attack',
            '8008': 'Lethal Tempo',
            '8021': 'Fleet Footwork',
            '8010': 'Conqueror',
            '8112': 'Electrocute',
            '8124': 'Predator',
            '8128': 'Dark Harvest',
            '9923': 'Hail of Blades',
            '8214': 'Summon Aery',
            '8229': 'Arcane Comet',
            '8230': 'Phase Rush',
            '8437': 'Grasp of the Undying',
            '8439': 'Aftershock',
            '8465': 'Guardian',
            '8351': 'Glacial Augment',
            '8360': 'Unsealed Spellbook',
            '8369': 'First Strike'
        }
        
        primary = rune_trees.get(str(rune_data.get('primary_tree')), 'Unknown')
        secondary = rune_trees.get(str(rune_data.get('secondary_tree')), 'Unknown')
        keystone = keystones.get(str(rune_data.get('keystone')), 'Unknown')
        
        is_ap = self._determine_damage_type(champion_info)
        
        return {
            'champion': champion_name,
            'role': build_data.get('role', 'middle'),
            'type': 'AP' if is_ap else 'AD',
            'starting_items': starting_items,
            'core_items': core_items,
            'boots': boots,
            'situational_items': situational,
            'summoner_spells': summoners,
            'runes': {
                'primary_path': primary,
                'secondary_path': secondary,
                'keystone': keystone
            },
            'stats': build_data.get('stats', {}),
            'source': build_data.get('source', 'community')
        }
    
    def _fallback_build(self, champion_info: Dict, role: str) -> Dict:
        is_ap = self._determine_damage_type(champion_info)
        items = self._select_items(is_ap, role, [])
        runes = self._select_runes(champion_info, is_ap)
        
        return {
            'champion': champion_info.get('name', 'Unknown'),
            'role': role,
            'type': 'AP' if is_ap else 'AD',
            'starting_items': [],
            'core_items': [{'name': item['name'], 'id': ''} for item in items[:6]],
            'boots': None,
            'situational_items': [],
            'summoner_spells': ['Flash', 'Ignite'],
            'runes': runes,
            'stats': {},
            'source': 'expert_system'
        }
    
    def _find_champion(self, champions_data: Dict, champion_name: str):
        for champ_id, champ_data in champions_data['data'].items():
            if champ_data['name'].lower() == champion_name.lower():
                return champ_data
        return None
    
    def _determine_damage_type(self, champion_info: Dict) -> bool:
        tags = champion_info.get('tags', [])
        partype = champion_info.get('partype', '')
        
        if 'Mage' in tags:
            return True
        if partype == 'Mana' and ('Support' in tags or 'Tank' not in tags):
            return True
        if 'Marksman' in tags or 'Fighter' in tags or 'Assassin' in tags:
            return False
        
        return False
    
    def _select_items(self, is_ap: bool, role: str, enemy_comp: List[str]) -> List[Dict]:
        selected = []
        
        boots = self._get_boots(is_ap, role)
        if boots:
            selected.append(boots)
        
        if is_ap:
            core_items = self._get_ap_core_items(enemy_comp)
        else:
            core_items = self._get_ad_core_items(role, enemy_comp)
        
        selected.extend(core_items[:5])
        
        return selected
    
    def _get_boots(self, is_ap: bool, role: str) -> Dict:
        boots_map = {
            'ap': '3020',
            'ad': '3006',
            'tank': '3047',
            'support': '3117'
        }
        
        if role == 'Support':
            boots_id = boots_map['support']
        elif is_ap:
            boots_id = boots_map['ap']
        else:
            boots_id = boots_map['ad']
        
        if boots_id in self.items:
            return {
                'name': self.items[boots_id]['name'],
                'reason': 'Core boots for mobility and stats'
            }
        return None
    
    def _get_ap_core_items(self, enemy_comp: List[str]) -> List[Dict]:
        core = []
        
        ap_items = [
            ('3089', 'High AP and magic penetration'),
            ('3135', 'Magic penetration for tanks'),
            ('3157', 'Defense against AD/Assassins'),
            ('3116', 'Slow and damage over time'),
            ('3165', 'Magic penetration'),
        ]
        
        has_tanks = any('tank' in comp.lower() for comp in enemy_comp)
        has_assassins = any('assassin' in comp.lower() for comp in enemy_comp)
        
        for item_id, reason in ap_items:
            if item_id in self.items:
                if item_id == '3135' and not has_tanks:
                    continue
                if item_id == '3157' and not has_assassins:
                    continue
                    
                core.append({
                    'name': self.items[item_id]['name'],
                    'reason': reason
                })
        
        return core
    
    def _get_ad_core_items(self, role: str, enemy_comp: List[str]) -> List[Dict]:
        core = []
        
        if role == 'ADC':
            ad_items = [
                ('3031', 'Core crit damage'),
                ('3094', 'Attack speed and on-hit'),
                ('3036', 'Armor penetration'),
                ('3072', 'Lifesteal and damage'),
            ]
        else:
            ad_items = [
                ('3074', 'Waveclear and sustain'),
                ('3071', 'Health and damage'),
                ('3153', 'Tank shredding'),
                ('3036', 'Armor penetration'),
            ]
        
        for item_id, reason in ad_items:
            if item_id in self.items:
                core.append({
                    'name': self.items[item_id]['name'],
                    'reason': reason
                })
        
        return core
    
    def _select_runes(self, champion_info: Dict, is_ap: bool) -> Dict:
        tags = champion_info.get('tags', [])
        
        if 'Assassin' in tags:
            primary_path = 'Domination'
            keystone = 'Electrocute'
        elif 'Marksman' in tags:
            primary_path = 'Precision'
            keystone = 'Press the Attack'
        elif 'Mage' in tags:
            primary_path = 'Sorcery'
            keystone = 'Arcane Comet'
        elif 'Tank' in tags:
            primary_path = 'Resolve'
            keystone = 'Grasp of the Undying'
        else:
            primary_path = 'Precision'
            keystone = 'Conqueror'
        
        return {
            'primary_path': primary_path,
            'keystone': keystone,
            'secondary_path': self._get_secondary_path(primary_path)
        }
    
    def _get_secondary_path(self, primary: str) -> str:
        secondary_map = {
            'Precision': 'Domination',
            'Domination': 'Sorcery',
            'Sorcery': 'Inspiration',
            'Resolve': 'Precision',
            'Inspiration': 'Resolve'
        }
        return secondary_map.get(primary, 'Inspiration')
