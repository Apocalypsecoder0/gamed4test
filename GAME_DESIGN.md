# Diablo 4: Eternal Quest - Game Design Document

## 1. Game Overview
A modular, extensible RPG system inspired by Diablo 4, Diablo 3, and Last Epoch. Features include:
- Character creation, classes, races, professions, jobs
- Inventory, loot, equipment, set items, Kanai's Cube
- Skills, passives, paragon, and DPS calculations
- Open world zones, dungeons, raids, trials, rifts
- Social, party, trial, and raid group systems
- World difficulty, seasons, eternal realm, battle pass, auction house, factions
- Nemesis system, codex, crafting, masterwork, tempering

## 2. Core Systems
- **Character System**: Level 1-100, paragon, professions, jobs, skill/passive trees
- **Inventory & Loot**: Grid-based, rarity, set items, Kanai's Cube, auction house
- **Combat**: DPS calculation, world difficulty, nemesis, party/raid mechanics
- **Progression**: XP, paragon, battle pass, season/eternal realm
- **World**: Zones, towns, cities, dungeons, raids, trials, rifts
- **Social**: Friends, clans, factions, auction house

## 3. UI/UX
- Tkinter-based GUI for all major systems
- Main menu with loading screen, credits, and system access

## 4. Update & Patch System
- Versioning and patch notes
- Patch log for debugging
- Update notification in main menu

## 5. Debugging & Logging
- Log file for errors, warnings, and info
- Patch/update notes appended to log

## 6. UML
- See `uml_diagram.png` (to be created)

## 7. Notes
- All content is fan-made and non-commercial.
- Modular code for easy extension.

## 8. Resources & Rarity

- **Resources**: Gold, Obols, Murmuring Obols, Red Dust, Veiled Crystal, Forgotten Soul, Fiend Rose, Iron Chunk, Silver Ore, Rawhide, Superior Leather, Demon Heart, Angelbreath, Scattered Prism, Baleful Fragment, Abstruse Sigil, Coiling Ward, Greater/Grand/Exquisite Blood, Grim Favor, Whispering Key, and more.

- **Resource Rarity**:
  - Common: Gold, Iron Chunk, Rawhide
  - Uncommon: Silver Ore, Superior Leather, Veiled Crystal
  - Rare: Fiend Rose, Forgotten Soul, Demon Heart, Angelbreath
  - Epic: Scattered Prism, Baleful Fragment, Abstruse Sigil, Coiling Ward
  - Legendary/Mythic: Greater Blood, Grand Blood, Exquisite Blood, Grim Favor
  - Special: Obols, Murmuring Obols, Red Dust, Whispering Key

- Resources are used for crafting, upgrading, gambling, and special events. Rarity affects drop rate and usage in high-end recipes.

## 9. Banking, Vendors, and Tree of Whispers

- **Bank System**: Players can store excess items, gold, and resources in a personal bank accessible from major cities. The bank has limited slots, with upgrades available for gold or special resources.
- **Vendors/NPCs**: Towns and cities feature various vendors:
  - Blacksmith: Repairs and upgrades weapons/armor.
  - Jeweler: Socketing and upgrading gems.
  - Alchemist: Sells potions, crafting mats, and upgrades flasks.
  - Purveyor of Curiosities: Gambles for random items using Obols.
  - General Goods: Sells basic supplies.
  - Quest Givers: Provide main/side quests and bounties.
  - Bank NPC: Manages player bank access and upgrades.
- **Tree of Whispers**: Endgame system where players complete world objectives (Whispers) to earn Grim Favors. Turning in Grim Favors at the Tree of Whispers grants powerful rewards, crafting mats, and legendary/unique items. The Tree is a central hub for endgame progression and bounties.
