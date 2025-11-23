#!/bin/bash
# Quick Commands for League of Legends Expert Build System

echo "🎮 League of Legends Expert Build System - Quick Commands"
echo "=========================================================="
echo ""

# Check if in correct directory
if [ ! -f "lol_manager.py" ]; then
    echo "❌ Error: Run this script from the project directory"
    exit 1
fi

# Check if venv exists
if [ ! -d ".venv" ]; then
    echo "❌ Error: Virtual environment not found"
    echo "   Create it with: python3 -m venv .venv"
    exit 1
fi

show_menu() {
    echo "Choose an action:"
    echo ""
    echo "[1] 🚀 Launch main program"
    echo "[2] 🔑 Test API key"
    echo "[3] 📝 Create API key file"
    echo "[4] 📊 Show project stats"
    echo "[5] 🧹 Clean cache"
    echo "[0] 🚪 Exit"
    echo ""
    read -p "Your choice: " choice
    
    case $choice in
        1)
            echo ""
            echo "🚀 Launching League of Legends Expert Build System..."
            source .venv/bin/activate
            python lol_manager.py
            ;;
        2)
            echo ""
            if [ ! -f "riot_api_key.txt" ]; then
                echo "❌ riot_api_key.txt not found"
                echo "   Create it first with option [3]"
            else
                echo "🔑 Testing your API key..."
                source .venv/bin/activate
                python test_api_key.py
            fi
            ;;
        3)
            echo ""
            read -p "🔑 Enter your Riot API key (RGAPI-...): " api_key
            if [ -z "$api_key" ]; then
                echo "❌ No key provided"
            else
                echo "$api_key" > riot_api_key.txt
                echo "✅ API key saved to riot_api_key.txt"
                echo ""
                echo "Testing the key..."
                source .venv/bin/activate
                python test_api_key.py
            fi
            ;;
        4)
            echo ""
            echo "📊 Project Statistics"
            echo "===================="
            echo ""
            echo "Python files:"
            find . -name "*.py" -not -path "./.venv/*" -not -path "./__pycache__/*" | wc -l | xargs echo "  "
            echo ""
            echo "Total lines of code:"
            find . -name "*.py" -not -path "./.venv/*" -not -path "./__pycache__/*" | xargs wc -l | tail -1
            echo ""
            echo "Cache size:"
            if [ -d "cache" ]; then
                du -sh cache
            else
                echo "  No cache"
            fi
            echo ""
            echo "API key status:"
            if [ -f "riot_api_key.txt" ]; then
                echo "  ✅ Present"
            else
                echo "  ❌ Not found"
            fi
            ;;
        5)
            echo ""
            if [ -d "cache" ]; then
                read -p "⚠️  Delete all cache? [y/N]: " confirm
                if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
                    rm -rf cache
                    echo "✅ Cache deleted"
                else
                    echo "❌ Cancelled"
                fi
            else
                echo "ℹ️  No cache to clean"
            fi
            ;;
        0)
            echo ""
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo ""
            echo "❌ Invalid choice"
            ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
    clear
    show_menu
}

clear
show_menu
