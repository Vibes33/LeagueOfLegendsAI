#!/usr/bin/env python3
"""
League of Legends Champion Manager
Un programme terminal interactif pour consulter les champions, builds, items et runes
"""

import json
import os
from typing import Dict, List, Any
from colorama import init, Fore, Back, Style
from build_recommender import BuildRecommender
from gameplay_analyzer import GameplayAnalyzer, GameMetrics, TimelineEvent

# Initialiser colorama pour les couleurs terminal
init(autoreset=True)


class LoLManager:
    def __init__(self):
        self.champions_data = self.load_champions()
        self.build_recommender = BuildRecommender()
        self.gameplay_analyzer = GameplayAnalyzer()
        self.current_page = 1
        self.champions_per_page = 10
        
    def load_champions(self) -> Dict:
        """Charge les données des champions depuis le fichier JSON"""
        try:
            with open('champions_data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"{Fore.RED}Erreur: Fichier champions_data.json introuvable!")
            return {"champions": []}
    
    def clear_screen(self):
        """Nettoie l'écran du terminal"""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def print_header(self, title: str):
        """Affiche un en-tête stylisé"""
        self.clear_screen()
        width = 80
        print("\n" + "=" * width)
        print(f"{Fore.CYAN}{Style.BRIGHT}{title.center(width)}")
        print("=" * width + "\n")
    
    def print_separator(self):
        """Affiche une ligne de séparation"""
        print(f"{Fore.BLUE}" + "-" * 80)
    
    def get_type_color(self, champion_type: str) -> str:
        """Retourne la couleur en fonction du type de champion"""
        if champion_type == "AP":
            return Fore.MAGENTA
        elif champion_type == "AD":
            return Fore.RED
        else:
            return Fore.WHITE
    
    def display_main_menu(self):
        """Affiche le menu principal"""
        self.print_header("⚔️  LEAGUE OF LEGENDS - CHAMPION MANAGER  ⚔️")
        
        print(f"{Fore.YELLOW}{Style.BRIGHT}MENU PRINCIPAL:\n")
        print(f"{Fore.GREEN}[1]{Fore.WHITE} 📋 Liste des Champions")
        print(f"{Fore.GREEN}[2]{Fore.WHITE} 🔍 Rechercher un Champion")
        print(f"{Fore.GREEN}[3]{Fore.WHITE} 🛠️  Builds & Recommandations")
        print(f"{Fore.GREEN}[4]{Fore.WHITE} ⚔️  Items List")
        print(f"{Fore.GREEN}[5]{Fore.WHITE} 🔮 Runes List")
        print(f"{Fore.GREEN}[6]{Fore.WHITE} 🤖 Analyse IA Gameplay")
        print(f"{Fore.RED}[0]{Fore.WHITE} ❌ Quitter\n")
        self.print_separator()
    
    def display_champions_list(self):
        """Affiche la liste des champions avec pagination"""
        while True:
            self.print_header("📋 LISTE DES CHAMPIONS")
            
            champions = self.champions_data.get("champions", [])
            total_champions = len(champions)
            
            if total_champions == 0:
                print(f"{Fore.RED}Aucun champion trouvé!")
                input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...")
                return
            
            # Calculer la pagination
            start_idx = (self.current_page - 1) * self.champions_per_page
            end_idx = min(start_idx + self.champions_per_page, total_champions)
            total_pages = (total_champions + self.champions_per_page - 1) // self.champions_per_page
            
            # Afficher les champions
            print(f"{Fore.CYAN}Page {self.current_page}/{total_pages} - Total: {total_champions} champions\n")
            
            for i, champion in enumerate(champions[start_idx:end_idx], start=start_idx + 1):
                type_color = self.get_type_color(champion['type'])
                print(f"{Fore.YELLOW}[{i}] {Fore.WHITE}{champion['name']:<15} "
                      f"{type_color}[{champion['type']}]{Fore.WHITE}  "
                      f"{Fore.LIGHTBLACK_EX}{champion.get('role', 'N/A')}")
            
            print()
            self.print_separator()
            print(f"\n{Fore.GREEN}[N]{Fore.WHITE} Page suivante  "
                  f"{Fore.GREEN}[P]{Fore.WHITE} Page précédente  "
                  f"{Fore.GREEN}[1-{total_champions}]{Fore.WHITE} Détails champion  "
                  f"{Fore.RED}[R]{Fore.WHITE} Retour\n")
            
            choice = input(f"{Fore.CYAN}Votre choix: {Fore.WHITE}").strip().upper()
            
            if choice == 'R':
                self.current_page = 1
                return
            elif choice == 'N' and self.current_page < total_pages:
                self.current_page += 1
            elif choice == 'P' and self.current_page > 1:
                self.current_page -= 1
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < total_champions:
                    self.display_champion_details(champions[idx])
    
    def display_champion_details(self, champion: Dict):
        """Affiche les détails complets d'un champion"""
        self.print_header(f"⚔️  {champion['name'].upper()}  ⚔️")
        
        type_color = self.get_type_color(champion['type'])
        
        # Informations générales
        print(f"{Fore.YELLOW}Type: {type_color}{champion['type']}{Fore.WHITE}  |  "
              f"{Fore.YELLOW}Rôle: {Fore.WHITE}{champion.get('role', 'N/A')}\n")
        
        # Statistiques
        print(f"{Fore.CYAN}{Style.BRIGHT}📊 STATISTIQUES DE BASE:")
        self.print_separator()
        stats = champion['stats']
        print(f"{Fore.GREEN}❤️  PV: {Fore.WHITE}{stats['hp']} (+{stats['hp_per_level']}/niveau)")
        
        if stats['mana'] > 0:
            print(f"{Fore.BLUE}💧 Mana: {Fore.WHITE}{stats['mana']} (+{stats['mana_per_level']}/niveau)")
        else:
            print(f"{Fore.BLUE}⚡ Énergie/Ressource alternative")
        
        print(f"{Fore.YELLOW}🛡️  Armure: {Fore.WHITE}{stats['armor']}")
        print(f"{Fore.MAGENTA}🔮 RM: {Fore.WHITE}{stats['magic_resist']}")
        print(f"{Fore.RED}⚔️  AD: {Fore.WHITE}{stats['attack_damage']}")
        print(f"{Fore.LIGHTCYAN_EX}⚡ AS: {Fore.WHITE}{stats['attack_speed']}")
        print(f"{Fore.LIGHTYELLOW_EX}👟 MS: {Fore.WHITE}{stats['movement_speed']}")
        
        # Capacités
        print(f"\n{Fore.CYAN}{Style.BRIGHT}✨ CAPACITÉS:")
        self.print_separator()
        
        abilities = champion['abilities']
        
        # Passif
        passive = abilities['passive']
        print(f"\n{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}[PASSIF] {passive['name']}")
        print(f"{Fore.WHITE}{passive['description']}")
        
        # Sorts Q, W, E, R
        for key, label in [('q', 'Q'), ('w', 'W'), ('e', 'E'), ('r', 'R')]:
            if key in abilities:
                spell = abilities[key]
                print(f"\n{Fore.LIGHTGREEN_EX}{Style.BRIGHT}[{label}] {spell['name']}")
                print(f"{Fore.WHITE}{spell['description']}")
                
                # Cooldown
                cd = spell.get('cooldown', [])
                if cd:
                    cd_str = "/".join(map(str, cd))
                    print(f"{Fore.CYAN}⏱️  CD: {Fore.WHITE}{cd_str}s")
                
                # Coût en mana
                mana = spell.get('mana_cost', [])
                if mana and any(m > 0 for m in mana):
                    mana_str = "/".join(map(str, mana))
                    resource = spell.get('resource', 'Mana')
                    print(f"{Fore.BLUE}💧 Coût: {Fore.WHITE}{mana_str} {resource}")
                
                # Dégâts
                damage = spell.get('damage', [])
                if damage and any(d > 0 for d in damage):
                    damage_str = "/".join(map(str, damage))
                    print(f"{Fore.RED}💥 Dégâts: {Fore.WHITE}{damage_str}")
        
        print()
        self.print_separator()
        input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...")
    
    def search_champion(self):
        """Recherche un champion par nom"""
        self.print_header("🔍 RECHERCHER UN CHAMPION")
        
        search_term = input(f"{Fore.CYAN}Entrez le nom du champion: {Fore.WHITE}").strip().lower()
        
        if not search_term:
            return
        
        champions = self.champions_data.get("champions", [])
        results = [c for c in champions if search_term in c['name'].lower()]
        
        if not results:
            print(f"\n{Fore.RED}Aucun champion trouvé avec '{search_term}'")
            input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...")
            return
        
        if len(results) == 1:
            self.display_champion_details(results[0])
        else:
            print(f"\n{Fore.GREEN}Champions trouvés:\n")
            for i, champion in enumerate(results, 1):
                type_color = self.get_type_color(champion['type'])
                print(f"{Fore.YELLOW}[{i}] {Fore.WHITE}{champion['name']} "
                      f"{type_color}[{champion['type']}]")
            
            print()
            choice = input(f"\n{Fore.CYAN}Choisissez un champion (1-{len(results)}) ou R pour retour: {Fore.WHITE}").strip()
            
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(results):
                    self.display_champion_details(results[idx])
    
    def coming_soon(self, feature: str):
        """Affiche un message pour les fonctionnalités à venir"""
        self.print_header(f"🚧 {feature.upper()} - À VENIR")
        print(f"{Fore.YELLOW}Cette fonctionnalité sera disponible prochainement!")
        print(f"\n{Fore.LIGHTBLACK_EX}Restez connecté pour les mises à jour...")
        input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...")
    
    def display_builds_menu(self):
        """Affiche le menu des builds"""
        while True:
            self.print_header("🛠️  BUILDS & RECOMMANDATIONS")
            
            print(f"{Fore.YELLOW}{Style.BRIGHT}OPTIONS:\n")
            print(f"{Fore.GREEN}[1]{Fore.WHITE} 🎯 Recommander un Build pour un Champion")
            print(f"{Fore.GREEN}[2]{Fore.WHITE} 📚 Voir les Builds Pré-configurés")
            print(f"{Fore.GREEN}[3]{Fore.WHITE} 🔍 Analyser une Composition (Counter Items)")
            print(f"{Fore.RED}[R]{Fore.WHITE} ⬅️  Retour\n")
            self.print_separator()
            
            choice = input(f"\n{Fore.CYAN}Votre choix: {Fore.WHITE}").strip().upper()
            
            if choice == '1':
                self.recommend_build_interactive()
            elif choice == '2':
                self.display_preconfigured_builds()
            elif choice == '3':
                self.analyze_composition()
            elif choice == 'R':
                return
    
    def recommend_build_interactive(self):
        """Recommandation de build interactive"""
        self.print_header("🎯 RECOMMANDATION DE BUILD")
        
        # Sélection du champion
        champion_name = input(f"{Fore.CYAN}Nom du champion: {Fore.WHITE}").strip()
        
        champions = self.champions_data.get("champions", [])
        champion = None
        for c in champions:
            if c['name'].lower() == champion_name.lower():
                champion = c
                break
        
        if not champion:
            print(f"\n{Fore.RED}Champion non trouvé!")
            input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...")
            return
        
        # Composition ennemie (optionnel)
        print(f"\n{Fore.YELLOW}Composition ennemie (optionnel):")
        print(f"{Fore.LIGHTBLACK_EX}Entrez les types séparés par des virgules (ex: AP,AD,Tank,AP,AD)")
        print(f"{Fore.LIGHTBLACK_EX}Ou appuyez sur Entrée pour build standard\n")
        
        enemy_input = input(f"{Fore.CYAN}Composition: {Fore.WHITE}").strip()
        enemy_comp = [e.strip() for e in enemy_input.split(',')] if enemy_input else None
        
        # Génération du build
        build = self.build_recommender.get_build_for_champion(
            champion['name'], 
            champion['type'],
            champion.get('role', ''),
            enemy_comp
        )
        
        self.display_build_details(build)
    
    def display_build_details(self, build: Dict):
        """Affiche les détails d'un build"""
        self.print_header(f"🛠️  BUILD - {build['champion'].upper()}")
        
        type_color = self.get_type_color(build['type'])
        
        # Informations générales
        print(f"{Fore.YELLOW}Type: {type_color}{build['type']}{Fore.WHITE}  |  "
              f"{Fore.YELLOW}Rôle: {Fore.WHITE}{build.get('role', 'N/A')}")
        
        if build.get('playstyle'):
            print(f"{Fore.YELLOW}Style: {Fore.WHITE}{build['playstyle']}")
        
        print()
        
        # Runes
        print(f"{Fore.CYAN}{Style.BRIGHT}🔮 RUNES:")
        self.print_separator()
        runes = build.get('runes', {})
        
        if isinstance(runes, dict):
            keystone = runes.get('keystone')
            if keystone:
                if isinstance(keystone, dict):
                    print(f"{Fore.MAGENTA}{Style.BRIGHT}Keystone: {Fore.WHITE}{keystone.get('name', 'N/A')}")
                    print(f"{Fore.LIGHTBLACK_EX}{keystone.get('description', '')}")
                else:
                    print(f"{Fore.MAGENTA}{Style.BRIGHT}Keystone: {Fore.WHITE}{keystone}")
            
            primary = runes.get('primary_path', 'N/A')
            secondary = runes.get('secondary_path', 'N/A')
            print(f"\n{Fore.YELLOW}Primaire: {Fore.WHITE}{primary}")
            print(f"{Fore.YELLOW}Secondaire: {Fore.WHITE}{secondary}")
            
            if runes.get('description'):
                print(f"{Fore.LIGHTBLACK_EX}{runes['description']}")
        
        # Items
        print(f"\n{Fore.CYAN}{Style.BRIGHT}⚔️  BUILD PATH:")
        self.print_separator()
        
        items = build.get('items', [])
        for i, item in enumerate(items, 1):
            if isinstance(item, dict):
                if 'name' in item:
                    # Format build_database
                    item_name = item.get('name', 'Unknown')
                    reason = item.get('reason', '')
                    item_category = item.get('category', '')
                    
                    # Couleur selon catégorie
                    if 'Mythic' in item_category or item_name in ['Luden\'s Tempest', 'Kraken Slayer', 'Immortal Shieldbow', 'Galeforce', 'Liandry\'s Torment', 'Hextech Rocketbelt', 'Sunfire Aegis']:
                        color = Fore.YELLOW
                    elif 'Boots' in item_category or 'Greaves' in item_name or 'Shoes' in item_name:
                        color = Fore.LIGHTCYAN_EX
                    else:
                        color = Fore.WHITE
                    
                    print(f"{Fore.GREEN}[{i}] {color}{Style.BRIGHT}{item_name}")
                    if reason:
                        print(f"    {Fore.LIGHTBLACK_EX}└─ {reason}")
                else:
                    # Format recommender (item complet)
                    print(f"{Fore.GREEN}[{i}] {Fore.WHITE}{Style.BRIGHT}{item.get('name', 'Unknown')}")
                    
                    stats = item.get('stats', {})
                    stats_str = []
                    if stats.get('ability_power'):
                        stats_str.append(f"{Fore.MAGENTA}{stats['ability_power']} AP")
                    if stats.get('attack_damage'):
                        stats_str.append(f"{Fore.RED}{stats['attack_damage']} AD")
                    if stats.get('health'):
                        stats_str.append(f"{Fore.GREEN}{stats['health']} HP")
                    if stats.get('armor'):
                        stats_str.append(f"{Fore.YELLOW}{stats['armor']} Armor")
                    if stats.get('magic_resist'):
                        stats_str.append(f"{Fore.CYAN}{stats['magic_resist']} MR")
                    
                    if stats_str:
                        print(f"    {Fore.LIGHTBLACK_EX}└─ {Fore.WHITE}" + " | ".join(stats_str))
        
        # Power spikes
        if build.get('power_spikes'):
            print(f"\n{Fore.CYAN}{Style.BRIGHT}⚡ POWER SPIKES:")
            self.print_separator()
            for spike in build['power_spikes']:
                print(f"{Fore.YELLOW}• {Fore.WHITE}{spike}")
        
        # Note si build généré
        if build.get('generated'):
            print(f"\n{Fore.LIGHTBLACK_EX}ℹ️  Build généré automatiquement basé sur l'analyse contextuelle")
        
        print()
        self.print_separator()
        input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...")
    
    def display_preconfigured_builds(self):
        """Affiche les builds pré-configurés"""
        while True:
            self.print_header("📚 BUILDS PRÉ-CONFIGURÉS")
            
            builds = self.build_recommender.builds_database.get('builds', [])
            
            if not builds:
                print(f"{Fore.RED}Aucun build pré-configuré disponible!")
                input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...")
                return
            
            print(f"{Fore.CYAN}Total: {len(builds)} builds disponibles\n")
            
            for i, build in enumerate(builds, 1):
                type_color = self.get_type_color(build['type'])
                print(f"{Fore.YELLOW}[{i}] {Fore.WHITE}{build['champion']:<15} "
                      f"{type_color}[{build['type']}]{Fore.WHITE}  "
                      f"{Fore.LIGHTBLACK_EX}{build.get('role', 'N/A')}")
            
            print()
            self.print_separator()
            print(f"\n{Fore.GREEN}[1-{len(builds)}]{Fore.WHITE} Voir détails  {Fore.RED}[R]{Fore.WHITE} Retour\n")
            
            choice = input(f"{Fore.CYAN}Votre choix: {Fore.WHITE}").strip().upper()
            
            if choice == 'R':
                return
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(builds):
                    self.display_build_details(builds[idx])
    
    def analyze_composition(self):
        """Analyse une composition et suggère des counter items"""
        self.print_header("🔍 ANALYSE DE COMPOSITION")
        
        print(f"{Fore.YELLOW}Types d'ennemis (séparés par des virgules):")
        print(f"{Fore.LIGHTBLACK_EX}Exemples: Tank, AP, AD, Assassin, Healing, Burst\n")
        
        threats = input(f"{Fore.CYAN}Menaces: {Fore.WHITE}").strip()
        
        if not threats:
            return
        
        threat_list = [t.strip() for t in threats.split(',')]
        
        # Récupérer les items counter
        counter_items = self.build_recommender.get_counter_items(threat_list)
        
        self.print_header("🔍 ITEMS RECOMMANDÉS")
        
        print(f"{Fore.YELLOW}Contre: {Fore.WHITE}{', '.join(threat_list)}\n")
        
        if not counter_items:
            print(f"{Fore.RED}Aucun item spécifique trouvé pour ces menaces.")
        else:
            print(f"{Fore.GREEN}Items recommandés:\n")
            
            for item in counter_items[:10]:  # Limite à 10
                type_color = Fore.MAGENTA if item['type'] == 'AP' else Fore.RED if item['type'] == 'AD' else Fore.CYAN
                
                print(f"{type_color}▸ {Fore.WHITE}{Style.BRIGHT}{item['name']}")
                print(f"  {Fore.LIGHTBLACK_EX}{item['description']}")
                
                # Tags
                tags = item.get('tags', [])
                if tags:
                    tags_str = ', '.join(tags)
                    print(f"  {Fore.YELLOW}Tags: {Fore.WHITE}{tags_str}")
                
                # Stats principales
                stats = item.get('stats', {})
                stats_list = []
                if stats.get('ability_power'):
                    stats_list.append(f"{stats['ability_power']} AP")
                if stats.get('attack_damage'):
                    stats_list.append(f"{stats['attack_damage']} AD")
                if stats.get('armor'):
                    stats_list.append(f"{stats['armor']} Armor")
                if stats.get('magic_resist'):
                    stats_list.append(f"{stats['magic_resist']} MR")
                
                if stats_list:
                    print(f"  {Fore.CYAN}Stats: {Fore.WHITE}{' | '.join(stats_list)}")
                
                print()
        
        self.print_separator()
        input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...")
    
    def display_items_list(self):
        """Affiche la liste complète des items"""
        while True:
            self.print_header("⚔️  LISTE DES ITEMS")
            
            print(f"{Fore.YELLOW}{Style.BRIGHT}FILTRER PAR:\n")
            print(f"{Fore.GREEN}[1]{Fore.WHITE} Tous les Items")
            print(f"{Fore.GREEN}[2]{Fore.WHITE} Items AP")
            print(f"{Fore.GREEN}[3]{Fore.WHITE} Items AD")
            print(f"{Fore.GREEN}[4]{Fore.WHITE} Items Tank")
            print(f"{Fore.GREEN}[5]{Fore.WHITE} Items Mythiques")
            print(f"{Fore.GREEN}[6]{Fore.WHITE} Rechercher un Item")
            print(f"{Fore.RED}[R]{Fore.WHITE} ⬅️  Retour\n")
            self.print_separator()
            
            choice = input(f"\n{Fore.CYAN}Votre choix: {Fore.WHITE}").strip().upper()
            
            if choice == 'R':
                return
            elif choice == '1':
                self.show_items_by_filter('All')
            elif choice == '2':
                self.show_items_by_filter('AP')
            elif choice == '3':
                self.show_items_by_filter('AD')
            elif choice == '4':
                self.show_items_by_filter('Tank')
            elif choice == '5':
                self.show_items_by_filter('Mythic')
            elif choice == '6':
                self.search_items()
    
    def show_items_by_filter(self, filter_type: str):
        """Affiche les items selon un filtre"""
        self.print_header(f"⚔️  ITEMS - {filter_type.upper()}")
        
        all_items = self.build_recommender.items_data.get('items', [])
        
        if filter_type == 'All':
            filtered = all_items
        elif filter_type == 'Mythic':
            filtered = [i for i in all_items if i.get('category') == 'Mythic']
        else:
            filtered = [i for i in all_items if i.get('type') == filter_type]
        
        if not filtered:
            print(f"{Fore.RED}Aucun item trouvé pour ce filtre!")
            input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...")
            return
        
        print(f"{Fore.CYAN}Total: {len(filtered)} items\n")
        
        for item in filtered:
            type_color = Fore.MAGENTA if item['type'] == 'AP' else Fore.RED if item['type'] == 'AD' else Fore.CYAN
            category = item.get('category', 'Item')
            
            print(f"{type_color}▸ {Fore.WHITE}{Style.BRIGHT}{item['name']} {Fore.YELLOW}[{category}]")
            print(f"  {Fore.LIGHTBLACK_EX}{item['description']}")
            
            # Stats
            stats = item.get('stats', {})
            stats_parts = []
            for key, value in stats.items():
                if isinstance(value, (int, float)):
                    key_display = key.replace('_', ' ').title()
                    stats_parts.append(f"{key_display}: {value}")
            
            if stats_parts:
                print(f"  {Fore.CYAN}Stats: {Fore.WHITE}{' | '.join(stats_parts)}")
            
            print(f"  {Fore.YELLOW}Coût: {Fore.WHITE}{item.get('cost', 'N/A')}g")
            print()
        
        self.print_separator()
        input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...")
    
    def search_items(self):
        """Recherche d'items"""
        self.print_header("🔍 RECHERCHER UN ITEM")
        
        query = input(f"{Fore.CYAN}Nom de l'item: {Fore.WHITE}").strip()
        
        if not query:
            return
        
        results = self.build_recommender.search_items(query)
        
        if not results:
            print(f"\n{Fore.RED}Aucun item trouvé avec '{query}'")
            input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...")
            return
        
        self.print_header(f"🔍 RÉSULTATS - {query}")
        
        for item in results:
            type_color = Fore.MAGENTA if item['type'] == 'AP' else Fore.RED if item['type'] == 'AD' else Fore.CYAN
            
            print(f"{type_color}▸ {Fore.WHITE}{Style.BRIGHT}{item['name']}")
            print(f"  {Fore.LIGHTBLACK_EX}{item['description']}")
            print(f"  {Fore.YELLOW}Coût: {Fore.WHITE}{item.get('cost', 'N/A')}g\n")
        
        self.print_separator()
        input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...")
    
    def display_runes_list(self):
        """Affiche la liste des runes"""
        while True:
            self.print_header("🔮 LISTE DES RUNES")
            
            rune_paths = self.build_recommender.runes_data.get('rune_paths', {})
            
            print(f"{Fore.YELLOW}{Style.BRIGHT}CHEMINS DE RUNES:\n")
            
            paths = list(rune_paths.keys())
            for i, path in enumerate(paths, 1):
                path_info = rune_paths[path]
                print(f"{Fore.GREEN}[{i}] {Fore.WHITE}{path} - {Fore.LIGHTBLACK_EX}{path_info.get('description', '')}")
            
            print(f"\n{Fore.GREEN}[A]{Fore.WHITE} Voir toutes les Keystones")
            print(f"{Fore.RED}[R]{Fore.WHITE} ⬅️  Retour\n")
            self.print_separator()
            
            choice = input(f"\n{Fore.CYAN}Votre choix: {Fore.WHITE}").strip().upper()
            
            if choice == 'R':
                return
            elif choice == 'A':
                self.show_all_keystones()
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(paths):
                    self.show_runes_by_path(paths[idx])
    
    def show_all_keystones(self):
        """Affiche toutes les keystones"""
        self.print_header("🔮 RUNES KEYSTONES")
        
        runes = self.build_recommender.runes_data.get('runes', [])
        keystones = [r for r in runes if r['type'] == 'Keystone']
        
        for rune in keystones:
            path_color = self._get_path_color(rune['path'])
            
            print(f"{path_color}▸ {Fore.WHITE}{Style.BRIGHT}{rune['name']} {Fore.YELLOW}[{rune['path']}]")
            print(f"  {Fore.LIGHTBLACK_EX}{rune['description']}")
            
            champions = rune.get('champions', [])
            if champions:
                print(f"  {Fore.CYAN}Champions: {Fore.WHITE}{', '.join(champions[:5])}")
            print()
        
        self.print_separator()
        input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...")
    
    def show_runes_by_path(self, path: str):
        """Affiche les runes d'un chemin spécifique"""
        self.print_header(f"🔮 RUNES - {path.upper()}")
        
        runes = self.build_recommender.runes_data.get('runes', [])
        path_runes = [r for r in runes if r['path'] == path and r['type'] == 'Keystone']
        
        path_info = self.build_recommender.runes_data.get('rune_paths', {}).get(path, {})
        print(f"{Fore.YELLOW}Description: {Fore.WHITE}{path_info.get('description', '')}")
        print(f"{Fore.YELLOW}Bonus: {Fore.WHITE}{path_info.get('bonus', '')}\n")
        
        self.print_separator()
        print(f"\n{Fore.CYAN}{Style.BRIGHT}KEYSTONES:\n")
        
        for rune in path_runes:
            path_color = self._get_path_color(path)
            
            print(f"{path_color}▸ {Fore.WHITE}{Style.BRIGHT}{rune['name']}")
            print(f"  {Fore.LIGHTBLACK_EX}{rune['description']}")
            
            champions = rune.get('champions', [])
            if champions:
                print(f"  {Fore.CYAN}Bons pour: {Fore.WHITE}{', '.join(champions)}")
            print()
        
        self.print_separator()
        input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...")
    
    def _get_path_color(self, path: str) -> str:
        """Retourne la couleur associée à un chemin de runes"""
        colors = {
            'Precision': Fore.YELLOW,
            'Domination': Fore.RED,
            'Sorcery': Fore.BLUE,
            'Resolve': Fore.GREEN,
            'Inspiration': Fore.CYAN
        }
        return colors.get(path, Fore.WHITE)
    
    def display_gameplay_analysis_menu(self):
        """Menu d'analyse gameplay IA"""
        while True:
            self.print_header("🤖 ANALYSE IA GAMEPLAY")
            
            print(f"{Fore.YELLOW}{Style.BRIGHT}OPTIONS:\n")
            print(f"{Fore.GREEN}[1]{Fore.WHITE} 📊 Analyser une Partie (Données Manuelles)")
            print(f"{Fore.GREEN}[2]{Fore.WHITE} 📁 Analyser depuis un Fichier JSON")
            print(f"{Fore.GREEN}[3]{Fore.WHITE} 📈 Voir un Exemple d'Analyse")
            print(f"{Fore.GREEN}[4]{Fore.WHITE} 📚 Voir les Benchmarks par Rôle")
            print(f"{Fore.YELLOW}[5]{Fore.LIGHTBLACK_EX} 🔗 Analyser un Replay (À venir)")
            print(f"{Fore.RED}[R]{Fore.WHITE} ⬅️  Retour\n")
            self.print_separator()
            
            choice = input(f"\n{Fore.CYAN}Votre choix: {Fore.WHITE}").strip().upper()
            
            if choice == 'R':
                return
            elif choice == '1':
                self.analyze_game_manual()
            elif choice == '2':
                self.analyze_game_from_file()
            elif choice == '3':
                self.show_example_analysis()
            elif choice == '4':
                self.show_benchmarks()
            elif choice == '5':
                self.coming_soon_replay()
    
    def analyze_game_manual(self):
        """Analyse manuelle d'une partie"""
        self.print_header("📊 ANALYSE MANUELLE")
        
        print(f"{Fore.YELLOW}Entrez les statistiques de votre partie:\n")
        
        try:
            # Infos de base
            champion = input(f"{Fore.CYAN}Champion: {Fore.WHITE}").strip()
            role = input(f"{Fore.CYAN}Rôle (Top/Jungle/Mid/ADC/Support): {Fore.WHITE}").strip()
            duration = int(input(f"{Fore.CYAN}Durée (minutes): {Fore.WHITE}"))
            
            # KDA
            kills = int(input(f"{Fore.CYAN}Kills: {Fore.WHITE}"))
            deaths = int(input(f"{Fore.CYAN}Deaths: {Fore.WHITE}"))
            assists = int(input(f"{Fore.CYAN}Assists: {Fore.WHITE}"))
            
            # CS
            cs = int(input(f"{Fore.CYAN}CS total: {Fore.WHITE}"))
            
            # Vision
            vision = int(input(f"{Fore.CYAN}Vision score: {Fore.WHITE}"))
            control_wards = int(input(f"{Fore.CYAN}Control wards achetés: {Fore.WHITE}"))
            
            # Dégâts
            damage = int(input(f"{Fore.CYAN}Dégâts infligés: {Fore.WHITE}"))
            
            # Objectifs
            print(f"\n{Fore.YELLOW}Objectifs:")
            dragons_participated = int(input(f"{Fore.CYAN}Dragons auxquels vous avez participé: {Fore.WHITE}"))
            total_dragons = int(input(f"{Fore.CYAN}Total de dragons pris par votre équipe: {Fore.WHITE}"))
            barons_participated = int(input(f"{Fore.CYAN}Barons auxquels vous avez participé: {Fore.WHITE}"))
            turrets_participated = int(input(f"{Fore.CYAN}Tours détruites où vous avez participé: {Fore.WHITE}"))
            
            # Contexte équipe
            print(f"\n{Fore.YELLOW}Contexte d'équipe:")
            team_kda = float(input(f"{Fore.CYAN}KDA moyen de vos alliés (ex: 2.5): {Fore.WHITE}"))
            nemesis = input(f"{Fore.CYAN}Champion ennemi qui vous a le plus tué: {Fore.WHITE}").strip()
            
            # Créer les metrics
            game_duration_sec = duration * 60
            kda = (kills + assists) / deaths if deaths > 0 else kills + assists
            
            # Calcul participation objectifs (%)
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
                nemesis_champion=nemesis if nemesis else "Aucun"
            )
            
            # Analyser
            analysis = self.gameplay_analyzer.analyze_game(metrics)
            self.display_analysis_results(analysis, metrics)
            
        except ValueError:
            print(f"\n{Fore.RED}Erreur: Valeurs invalides!")
            input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...")
        except KeyboardInterrupt:
            return
    
    def analyze_game_from_file(self):
        """Analyse depuis un fichier JSON"""
        self.print_header("📁 ANALYSE DEPUIS FICHIER")
        
        print(f"{Fore.YELLOW}Format JSON attendu:")
        print(f"{Fore.LIGHTBLACK_EX}{{")
        print(f'{Fore.LIGHTBLACK_EX}  "champion": "Ahri",')
        print(f'{Fore.LIGHTBLACK_EX}  "role": "Mid",')
        print(f'{Fore.LIGHTBLACK_EX}  "duration": 30,')
        print(f'{Fore.LIGHTBLACK_EX}  "kills": 5, "deaths": 3, "assists": 8,')
        print(f'{Fore.LIGHTBLACK_EX}  "cs": 210, ...}}\n')
        
        filepath = input(f"{Fore.CYAN}Chemin du fichier JSON: {Fore.WHITE}").strip()
        
        if not filepath:
            return
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Parser les données
            duration_min = data.get('duration', 30)
            game_duration_sec = duration_min * 60
            cs = data.get('cs', 0)
            damage = data.get('damage', 0)
            deaths = data.get('deaths', 1)
            
            metrics = GameMetrics(
                game_duration=game_duration_sec,
                champion=data.get('champion', 'Unknown'),
                role=data.get('role', 'Mid'),
                total_cs=cs,
                cs_per_min=cs / duration_min,
                jungle_cs=data.get('jungle_cs', 0),
                kills=data.get('kills', 0),
                deaths=deaths,
                assists=data.get('assists', 0),
                kda=(data.get('kills', 0) + data.get('assists', 0)) / deaths if deaths > 0 else 0,
                damage_dealt=damage,
                damage_taken=data.get('damage_taken', 0),
                damage_per_min=damage / duration_min,
                vision_score=data.get('vision', 0),
                wards_placed=data.get('wards_placed', 0),
                wards_destroyed=data.get('wards_destroyed', 0),
                control_wards_bought=data.get('control_wards', 0),
                turret_plates=data.get('turret_plates', 0),
                turrets_destroyed=data.get('turrets', 0),
                dragons_secured=data.get('dragons', 0),
                barons_secured=data.get('barons', 0),
                objective_participation=data.get('objective_participation', 0),
                gold_earned=data.get('gold', 0),
                gold_per_min=data.get('gold', 0) / duration_min,
                time_cc_others=data.get('cc_time', 0),
                time_spent_dead=data.get('time_dead', deaths * 30),
                team_average_kda=data.get('team_average_kda', 2.0),
                nemesis_champion=data.get('nemesis_champion', 'Unknown')
            )
            
            analysis = self.gameplay_analyzer.analyze_game(metrics)
            self.display_analysis_results(analysis, metrics)
            
        except FileNotFoundError:
            print(f"\n{Fore.RED}Fichier non trouvé!")
            input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...")
        except json.JSONDecodeError:
            print(f"\n{Fore.RED}Erreur: Fichier JSON invalide!")
            input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...")
    
    def display_analysis_results(self, analysis: Dict, metrics: GameMetrics):
        """Affiche les résultats d'analyse"""
        self.print_header(f"📊 ANALYSE - {metrics.champion.upper()}")
        
        # Infos de partie
        print(f"{Fore.YELLOW}Partie:")
        print(f"  Champion: {Fore.WHITE}{metrics.champion}")
        print(f"  Rôle: {Fore.WHITE}{metrics.role}")
        print(f"  Durée: {Fore.WHITE}{metrics.game_duration // 60} minutes")
        print(f"  KDA: {Fore.WHITE}{metrics.kills}/{metrics.deaths}/{metrics.assists} ({metrics.kda:.2f})")
        print(f"  CS: {Fore.WHITE}{metrics.total_cs} ({metrics.cs_per_min:.1f}/min)")
        
        # Contexte équipe et objectifs
        print(f"\n{Fore.YELLOW}Contexte:")
        print(f"  Participation objectifs: {Fore.WHITE}{metrics.objective_participation:.0f}%")
        print(f"  Tours détruites: {Fore.WHITE}{metrics.turrets_destroyed}")
        print(f"  KDA moyen alliés: {Fore.WHITE}{metrics.team_average_kda:.2f}")
        
        # Comparaison avec l'équipe
        if metrics.kda < metrics.team_average_kda:
            kda_comparison = f"{Fore.RED}Inférieur à l'équipe ({metrics.team_average_kda:.2f})"
        elif metrics.kda > metrics.team_average_kda * 1.2:
            kda_comparison = f"{Fore.GREEN}Meilleur que l'équipe ({metrics.team_average_kda:.2f})"
        else:
            kda_comparison = f"{Fore.YELLOW}Similaire à l'équipe ({metrics.team_average_kda:.2f})"
        print(f"  Comparaison KDA: {kda_comparison}")
        
        # Nemesis
        if metrics.nemesis_champion and metrics.nemesis_champion != "Aucun":
            print(f"  {Fore.RED}Champion problématique: {Fore.WHITE}{metrics.nemesis_champion}")
        
        print()
        
        # Score global
        score = analysis["overall_score"]
        rank_estimate = self.gameplay_analyzer.get_rank_estimate(score)
        score_color = Fore.GREEN if score >= 75 else Fore.YELLOW if score >= 50 else Fore.RED
        
        print(f"{Fore.CYAN}{Style.BRIGHT}SCORE GLOBAL: {score_color}{score:.1f}/100")
        print(f"{Fore.CYAN}Niveau estimé: {Fore.WHITE}{rank_estimate}\n")
        
        # Scores par catégorie
        print(f"{Fore.CYAN}{Style.BRIGHT}SCORES PAR CATÉGORIE:\n")
        for category, cat_score in analysis["category_scores"].items():
            color = Fore.GREEN if cat_score >= 75 else Fore.YELLOW if cat_score >= 50 else Fore.RED
            bar_length = int(cat_score / 5)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            print(f"{Fore.WHITE}{category:<30} {color}{bar} {cat_score:.0f}/100")
        
        print()
        
        # Problèmes critiques
        if analysis["critical_issues"]:
            print(f"{Fore.RED}{Style.BRIGHT}🚨 PROBLÈMES CRITIQUES:\n")
            for issue in analysis["critical_issues"][:5]:
                print(f"{Fore.RED}  ✗ {issue}")
            print()
        
        # Points à améliorer
        if analysis["weaknesses"]:
            print(f"{Fore.YELLOW}{Style.BRIGHT}⚠️  POINTS À AMÉLIORER:\n")
            for weakness in analysis["weaknesses"][:5]:
                print(f"{Fore.YELLOW}  • {weakness}")
            print()
        
        # Points forts
        if analysis["strengths"]:
            print(f"{Fore.GREEN}{Style.BRIGHT}✅ POINTS FORTS:\n")
            for strength in analysis["strengths"][:5]:
                print(f"{Fore.GREEN}  ✓ {strength}")
            print()
        
        # Recommandations
        if analysis["recommendations"]:
            print(f"{Fore.CYAN}{Style.BRIGHT}💡 TOP RECOMMANDATIONS:\n")
            for i, rec in enumerate(analysis["recommendations"][:7], 1):
                print(f"{Fore.CYAN}  {i}. {Fore.WHITE}{rec}")
            print()
        
        self.print_separator()
        input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...")
    
    def show_example_analysis(self):
        """Affiche un exemple d'analyse"""
        from gameplay_analyzer import create_sample_game
        
        self.print_header("📈 EXEMPLE D'ANALYSE")
        
        print(f"{Fore.YELLOW}Analyse d'une partie exemple...\n")
        
        metrics, timeline = create_sample_game()
        analysis = self.gameplay_analyzer.analyze_game(metrics, timeline)
        
        self.display_analysis_results(analysis, metrics)
    
    def show_benchmarks(self):
        """Affiche les benchmarks par rôle"""
        self.print_header("📚 BENCHMARKS PAR RÔLE")
        
        print(f"{Fore.YELLOW}Ces valeurs représentent les performances moyennes attendues:\n")
        
        print(f"{Fore.CYAN}{Style.BRIGHT}{'Rôle':<12} {'CS/min':<10} {'Vision/min':<12} {'Damage/min':<12} {'KDA Target'}")
        print(f"{Fore.BLUE}{'-'*70}")
        
        for role, benchmarks in self.gameplay_analyzer.benchmarks.items():
            print(f"{Fore.GREEN}{role:<12} "
                  f"{Fore.WHITE}{benchmarks['cs_per_min']:<10.1f} "
                  f"{Fore.CYAN}{benchmarks['vision_score_per_min']:<12.1f} "
                  f"{Fore.MAGENTA}{benchmarks['damage_per_min']:<12.0f} "
                  f"{Fore.YELLOW}{benchmarks['kda_target']:.1f}")
        
        print(f"\n{Fore.LIGHTBLACK_EX}Note: Ces benchmarks sont adaptés pour les ranks Iron à Gold")
        print(f"{Fore.LIGHTBLACK_EX}Les joueurs de rank supérieur devraient viser +20-30% au-dessus")
        
        print()
        self.print_separator()
        input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...")
    
    def coming_soon_replay(self):
        """Message pour l'analyse de replay"""
        self.print_header("🔗 ANALYSE DE REPLAY")
        
        print(f"{Fore.YELLOW}Fonctionnalité en développement!\n")
        print(f"{Fore.WHITE}Cette feature permettra:")
        print(f"{Fore.CYAN}  • Analyser des replays .rofl")
        print(f"{Fore.CYAN}  • Parser automatiquement les données")
        print(f"{Fore.CYAN}  • Détecter les erreurs de positionnement")
        print(f"{Fore.CYAN}  • Analyser les trades et combats")
        print(f"{Fore.CYAN}  • Générer des conseils personnalisés")
        
        print(f"\n{Fore.LIGHTBLACK_EX}En attendant, utilisez l'analyse manuelle ou depuis JSON")
        
        print()
        self.print_separator()
        input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...")
    
    def run(self):
        """Lance l'application principale"""
        while True:
            self.display_main_menu()
            choice = input(f"{Fore.CYAN}Votre choix: {Fore.WHITE}").strip()
            
            if choice == '1':
                self.display_champions_list()
            elif choice == '2':
                self.search_champion()
            elif choice == '3':
                self.display_builds_menu()
            elif choice == '4':
                self.display_items_list()
            elif choice == '5':
                self.display_runes_list()
            elif choice == '6':
                self.display_gameplay_analysis_menu()
            elif choice == '0':
                self.print_header("👋 AU REVOIR!")
                print(f"{Fore.YELLOW}Merci d'avoir utilisé LoL Champion Manager!")
                print(f"{Fore.CYAN}À bientôt sur la faille de l'invocateur! ⚔️\n")
                break
            else:
                print(f"{Fore.RED}Choix invalide! Veuillez réessayer.")
                input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...")


def main():
    """Point d'entrée du programme"""
    try:
        app = LoLManager()
        app.run()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Programme interrompu. Au revoir! 👋\n")
    except Exception as e:
        print(f"\n{Fore.RED}Erreur inattendue: {e}")


if __name__ == "__main__":
    main()
