# Arcane Engine RPG System

A modular, extensible Python RPG system inspired by Diablo 4, Diablo 3, and Last Epoch, featuring a Tkinter GUI main menu and advanced RPG subsystems.

## Features

- **Tkinter GUI Main Menu**: Modern, user-friendly interface with campaign, world map, and system access.
- **Subsystems**: Character, Inventory, Skills, Quests, Map, Social, Settings, Patch/Update, Debug Logging, and more.
- **Advanced RPG Mechanics**:
  - Open world, dungeons, raids, trials, rifts
  - Professions, jobs, crafting, masterwork, tempering
  - Set items, Kanai's Cube, world difficulty, seasons/eternal realms
  - Battle pass, auction house, factions, party/raid, codex
  - Skill/passive trees, paragon, DPS calculations
- **Centralized Asset Database**: Items, monsters, stats, world geography (continents, countries, kingdoms, zones), resources, settings, input mappings.
- **Loot & Crafting**: Medieval weapons, affixes, stat/substat rolls, class/type restrictions, rarity weights/colors, advanced loot/crafting/affix/stat logic.
- **World Map**: Grid-based, interactive, with towns, cities, zones, and world seed display. Click to view info, right-click to travel.
- **Game Stats & Random Seed**: Initialization/reset and reproducible gameplay.
- **Robust Error Handling**: User-friendly error dialogs and debug logging.
- **Engine Branding**: All UI/info displays use "Arcane Engine" branding.

## Getting Started

1. Ensure Python 3.8+ is installed.
2. Run `main_menu.py` to launch the main menu and start a new game.
3. Explore the campaign, world map, inventory, skills, quests, and more from the GUI.

## File Structure

- `main_menu.py`: Main menu, campaign, world map, gameplay logic, loot/crafting/affix/stat logic, engine branding.
- `character_system.py`: Character, equipment, loot, nemesis, party/raid/trial, codex, professions, jobs, crafting, world difficulty, etc.
- `skills_system.py`: Skills system, GUI, skill/passive trees.
- `quests_system.py`, `map_system.py`, `social_system.py`, `settings_system.py`, `patch_system.py`: Subsystems.
- `game_assets.py`: Centralized asset database.
- `PATCH_NOTES.md`, `GAME_DESIGN.md`, `README.md`, `uml_diagram.puml`, `debug.log`: Documentation and logs.

## World Map Interactivity

- **Left-click** any location to view info.
- **Right-click** towns/cities/kingdoms to travel and update your current zone.
- Map legend and lists of continents, countries, kingdoms, towns, and zones are displayed below the map.

## Extensibility

- Easily add new items, monsters, skills, passives, world regions, and features by editing the asset database and subsystem files.
- Designed for rapid prototyping and expansion of RPG mechanics.

## Credits

- Lead Developer: Shadow
- Inspired by Diablo, Last Epoch, and the ARPG community.
- Engine: Arcane Engine v1.0

---

All content is fan-made and non-commercial. For educational and prototyping use only.
