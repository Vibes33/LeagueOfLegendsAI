#!/usr/bin/env python3

import os
from typing import Dict, List
from colorama import init, Fore, Style
from build_generator import BuildGenerator
from gameplay_analyzer import GameplayAnalyzer, GameMetrics

init(autoreset=True)


class LoLManager:
    def __init__(self):
        print(f"{Fore.CYAN}Loading data from Riot API...")
        self.build_gen = BuildGenerator()
        self.gameplay_analyzer = GameplayAnalyzer()
        self.champions = self.build_gen.ddragon.get_champions()
        print(f"{Fore.GREEN}✓ Loaded {len(self.champions['data'])} champions")
        print(f"{Fore.GREEN}✓ Loaded {len(self.build_gen.items)} items")
        print(f"{Fore.GREEN}✓ Patch {self.build_gen.ddragon.version}")
        
    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def print_header(self, title: str):
        self.clear_screen()
        width = 80
        print("\n" + "=" * width)
        print(f"{Fore.CYAN}{Style.BRIGHT}{title.center(width)}")
        print("=" * width + "\n")
    
    def print_separator(self):
        print(f"{Fore.BLUE}" + "-" * 80)
    
    def display_main_menu(self):
        self.print_header("⚔️  LEAGUE OF LEGENDS EXPERT BUILD SYSTEM")
        
        print(f"{Fore.YELLOW}{Style.BRIGHT}MAIN MENU:\n")
        print(f"{Fore.GREEN}[1]{Fore.WHITE} 📋 Champions List")
        print(f"{Fore.GREEN}[2]{Fore.WHITE} 🔍 Search Champion")
        print(f"{Fore.GREEN}[3]{Fore.WHITE} 🎒 Items Database")
        print(f"{Fore.GREEN}[4]{Fore.WHITE} 🛡️  Generate Build")
        print(f"{Fore.GREEN}[5]{Fore.WHITE} 🤖 Gameplay Analysis")
        print(f"{Fore.RED}[0]{Fore.WHITE} 🚪 Exit\n")
        self.print_separator()
    
    def display_champions_list(self):
        self.print_header("📋 CHAMPIONS LIST")
        
        champs = sorted(self.champions['data'].values(), key=lambda x: x['name'])
        total_pages = (len(champs) + 9) // 10
        page = 1
        
        while True:
            self.print_header(f"📋 CHAMPIONS LIST - Page {page}/{total_pages}")
            
            start = (page - 1) * 10
            end = start + 10
            page_champs = champs[start:end]
            
            for i, champ in enumerate(page_champs, start + 1):
                tags = ', '.join(champ.get('tags', []))
                print(f"{Fore.YELLOW}[{i}] {Fore.WHITE}{champ['name']:<20} {Fore.LIGHTBLACK_EX}{tags}")
            
            print()
            self.print_separator()
            print(f"\n{Fore.GREEN}[N]{Fore.WHITE} Next  {Fore.GREEN}[P]{Fore.WHITE} Previous  {Fore.RED}[R]{Fore.WHITE} Return\n")
            
            choice = input(f"{Fore.CYAN}Your choice: {Fore.WHITE}").strip().upper()
            
            if choice == 'R':
                return
            elif choice == 'N' and page < total_pages:
                page += 1
            elif choice == 'P' and page > 1:
                page -= 1
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(champs):
                    self.display_champion_details(champs[idx])
    
    def display_champion_details(self, champ: Dict):
        self.print_header(f"👤 {champ['name'].upper()}")
        
        print(f"{Fore.YELLOW}Title: {Fore.WHITE}{champ.get('title', 'N/A')}")
        print(f"{Fore.YELLOW}Tags: {Fore.WHITE}{', '.join(champ.get('tags', []))}")
        print(f"{Fore.YELLOW}Role: {Fore.WHITE}{champ.get('partype', 'N/A')}")
        
        stats = champ.get('stats', {})
        if stats:
            print(f"\n{Fore.CYAN}{Style.BRIGHT}BASE STATS:")
            print(f"  HP: {Fore.WHITE}{stats.get('hp', 0):.0f}")
            print(f"  Attack: {Fore.WHITE}{stats.get('attackdamage', 0):.0f}")
            print(f"  Armor: {Fore.WHITE}{stats.get('armor', 0):.0f}")
            print(f"  Magic Resist: {Fore.WHITE}{stats.get('spellblock', 0):.0f}")
            print(f"  Move Speed: {Fore.WHITE}{stats.get('movespeed', 0):.0f}")
        
        print(f"\n{Fore.CYAN}Loading abilities details...")
        detailed_champ = self.build_gen.ddragon.get_champion_details(champ['id'])
        champ_data = detailed_champ['data'][champ['id']]
        
        passive = champ_data.get('passive', {})
        if passive:
            print(f"\n{Fore.MAGENTA}{Style.BRIGHT}🔮 PASSIVE: {passive.get('name', 'N/A')}")
            desc = self._clean_html(passive.get('description', ''))
            print(f"{Fore.WHITE}  {desc[:150]}..." if len(desc) > 150 else f"{Fore.WHITE}  {desc}")
        
        spells = champ_data.get('spells', [])
        if spells:
            print(f"\n{Fore.CYAN}{Style.BRIGHT}⚔️  ABILITIES:\n")
            keys = ['Q', 'W', 'E', 'R']
            for i, spell in enumerate(spells[:4]):
                key = keys[i]
                name = spell.get('name', 'N/A')
                
                costs = spell.get('costBurn', 'N/A')
                cooldowns = spell.get('cooldownBurn', 'N/A')
                damage = spell.get('effectBurn', ['N/A'] * 11)
                
                print(f"{Fore.YELLOW}[{key}] {Fore.WHITE}{Style.BRIGHT}{name}")
                print(f"{Fore.LIGHTBLACK_EX}    Cooldown: {Fore.WHITE}{cooldowns}s  {Fore.LIGHTBLACK_EX}Cost: {Fore.WHITE}{costs} mana")
                
                desc = self._clean_html(spell.get('description', ''))
                if len(desc) > 120:
                    desc = desc[:120] + "..."
                print(f"{Fore.WHITE}    {desc}")
                print()
        
        self.print_separator()
        input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def _clean_html(self, text: str) -> str:
        import re
        text = re.sub(r'<br>', ' ', text)
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def search_champion(self):
        self.print_header("🔍 SEARCH CHAMPION")
        
        query = input(f"{Fore.CYAN}Champion name: {Fore.WHITE}").strip().lower()
        
        if not query:
            return
        
        results = [c for c in self.champions['data'].values() if query in c['name'].lower()]
        
        if not results:
            print(f"\n{Fore.RED}No champions found with '{query}'")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            return
        
        self.print_header(f"🔍 SEARCH RESULTS - {query}")
        
        for i, champ in enumerate(results, 1):
            tags = ', '.join(champ.get('tags', []))
            print(f"{Fore.YELLOW}[{i}] {Fore.WHITE}{champ['name']:<20} {Fore.LIGHTBLACK_EX}{tags}")
        
        print()
        self.print_separator()
        print(f"\n{Fore.GREEN}[1-{len(results)}]{Fore.WHITE} View details  {Fore.RED}[R]{Fore.WHITE} Return\n")
        
        choice = input(f"{Fore.CYAN}Your choice: {Fore.WHITE}").strip().upper()
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(results):
                self.display_champion_details(results[idx])
    
    def display_items_database(self):
        items_list = []
        for item_id, item_data in self.build_gen.items_data['data'].items():
            gold = item_data.get('gold', {})
            if gold.get('purchasable', False):
                items_list.append({
                    'id': item_id,
                    'name': item_data['name'],
                    'gold': gold.get('total', 0),
                    'tags': item_data.get('tags', []),
                    'description': item_data.get('plaintext', ''),
                    'stats': item_data.get('stats', {}),
                    'maps': item_data.get('maps', {})
                })
        
        items_list.sort(key=lambda x: x['name'])
        
        while True:
            self.print_header("🏺 ITEMS DATABASE")
            
            print(f"{Fore.YELLOW}Options:\n")
            print(f"{Fore.GREEN}[1]{Fore.WHITE} Browse all items")
            print(f"{Fore.GREEN}[2]{Fore.WHITE} Search item by name")
            print(f"{Fore.RED}[0]{Fore.WHITE} Return\n")
            self.print_separator()
            
            choice = input(f"\n{Fore.CYAN}Your choice: {Fore.WHITE}").strip()
            
            if choice == '1':
                self._browse_items(items_list)
            elif choice == '2':
                self._search_items(items_list)
            elif choice == '0':
                return
    
    def _browse_items(self, items_list: List[Dict]):
        total_pages = (len(items_list) + 9) // 10
        page = 1
        
        while True:
            self.print_header(f"🏺 ITEMS DATABASE - Page {page}/{total_pages}")
            
            start = (page - 1) * 10
            end = start + 10
            page_items = items_list[start:end]
            
            for i, item in enumerate(page_items, start + 1):
                tags = ', '.join(item['tags'][:2]) if item['tags'] else 'Other'
                gold = item['gold']
                print(f"{Fore.YELLOW}[{i}] {Fore.WHITE}{item['name']:<30} {Fore.YELLOW}{gold}g  {Fore.LIGHTBLACK_EX}{tags}")
            
            print()
            self.print_separator()
            print(f"\n{Fore.GREEN}[N]{Fore.WHITE} Next  {Fore.GREEN}[P]{Fore.WHITE} Previous  {Fore.RED}[R]{Fore.WHITE} Return\n")
            
            choice = input(f"{Fore.CYAN}Your choice: {Fore.WHITE}").strip().upper()
            
            if choice == 'R':
                return
            elif choice == 'N' and page < total_pages:
                page += 1
            elif choice == 'P' and page > 1:
                page -= 1
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(items_list):
                    self.display_item_details(items_list[idx])
    
    def _search_items(self, items_list: List[Dict]):
        self.print_header("🔍 SEARCH ITEMS")
        
        query = input(f"{Fore.CYAN}Item name: {Fore.WHITE}").strip().lower()
        
        if not query:
            return
        
        results = [item for item in items_list if query in item['name'].lower()]
        
        if not results:
            print(f"\n{Fore.RED}No items found matching '{query}'")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            return
        
        self.print_header(f"🔍 SEARCH RESULTS - {query}")
        print(f"{Fore.GREEN}Found {len(results)} items:\n")
        
        for i, item in enumerate(results, 1):
            tags = ', '.join(item['tags'][:2]) if item['tags'] else 'Other'
            gold = item['gold']
            print(f"{Fore.YELLOW}[{i}] {Fore.WHITE}{item['name']:<30} {Fore.YELLOW}{gold}g  {Fore.LIGHTBLACK_EX}{tags}")
        
        print()
        self.print_separator()
        print(f"\n{Fore.GREEN}[1-{len(results)}]{Fore.WHITE} View details  {Fore.RED}[R]{Fore.WHITE} Return\n")
        
        choice = input(f"{Fore.CYAN}Your choice: {Fore.WHITE}").strip().upper()
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(results):
                self.display_item_details(results[idx])
    
    def display_item_details(self, item: Dict):
        self.print_header(f"🏺 {item['name'].upper()}")
        
        print(f"{Fore.YELLOW}Cost: {Fore.WHITE}{item['gold']}g")
        print(f"{Fore.YELLOW}Category: {Fore.WHITE}{', '.join(item['tags']) if item['tags'] else 'N/A'}")
        
        if item['description']:
            print(f"\n{Fore.CYAN}Description:")
            print(f"{Fore.WHITE}{item['description']}")
        
        stats = item['stats']
        if stats:
            print(f"\n{Fore.CYAN}{Style.BRIGHT}STATISTICS:")
            
            stat_mapping = {
                'FlatHPPoolMod': ('Health', 'HP'),
                'FlatMPPoolMod': ('Mana', 'MP'),
                'FlatMagicDamageMod': ('Ability Power', 'AP'),
                'FlatPhysicalDamageMod': ('Attack Damage', 'AD'),
                'FlatArmorMod': ('Armor', 'Armor'),
                'FlatSpellBlockMod': ('Magic Resist', 'MR'),
                'PercentAttackSpeedMod': ('Attack Speed', 'AS'),
                'PercentMovementSpeedMod': ('Movement Speed', 'MS'),
                'FlatCritChanceMod': ('Critical Strike', 'Crit'),
                'PercentLifeStealMod': ('Life Steal', 'LS'),
                'FlatHPRegenMod': ('Health Regen', 'HP5'),
                'PercentHPRegenMod': ('Health Regen %', 'HP5%'),
                'FlatMPRegenMod': ('Mana Regen', 'MP5'),
                'PercentMPRegenMod': ('Mana Regen %', 'MP5%'),
                'FlatMovementSpeedMod': ('Movement Speed', 'MS'),
            }
            
            for stat_key, stat_value in stats.items():
                if stat_value and stat_key in stat_mapping:
                    full_name, short = stat_mapping[stat_key]
                    
                    if 'Percent' in stat_key and 'Pool' not in stat_key:
                        display_value = f"+{stat_value * 100:.1f}%"
                    else:
                        display_value = f"+{stat_value:.0f}"
                    
                    print(f"  {Fore.GREEN}{short}: {Fore.WHITE}{display_value} {Fore.LIGHTBLACK_EX}({full_name})")
        
        print()
        self.print_separator()
        input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def generate_build(self):
        self.print_header("🛡️  BUILD GENERATOR")
        
        champion = input(f"{Fore.CYAN}Champion name: {Fore.WHITE}").strip()
        if not champion:
            return
        
        print(f"\n{Fore.YELLOW}Select role:")
        print(f"{Fore.GREEN}[1]{Fore.WHITE} Top")
        print(f"{Fore.GREEN}[2]{Fore.WHITE} Jungle")
        print(f"{Fore.GREEN}[3]{Fore.WHITE} Mid")
        print(f"{Fore.GREEN}[4]{Fore.WHITE} ADC")
        print(f"{Fore.GREEN}[5]{Fore.WHITE} Support")
        
        role_map = {'1': 'top', '2': 'jungle', '3': 'mid', '4': 'adc', '5': 'support'}
        role_choice = input(f"\n{Fore.CYAN}Role [default: Mid]: {Fore.WHITE}").strip() or '3'
        role = role_map.get(role_choice, 'mid')
        
        use_api = False
        if os.path.exists('riot_api_key.txt'):
            print(f"\n{Fore.GREEN}✓ API key detected")
            api_choice = input(f"{Fore.CYAN}Use Riot API for real high-elo data? [Y/n]: {Fore.WHITE}").strip().lower()
            use_api = api_choice != 'n'
            
            if use_api:
                print(f"\n{Fore.CYAN}⚡ Analyzing 50+ Challenger/Grandmaster games...")
                print(f"{Fore.YELLOW}This may take 1-2 minutes (rate limits apply)")
        else:
            print(f"\n{Fore.YELLOW}💡 Tip: Add riot_api_key.txt for real high-elo builds")
            print(f"{Fore.WHITE}   Get key at: https://developer.riotgames.com/")
            print(f"{Fore.WHITE}   See docs/riot_api_key.txt.example for instructions")
        
        build = self.build_gen.generate_build(champion, role, use_api=use_api)
        
        if not build:
            print(f"\n{Fore.RED}Champion '{champion}' not found!")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            return
        
        self.display_build(build)
    
    def display_build(self, build: Dict):
        self.print_header(f"🛡️  BUILD - {build['champion'].upper()}")
        
        type_color = Fore.MAGENTA if build['type'] == 'AP' else Fore.RED
        role = build.get('role', 'middle').capitalize()
        
        print(f"{Fore.YELLOW}Type: {type_color}{build['type']}{Fore.WHITE}  |  "
              f"{Fore.YELLOW}Role: {Fore.WHITE}{role}")
        
        stats = build.get('stats', {})
        source = build.get('source', 'expert_system')
        
        if stats and stats.get('winrate'):
            wr = stats['winrate']
            matches = stats.get('matches', 0)
            print(f"{Fore.YELLOW}Source: {Fore.GREEN}{source} {Fore.WHITE}({wr:.1f}% WR, {matches:,} games)")
        else:
            print(f"{Fore.YELLOW}Source: {Fore.CYAN}{source}")
        
        summoners = build.get('summoner_spells', [])
        if summoners:
            print(f"\n{Fore.CYAN}{Style.BRIGHT}✨ SUMMONER SPELLS:")
            print(f"{Fore.WHITE}  {' + '.join(summoners)}")
        
        runes = build.get('runes', {})
        if runes:
            print(f"\n{Fore.CYAN}{Style.BRIGHT}🔮 RUNES:")
            self.print_separator()
            print(f"{Fore.MAGENTA}{Style.BRIGHT}Keystone: {Fore.WHITE}{runes.get('keystone', 'N/A')}")
            print(f"{Fore.YELLOW}Primary: {Fore.WHITE}{runes.get('primary_path', 'N/A')}")
            print(f"{Fore.YELLOW}Secondary: {Fore.WHITE}{runes.get('secondary_path', 'N/A')}")
        
        starting_items = build.get('starting_items', [])
        if starting_items:
            print(f"\n{Fore.CYAN}{Style.BRIGHT}🎯 STARTING ITEMS:")
            self.print_separator()
            for item in starting_items:
                print(f"{Fore.GREEN}  • {Fore.WHITE}{item['name']}")
        
        core_items = build.get('core_items', [])
        if core_items:
            print(f"\n{Fore.CYAN}{Style.BRIGHT}⚔️  CORE BUILD (in order):")
            self.print_separator()
            for i, item in enumerate(core_items, 1):
                print(f"{Fore.YELLOW}[{i}] {Fore.WHITE}{Style.BRIGHT}{item['name']}")
        
        boots = build.get('boots')
        if boots:
            print(f"\n{Fore.CYAN}{Style.BRIGHT}👟 BOOTS:")
            print(f"{Fore.WHITE}  {boots['name']}")
        
        situational = build.get('situational_items', [])
        if situational:
            print(f"\n{Fore.CYAN}{Style.BRIGHT}🔄 SITUATIONAL ITEMS:")
            self.print_separator()
            for item in situational:
                context = item.get('context', 'Situational')
                print(f"{Fore.GREEN}  • {Fore.WHITE}{item['name']} {Fore.LIGHTBLACK_EX}({context})")
        
        print()
        self.print_separator()
        input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def analyze_gameplay(self):
        self.print_header("🤖 GAMEPLAY ANALYSIS")
        
        print(f"{Fore.YELLOW}Enter your game stats:\n")
        
        try:
            champion = input(f"{Fore.CYAN}Champion: {Fore.WHITE}").strip()
            role = input(f"{Fore.CYAN}Role (Top/Jungle/Mid/ADC/Support): {Fore.WHITE}").strip()
            duration = int(input(f"{Fore.CYAN}Duration (minutes): {Fore.WHITE}"))
            
            kills = int(input(f"{Fore.CYAN}Kills: {Fore.WHITE}"))
            deaths = int(input(f"{Fore.CYAN}Deaths: {Fore.WHITE}"))
            assists = int(input(f"{Fore.CYAN}Assists: {Fore.WHITE}"))
            
            cs = int(input(f"{Fore.CYAN}CS total: {Fore.WHITE}"))
            
            vision = int(input(f"{Fore.CYAN}Vision score: {Fore.WHITE}"))
            control_wards = int(input(f"{Fore.CYAN}Control wards bought: {Fore.WHITE}"))
            
            damage = int(input(f"{Fore.CYAN}Damage dealt: {Fore.WHITE}"))
            
            print(f"\n{Fore.YELLOW}Objectives:")
            dragons_participated = int(input(f"{Fore.CYAN}Dragons participated: {Fore.WHITE}"))
            total_dragons = int(input(f"{Fore.CYAN}Total team dragons: {Fore.WHITE}"))
            barons_participated = int(input(f"{Fore.CYAN}Barons participated: {Fore.WHITE}"))
            turrets_participated = int(input(f"{Fore.CYAN}Turrets participated: {Fore.WHITE}"))
            
            print(f"\n{Fore.YELLOW}Team context:")
            team_kda = float(input(f"{Fore.CYAN}Team average KDA: {Fore.WHITE}"))
            nemesis = input(f"{Fore.CYAN}Enemy champion that killed you most: {Fore.WHITE}").strip()
            
            game_duration_sec = duration * 60
            kda = (kills + assists) / deaths if deaths > 0 else kills + assists
            
            total_objectives = total_dragons + barons_participated
            objectives_participated = dragons_participated + barons_participated
            obj_participation = (objectives_participated / total_objectives * 100) if total_objectives > 0 else 0
            
            metrics = GameMetrics(
                game_duration=game_duration_sec,
                champion=champion,
                role=role,
                total_cs=cs,
                cs_per_min=cs / duration,
                jungle_cs=0,
                kills=kills,
                deaths=deaths,
                assists=assists,
                kda=kda,
                damage_dealt=damage,
                damage_taken=0,
                damage_per_min=damage / duration,
                vision_score=vision,
                wards_placed=vision // 2,
                wards_destroyed=vision // 4,
                control_wards_bought=control_wards,
                turret_plates=0,
                turrets_destroyed=turrets_participated,
                dragons_secured=dragons_participated,
                barons_secured=barons_participated,
                objective_participation=obj_participation,
                gold_earned=0,
                gold_per_min=0,
                time_cc_others=0,
                time_spent_dead=deaths * 30,
                team_average_kda=team_kda,
                nemesis_champion=nemesis if nemesis else "None"
            )
            
            analysis = self.gameplay_analyzer.analyze_game(metrics)
            self.display_analysis_results(analysis, metrics)
            
        except ValueError:
            print(f"\n{Fore.RED}Error: Invalid values!")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
        except KeyboardInterrupt:
            return
    
    def display_analysis_results(self, analysis: Dict, metrics: GameMetrics):
        self.print_header(f"📊 ANALYSIS - {metrics.champion.upper()}")
        
        print(f"{Fore.YELLOW}Game:")
        print(f"  Champion: {Fore.WHITE}{metrics.champion}")
        print(f"  Role: {Fore.WHITE}{metrics.role}")
        print(f"  Duration: {Fore.WHITE}{metrics.game_duration // 60} minutes")
        print(f"  KDA: {Fore.WHITE}{metrics.kills}/{metrics.deaths}/{metrics.assists} ({metrics.kda:.2f})")
        print(f"  CS: {Fore.WHITE}{metrics.total_cs} ({metrics.cs_per_min:.1f}/min)")
        
        print(f"\n{Fore.YELLOW}Context:")
        print(f"  Objective participation: {Fore.WHITE}{metrics.objective_participation:.0f}%")
        print(f"  Turrets destroyed: {Fore.WHITE}{metrics.turrets_destroyed}")
        print(f"  Team average KDA: {Fore.WHITE}{metrics.team_average_kda:.2f}")
        
        if metrics.kda < metrics.team_average_kda:
            kda_comparison = f"{Fore.RED}Below team average"
        elif metrics.kda > metrics.team_average_kda * 1.2:
            kda_comparison = f"{Fore.GREEN}Carrying the team!"
        else:
            kda_comparison = f"{Fore.YELLOW}Similar to team"
        print(f"  KDA comparison: {kda_comparison}")
        
        if metrics.nemesis_champion and metrics.nemesis_champion != "None":
            print(f"  {Fore.RED}Problematic champion: {Fore.WHITE}{metrics.nemesis_champion}")
        
        print()
        
        score = analysis["overall_score"]
        rank_estimate = self.gameplay_analyzer.get_rank_estimate(score)
        score_color = Fore.GREEN if score >= 75 else Fore.YELLOW if score >= 50 else Fore.RED
        
        print(f"{Fore.CYAN}{Style.BRIGHT}OVERALL SCORE: {score_color}{score:.1f}/100")
        print(f"{Fore.CYAN}Estimated rank: {Fore.WHITE}{rank_estimate}\n")
        
        print(f"{Fore.CYAN}{Style.BRIGHT}CATEGORY SCORES:\n")
        for category, cat_score in analysis["category_scores"].items():
            color = Fore.GREEN if cat_score >= 75 else Fore.YELLOW if cat_score >= 50 else Fore.RED
            bar_length = int(cat_score / 5)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            print(f"{Fore.WHITE}{category:<30} {color}{bar} {cat_score:.0f}/100")
        
        print()
        
        if analysis["critical_issues"]:
            print(f"{Fore.RED}{Style.BRIGHT}🚨 CRITICAL ISSUES:\n")
            for issue in analysis["critical_issues"][:5]:
                print(f"{Fore.RED}  ✗ {issue}")
            print()
        
        if analysis["weaknesses"]:
            print(f"{Fore.YELLOW}{Style.BRIGHT}⚠️  AREAS TO IMPROVE:\n")
            for weakness in analysis["weaknesses"][:5]:
                print(f"{Fore.YELLOW}  • {weakness}")
            print()
        
        if analysis["strengths"]:
            print(f"{Fore.GREEN}{Style.BRIGHT}✅ STRENGTHS:\n")
            for strength in analysis["strengths"][:5]:
                print(f"{Fore.GREEN}  ✓ {strength}")
            print()
        
        if analysis["recommendations"]:
            print(f"{Fore.CYAN}{Style.BRIGHT}💡 TOP RECOMMENDATIONS:\n")
            for i, rec in enumerate(analysis["recommendations"][:7], 1):
                print(f"{Fore.CYAN}  {i}. {Fore.WHITE}{rec}")
            print()
        
        self.print_separator()
        input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def run(self):
        while True:
            self.display_main_menu()
            choice = input(f"{Fore.CYAN}Your choice: {Fore.WHITE}").strip()
            
            if choice == '1':
                self.display_champions_list()
            elif choice == '2':
                self.search_champion()
            elif choice == '3':
                self.display_items_database()
            elif choice == '4':
                self.generate_build()
            elif choice == '5':
                self.analyze_gameplay()
            elif choice == '0':
                self.print_header("👋 GOODBYE!")
                print(f"{Fore.YELLOW}Thanks for using LoL Expert Build System!")
                print(f"{Fore.CYAN}See you on Summoner's Rift! ⚔️\n")
                break


def main():
    try:
        manager = LoLManager()
        manager.run()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Program interrupted by user.")
    except Exception as e:
        print(f"\n{Fore.RED}Unexpected error: {e}")


if __name__ == "__main__":
    main()
