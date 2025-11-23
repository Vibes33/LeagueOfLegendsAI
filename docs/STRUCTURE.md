# Project Structure

```
League Of Legends/
│
├── 📄 README.md                    # Quick start guide (root)
│
├── 🐍 Python Scripts (Core)
│   ├── lol_manager.py             # Main program (entry point)
│   ├── build_generator.py         # Build generation logic
│   ├── riot_api_client.py         # Riot API integration
│   ├── data_dragon_client.py      # Champion/Item data
│   ├── gameplay_analyzer.py       # Performance analysis
│   └── test_api_key.py            # API key validation tool
│
├── 🔧 Configuration
│   ├── requirements.txt           # Python dependencies
│   ├── .gitignore                 # Git ignore rules
│   └── riot_api_key.txt           # ⚠️ Your API key (create this)
│
├── 🛠️ Utilities
│   └── quick_menu.sh              # Interactive shell menu
│
├── 📚 Documentation (docs/)
│   ├── README.md                  # Full documentation
│   ├── CHANGELOG.md               # Version history
│   ├── GUIDE.txt                  # Visual guide with examples
│   └── riot_api_key.txt.example   # API key instructions
│
├── 📁 Runtime Folders
│   ├── .venv/                     # Python virtual environment
│   ├── cache/                     # API response cache
│   └── __pycache__/               # Python bytecode cache
│
└── 📊 Data Files (generated)
    └── (none - all data fetched from APIs)
```

## File Purposes

### Core Python Files
- **lol_manager.py**: Main UI with menu system
- **build_generator.py**: Generates optimal builds (API + fallback)
- **riot_api_client.py**: Fetches match data from Riot API
- **data_dragon_client.py**: Gets champion/item/rune data
- **gameplay_analyzer.py**: Analyzes player performance

### Configuration
- **requirements.txt**: `requests` and `colorama` packages
- **riot_api_key.txt**: Your personal Riot API key (not in git)
- **.gitignore**: Protects API key from being committed

### Documentation
All documentation is in the `docs/` folder for better organization:
- **docs/README.md**: Complete project documentation
- **docs/CHANGELOG.md**: Version 2.0 changes and history
- **docs/GUIDE.txt**: Visual ASCII guide with examples
- **docs/riot_api_key.txt.example**: How to get API key

### Tools
- **test_api_key.py**: Test if your Riot API key works
- **quick_menu.sh**: Bash menu for common tasks

## Important Files to Create

1. **riot_api_key.txt** (optional but recommended)
   - Get key from: https://developer.riotgames.com/
   - See: docs/riot_api_key.txt.example
   - Format: `RGAPI-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

## Files You Can Safely Ignore

- `__pycache__/` - Python bytecode (auto-generated)
- `cache/` - API response cache (auto-generated)
- `.venv/` - Virtual environment (already configured)
