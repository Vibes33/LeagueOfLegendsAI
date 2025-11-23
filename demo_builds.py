#!/usr/bin/env python3
"""
Demo script to show the new build format with boots separated
"""

from build_generator import BuildGenerator
from colorama import init, Fore, Style

init(autoreset=True)

def demo_build_display():
    print("=" * 80)
    print("🎮 BUILD GENERATOR - New Format Demo")
    print("=" * 80)
    print()
    
    bg = BuildGenerator()
    
    # Test 1: Expert system build
    print(f"{Fore.CYAN}TEST 1: Expert System Build (Ahri Mid)")
    print("-" * 80)
    build = bg.generate_build('Ahri', 'mid', use_api=False)
    
    if build:
        print(f"{Fore.GREEN}✓ Generated successfully")
        print(f"  Source: {build['source']}")
        print(f"  Core items: {len(build.get('core_items', []))}")
        print(f"  Boots: {build.get('boots', 'None')}")
        print(f"  Runes: {build.get('runes', {}).get('keystone')} ({build.get('runes', {}).get('primary_path')} + {build.get('runes', {}).get('secondary_path')})")
    print()
    
    # Test 2: API build (if API key exists)
    import os
    if os.path.exists('riot_api_key.txt'):
        print(f"{Fore.CYAN}TEST 2: API Build (Yasuo Mid - LIMITED TO 10 GAMES)")
        print("-" * 80)
        print(f"{Fore.YELLOW}Note: This will take 1-2 minutes due to rate limits...")
        print()
        
        build_api = bg.generate_build('Yasuo', 'MIDDLE', use_api=True)
        
        if build_api and build_api.get('source') == 'riot_api':
            print()
            print(f"{Fore.GREEN}✓ API analysis successful!")
            stats = build_api.get('stats', {})
            print(f"  Games analyzed: {stats.get('matches', 0)}")
            print(f"  Winrate: {stats.get('winrate', 0):.1f}%")
            print(f"  Core items: {len(build_api.get('core_items', []))}")
            
            boots = build_api.get('boots')
            if boots:
                print(f"  Boots: {boots.get('name', 'Unknown')}")
            
            runes = build_api.get('runes', {})
            print(f"  Runes: {runes.get('keystone')} ({runes.get('primary_path')} + {runes.get('secondary_path')})")
        else:
            print(f"{Fore.YELLOW}⚠️  API analysis failed, used fallback")
    else:
        print(f"{Fore.YELLOW}TEST 2: Skipped (no API key)")
        print(f"  Create riot_api_key.txt to test API builds")
    
    print()
    print("=" * 80)
    print("✅ Demo complete!")
    print()
    print("The new format includes:")
    print("  • Separate boots display (👟 BOOTS)")
    print("  • 6 core items (excluding boots)")
    print("  • Full rune paths (Primary + Secondary)")
    print("  • Real winrate when using API")
    print("=" * 80)

if __name__ == "__main__":
    demo_build_display()
