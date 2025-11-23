#!/usr/bin/env python3
"""
Quick script to test if your Riot API key is valid.
Usage: python test_api_key.py
"""

import os
import sys


def test_api_key():
    print("=" * 80)
    print("🔑 RIOT API KEY TESTER")
    print("=" * 80)
    
    # Check if file exists
    if not os.path.exists('riot_api_key.txt'):
        print("\n❌ ERROR: riot_api_key.txt not found")
        print("\n📝 To create it:")
        print("   1. Get your key from https://developer.riotgames.com/")
        print("   2. See docs/riot_api_key.txt.example for instructions")
        print("   3. Create file: echo 'RGAPI-your-key-here' > riot_api_key.txt")
        print("   4. Run this script again")
        return False
    
    # Read key
    with open('riot_api_key.txt', 'r') as f:
        api_key = f.read().strip()
    
    if not api_key:
        print("\n❌ ERROR: riot_api_key.txt is empty")
        return False
    
    if not api_key.startswith('RGAPI-'):
        print("\n⚠️  WARNING: Key doesn't start with 'RGAPI-'")
        print(f"   Your key starts with: {api_key[:10]}...")
        print("   This might not be a valid Riot API key")
    
    print(f"\n✓ Found API key: {api_key[:15]}...{api_key[-4:]}")
    print("\n🔍 Testing connection to Riot API...")
    
    try:
        from riot_api_client import RiotAPIClient
        
        client = RiotAPIClient(api_key=api_key, region='euw1')
        
        print("   Fetching Challenger players...")
        players = client.get_challenger_players()
        
        if players:
            print(f"\n✅ SUCCESS! API key is valid")
            print(f"   Retrieved {len(players)} Challenger players")
            print(f"\n   Example players:")
            for i, player in enumerate(players[:3], 1):
                name = player.get('summonerName') or player.get('name', 'Unknown')
                lp = player.get('leaguePoints', 0)
                print(f"   {i}. {name} ({lp} LP)")
            
            return True
        else:
            print("\n❌ ERROR: No data returned (but no error)")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        
        error_str = str(e)
        
        if '401' in error_str or 'Forbidden' in error_str:
            print("\n🔑 Your API key is invalid or expired")
            print("   Development keys expire after 24 hours")
            print("   Generate a new one at: https://developer.riotgames.com/")
        elif '403' in error_str:
            print("\n🚫 Access forbidden - check your key permissions")
        elif '429' in error_str:
            print("\n⏱️  Rate limit exceeded - wait a moment and try again")
        elif 'ConnectionError' in error_str:
            print("\n🌐 Connection error - check your internet connection")
        
        return False


if __name__ == "__main__":
    print("\n")
    success = test_api_key()
    print("\n" + "=" * 80)
    
    if success:
        print("✅ Your API key is working! You can now use the build generator.")
        print("\nRun: python lol_manager.py")
        print("Then select [4] Generate Build and choose 'Y' for API analysis")
    else:
        print("❌ API key test failed. Fix the issues above and try again.")
    
    print("=" * 80 + "\n")
    sys.exit(0 if success else 1)
