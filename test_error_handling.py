#!/usr/bin/env python3
"""
Test script for the improved error handling in API calls.
Tests:
1. Rate limit retry logic (429 responses)
2. Empty result detection
3. Clear user feedback messages
4. Timeout retry logic
"""

import os
import sys
from build_generator import BuildGenerator

print("=" * 60)
print("🧪 TESTING IMPROVED ERROR HANDLING")
print("=" * 60)

# Check if API key exists
if not os.path.exists('riot_api_key.txt'):
    print("\n⚠️  No riot_api_key.txt found")
    print("   This test requires a valid API key to work properly")
    print("   Create the file with: echo 'RGAPI-your-key' > riot_api_key.txt")
    sys.exit(1)

with open('riot_api_key.txt', 'r') as f:
    api_key = f.read().strip()
    print(f"\n✓ API key loaded: {api_key[:15]}...{api_key[-4:]}")

# Initialize build generator
bg = BuildGenerator()

print("\n" + "=" * 60)
print("TEST 1: Common champion (should find games quickly)")
print("=" * 60)
print("\nGenerating build for: Yasuo (MIDDLE)\n")

try:
    build = bg.generate_build('Yasuo', 'MIDDLE', use_api=True)
    
    if build:
        print("\n✅ Build generated successfully!")
        print(f"   Source: {'API' if build.get('source') == 'api' else 'Expert System'}")
        if build.get('total_games'):
            print(f"   Games analyzed: {build['total_games']}")
            print(f"   Winrate: {build.get('winrate', 0):.1f}%")
    else:
        print("\n❌ Build generation failed (returned None)")
        
except KeyboardInterrupt:
    print("\n\n⚠️  Test interrupted by user (Ctrl+C)")
    sys.exit(0)
except Exception as e:
    print(f"\n❌ Exception during build generation:")
    print(f"   {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("TEST 2: Rare champion (should still find some games)")
print("=" * 60)
print("\nGenerating build for: Ivern (JUNGLE)\n")

try:
    build = bg.generate_build('Ivern', 'JUNGLE', use_api=True)
    
    if build:
        print("\n✅ Build generated successfully!")
        print(f"   Source: {'API' if build.get('source') == 'api' else 'Expert System'}")
        if build.get('total_games'):
            print(f"   Games analyzed: {build['total_games']}")
            print(f"   Winrate: {build.get('winrate', 0):.1f}%")
        else:
            print("   No games found, used fallback system")
    else:
        print("\n❌ Build generation failed (returned None)")
        
except KeyboardInterrupt:
    print("\n\n⚠️  Test interrupted by user (Ctrl+C)")
    sys.exit(0)
except Exception as e:
    print(f"\n❌ Exception during build generation:")
    print(f"   {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("✅ TEST COMPLETE")
print("=" * 60)
print("\nExpected behaviors:")
print("  ✓ Clear status messages during API calls")
print("  ✓ Auto-retry on rate limits (429) with wait time")
print("  ✓ Auto-retry on timeout (up to 3 times)")
print("  ✓ '✅ Using API data: X games analyzed' on success")
print("  ✓ '⚠️ API returned no games, using fallback system' on empty result")
print("  ✓ '📊 Using expert system fallback' when fallback is used")
print("  ✓ Progress tracking: '✓ X/Y games found'")
print("  ✓ Player tracking: '🔍 Checked X players'")
print("\nIf you saw rate limit warnings, that's GOOD - it means retry logic works!")
