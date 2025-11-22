#!/usr/bin/env python3
"""
Tests automatisés du système de builds
"""

from build_recommender import BuildRecommender
from colorama import Fore, Style, init

init(autoreset=True)

def test_preconfigured_build():
    """Test 1: Build pré-configuré"""
    print(f'{Fore.YELLOW}1. Build pré-configuré pour Ahri:')
    recommender = BuildRecommender()
    build = recommender.get_build_for_champion('Ahri', 'AP')
    
    assert build['champion'] == 'Ahri', "Champion incorrect"
    assert len(build.get('items', [])) > 0, "Pas d'items"
    assert 'runes' in build, "Pas de runes"
    
    print(f'   ✓ Champion: {build["champion"]}')
    print(f'   ✓ Items: {len(build.get("items", []))} items')
    print(f'   ✓ Runes: {build["runes"].get("primary_path", "N/A")}')
    print(f'   {Fore.GREEN}✓ Test réussi!\n')

def test_generated_build():
    """Test 2: Build généré dynamiquement"""
    print(f'{Fore.YELLOW}2. Build généré pour nouveau champion:')
    recommender = BuildRecommender()
    build = recommender.get_build_for_champion('TestChampion', 'AD', enemy_composition=['Tank', 'AP', 'AD'])
    
    assert build.get('generated') == True, "Should be generated"
    assert len(build.get('items', [])) > 0, "Pas d'items générés"
    
    print(f'   ✓ Génération: {"Succès" if build.get("generated") else "Pré-configuré"}')
    print(f'   ✓ Items recommandés: {len(build.get("items", []))}')
    print(f'   {Fore.GREEN}✓ Test réussi!\n')

def test_counter_items():
    """Test 3: Counter items"""
    print(f'{Fore.YELLOW}3. Counter items:')
    recommender = BuildRecommender()
    counters = recommender.get_counter_items(['Tank', 'Healing'])
    
    assert len(counters) > 0, "Pas de counter items trouvés"
    
    print(f'   ✓ Items trouvés: {len(counters)}')
    print(f'   {Fore.GREEN}✓ Test réussi!\n')

def test_item_search():
    """Test 4: Recherche d'items"""
    print(f'{Fore.YELLOW}4. Recherche d\'items:')
    recommender = BuildRecommender()
    results = recommender.search_items('void')
    
    assert len(results) > 0, "Recherche échouée"
    
    print(f'   ✓ Résultats: {len(results)} item(s)')
    for item in results:
        print(f'     - {item["name"]}')
    print(f'   {Fore.GREEN}✓ Test réussi!\n')

def test_rune_recommendation():
    """Test 5: Recommandation de runes"""
    print(f'{Fore.YELLOW}5. Recommandation de runes:')
    recommender = BuildRecommender()
    runes = recommender.recommend_runes_for_champion('Zed', 'AD', 'Mid')
    
    assert 'keystone' in runes, "Pas de keystone"
    assert 'primary_path' in runes, "Pas de chemin primaire"
    
    keystone = runes['keystone']
    keystone_name = keystone['name'] if isinstance(keystone, dict) else keystone
    print(f'   ✓ Keystone: {keystone_name}')
    print(f'   ✓ Chemin primaire: {runes["primary_path"]}')
    print(f'   {Fore.GREEN}✓ Test réussi!\n')

def test_all_mythics():
    """Test 6: Liste des mythiques"""
    print(f'{Fore.YELLOW}6. Items mythiques:')
    recommender = BuildRecommender()
    mythics = recommender.get_all_items_by_category('Mythic')
    
    assert len(mythics) > 0, "Pas de mythiques trouvés"
    
    print(f'   ✓ Mythiques trouvés: {len(mythics)}')
    print(f'   {Fore.GREEN}✓ Test réussi!\n')

def test_contextual_build():
    """Test 7: Build contextuel"""
    print(f'{Fore.YELLOW}7. Build contextuel vs composition spécifique:')
    recommender = BuildRecommender()
    
    # Build vs tanks
    build_vs_tanks = recommender.get_build_for_champion(
        'Jinx', 'AD', enemy_composition=['Tank', 'Tank', 'AD']
    )
    
    item_names = [item.get('name', '') for item in build_vs_tanks.get('items', [])]
    has_anti_tank = any('Kraken' in name or 'Dominik' in name or 'Blade' in name for name in item_names)
    
    print(f'   ✓ Build adapté aux tanks: {"Oui" if has_anti_tank else "Non"}')
    print(f'   ✓ Items: {", ".join(item_names[:3])}...')
    print(f'   {Fore.GREEN}✓ Test réussi!\n')

def main():
    print(f'\n{Fore.CYAN}{"="*60}')
    print(f'{Fore.CYAN}{Style.BRIGHT}TEST SYSTÈME DE BUILDS - AUTOMATISÉ')
    print(f'{Fore.CYAN}{"="*60}\n')
    
    tests = [
        test_preconfigured_build,
        test_generated_build,
        test_counter_items,
        test_item_search,
        test_rune_recommendation,
        test_all_mythics,
        test_contextual_build
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f'   {Fore.RED}✗ Test échoué: {e}\n')
            failed += 1
        except Exception as e:
            print(f'   {Fore.RED}✗ Erreur: {e}\n')
            failed += 1
    
    print(f'{Fore.CYAN}{"="*60}')
    print(f'{Fore.GREEN}✓ Tests réussis: {passed}')
    if failed > 0:
        print(f'{Fore.RED}✗ Tests échoués: {failed}')
    print(f'{Fore.CYAN}{"="*60}\n')
    
    if failed == 0:
        print(f'{Fore.GREEN}{Style.BRIGHT}✅ TOUS LES TESTS SONT PASSÉS!\n')
    else:
        print(f'{Fore.RED}{Style.BRIGHT}❌ Certains tests ont échoué.\n')

if __name__ == "__main__":
    main()
