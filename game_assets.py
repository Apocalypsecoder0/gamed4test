"""
game_assets.py
Centralized database/module for game assets: items, monsters, stats, etc.
This module is designed for easy extension and integration with all RPG systems.
"""

from typing import Dict, List, Any

# Example item database
ITEMS: Dict[str, Dict[str, Any]] = {
    "sword_iron": {
        "name": "Iron Sword",
        "type": "weapon",
        "rarity": "common",
        "damage": 10,
        "stats": {"strength": 2},
        "level_req": 1,
        "description": "A basic iron sword."
    },
    "potion_healing": {
        "name": "Healing Potion",
        "type": "consumable",
        "rarity": "common",
        "heal": 50,
        "description": "Restores 50 HP."
    },
    # Diablo 4 Items, Equipment, Weapons, Armor, and Other Items
    "ancestral_sword": {
        "name": "Ancestral Sword",
        "type": "weapon",
        "rarity": "legendary",
        "damage": 120,
        "stats": {"strength": 10, "dexterity": 5},
        "level_req": 30,
        "description": "A sword passed down through generations, humming with power."
    },
    "unique_staff_of_lilith": {
        "name": "Staff of Lilith",
        "type": "weapon",
        "rarity": "unique",
        "damage": 150,
        "stats": {"intelligence": 20, "willpower": 10},
        "level_req": 50,
        "description": "A staff imbued with the essence of Lilith."
    },
    "druidic_totem": {
        "name": "Druidic Totem",
        "type": "weapon",
        "rarity": "rare",
        "damage": 80,
        "stats": {"willpower": 8, "spirit": 5},
        "level_req": 20,
        "description": "A totem used by druids to channel nature's wrath."
    },
    "hellforged_plate": {
        "name": "Hellforged Plate",
        "type": "armor",
        "rarity": "legendary",
        "armor": 200,
        "stats": {"strength": 12, "vitality": 8},
        "level_req": 40,
        "description": "Armor forged in the fires of Hell."
    },
    "shadow_cloak": {
        "name": "Shadow Cloak",
        "type": "armor",
        "rarity": "epic",
        "armor": 90,
        "stats": {"dexterity": 10, "evasion": 7},
        "level_req": 25,
        "description": "A cloak that blends the wearer into the shadows."
    },
    "fiend_rose": {
        "name": "Fiend Rose",
        "type": "crafting_material",
        "rarity": "rare",
        "description": "A rare flower used in high-end crafting recipes."
    },
    "scattered_prism": {
        "name": "Scattered Prism",
        "type": "crafting_material",
        "rarity": "epic",
        "description": "Used to add sockets to equipment."
    },
    "murmuring_obol": {
        "name": "Murmuring Obol",
        "type": "currency",
        "rarity": "special",
        "description": "A mysterious currency used for gambling."
    },
    "forgotten_soul": {
        "name": "Forgotten Soul",
        "type": "crafting_material",
        "rarity": "rare",
        "description": "A soul lost to time, used for legendary upgrades."
    },
    # Add more Diablo 4 items as needed...
}

# Example monster database
MONSTERS: Dict[str, Dict[str, Any]] = {
    # Undead
    "zombie": {
        "name": "Zombie",
        "type": "undead",
        "class": "shambler",
        "level": 1,
        "hp": 30,
        "damage": 5,
        "stats": {"strength": 1, "dexterity": 1},
        "loot_table": ["potion_healing"],
        "description": "A slow, shambling undead."
    },
    "skeleton_archer": {
        "name": "Skeleton Archer",
        "type": "undead",
        "class": "archer",
        "level": 2,
        "hp": 20,
        "damage": 7,
        "stats": {"dexterity": 3},
        "loot_table": ["sword_iron"],
        "description": "A nimble skeleton with a bow."
    },
    "skeleton_mage": {
        "name": "Skeleton Mage",
        "type": "undead",
        "class": "mage",
        "level": 3,
        "hp": 18,
        "damage": 10,
        "stats": {"intelligence": 4},
        "loot_table": ["potion_healing"],
        "description": "A skeleton that casts dark magic."
    },
    # Demons
    "fallen": {
        "name": "Fallen",
        "type": "demon",
        "class": "minion",
        "level": 2,
        "hp": 22,
        "damage": 6,
        "stats": {"dexterity": 2},
        "loot_table": ["potion_healing"],
        "description": "A mischievous demon imp."
    },
    "succubus": {
        "name": "Succubus",
        "type": "demon",
        "class": "caster",
        "level": 8,
        "hp": 40,
        "damage": 18,
        "stats": {"intelligence": 7},
        "loot_table": ["potion_healing"],
        "description": "A flying demoness that drains life."
    },
    "goatman": {
        "name": "Goatman",
        "type": "beastman",
        "class": "brute",
        "level": 4,
        "hp": 35,
        "damage": 12,
        "stats": {"strength": 4},
        "loot_table": ["sword_iron"],
        "description": "A savage goat-headed demon."
    },
    "blood_bishop": {
        "name": "Blood Bishop",
        "type": "demon",
        "class": "elite",
        "level": 12,
        "hp": 120,
        "damage": 30,
        "stats": {"intelligence": 12, "strength": 6},
        "loot_table": ["potion_healing", "sword_iron"],
        "description": "A powerful blood magic demon."
    },
    # Beasts/Animals
    "dire_wolf": {
        "name": "Dire Wolf",
        "type": "beast",
        "class": "animal",
        "level": 3,
        "hp": 28,
        "damage": 8,
        "stats": {"dexterity": 3},
        "loot_table": ["potion_healing"],
        "description": "A large, aggressive wolf."
    },
    "corrupted_bear": {
        "name": "Corrupted Bear",
        "type": "beast",
        "class": "animal",
        "level": 7,
        "hp": 70,
        "damage": 20,
        "stats": {"strength": 8},
        "loot_table": ["potion_healing"],
        "description": "A bear twisted by dark magic."
    },
    "plague_rat": {
        "name": "Plague Rat",
        "type": "beast",
        "class": "vermin",
        "level": 1,
        "hp": 8,
        "damage": 2,
        "stats": {"dexterity": 1},
        "loot_table": [],
        "description": "A disease-ridden rat."
    },
    # Constructs
    "animated_armor": {
        "name": "Animated Armor",
        "type": "construct",
        "class": "guardian",
        "level": 10,
        "hp": 90,
        "damage": 22,
        "stats": {"strength": 10},
        "loot_table": ["sword_iron"],
        "description": "A suit of armor brought to life by magic."
    },
    # Humans/Cultists
    "cultist_pyromancer": {
        "name": "Cultist Pyromancer",
        "type": "human",
        "class": "caster",
        "level": 6,
        "hp": 32,
        "damage": 15,
        "stats": {"intelligence": 6},
        "loot_table": ["potion_healing"],
        "description": "A human cultist wielding fire magic."
    },
    # Elites/Bosses (examples)
    "butcher": {
        "name": "The Butcher",
        "type": "demon",
        "class": "boss",
        "level": 20,
        "hp": 500,
        "damage": 60,
        "stats": {"strength": 20, "dexterity": 8},
        "loot_table": ["sword_iron", "potion_healing"],
        "description": "A legendary cleaver-wielding demon."
    },
    "andariel": {
        "name": "Andariel, Maiden of Anguish",
        "type": "demon",
        "class": "boss",
        "level": 30,
        "hp": 1200,
        "damage": 90,
        "stats": {"intelligence": 25, "dexterity": 15},
        "loot_table": ["potion_healing", "sword_iron"],
        "description": "A Prime Evil, mistress of poison and pain."
    },
    # ... add more monsters, demons, creatures, and animals as needed ...
}

# Example stat definitions
STATS: Dict[str, Dict[str, Any]] = {
    "strength": {
        "name": "Strength",
        "description": "Increases melee damage and carrying capacity."
    },
    "dexterity": {
        "name": "Dexterity",
        "description": "Increases ranged damage and dodge chance."
    },
    "intelligence": {
        "name": "Intelligence",
        "description": "Increases spell power and mana pool."
    },
    # ... more stats ...
}

# Example world geography definitions
CONTINENTS: Dict[str, Dict[str, Any]] = {
    "sanctuary": {
        "name": "Sanctuary",
        "description": "The world in which Diablo takes place, containing all continents and regions.",
    },
    # Add more continents if needed
}

COUNTRIES: Dict[str, Dict[str, Any]] = {
    "scosglen": {
        "name": "Scosglen",
        "continent": "sanctuary",
        "description": "A wild, forested land of druids and ancient spirits."
    },
    "kehristan": {
        "name": "Kehjistan",
        "continent": "sanctuary",
        "description": "A vast desert empire, home to ancient ruins and powerful mages."
    },
    "hawezar": {
        "name": "Hawezar",
        "continent": "sanctuary",
        "description": "A swampy, disease-ridden region filled with danger."
    },
    "fractured_peaks": {
        "name": "Fractured Peaks",
        "continent": "sanctuary",
        "description": "A cold, mountainous region with ancient monasteries."
    },
    "dry_steppes": {
        "name": "Dry Steppes",
        "continent": "sanctuary",
        "description": "A harsh, arid land of survival and conflict."
    },
    # ... add more countries ...
}

KINGDOMS: Dict[str, Dict[str, Any]] = {
    "westmarch": {
        "name": "Westmarch",
        "country": "kehristan",
        "description": "A powerful and wealthy kingdom, once a beacon of civilization."
    },
    "corvus": {
        "name": "Corvus",
        "country": "kehristan",
        "description": "An ancient, ruined kingdom buried beneath the sands."
    },
    "tur_dulra": {
        "name": "Tur Dulra",
        "country": "scosglen",
        "description": "A legendary druidic stronghold."
    },
    # ... add more kingdoms ...
}

ZONES: Dict[str, Dict[str, Any]] = {
    "zarbinzet": {
        "name": "Zarbinzet",
        "kingdom": "hawezar",
        "description": "A major city and hub in the swamps of Hawezar."
    },
    "kyovashad": {
        "name": "Kyovashad",
        "kingdom": "fractured_peaks",
        "description": "A fortified city in the Fractured Peaks, refuge for many."
    },
    "menestad": {
        "name": "Menestad",
        "kingdom": "fractured_peaks",
        "description": "A snowy outpost on the edge of civilization."
    },
    "tarsarak": {
        "name": "Tarsarak",
        "kingdom": "dry_steppes",
        "description": "A trade city in the Dry Steppes."
    },
    # ... add more zones ...
}

# Game settings and options (inspired by Diablo 4)
GAME_SETTINGS: Dict[str, Dict[str, Any]] = {
    "graphics": {
        "resolution": ["1920x1080", "2560x1440", "3840x2160"],
        "fullscreen": True,
        "vsync": True,
        "quality": ["Low", "Medium", "High", "Ultra"],
    },
    "audio": {
        "master_volume": 100,
        "music_volume": 80,
        "effects_volume": 90,
        "voice_volume": 85,
        "mute_all": False,
    },
    "gameplay": {
        "difficulty": ["Adventurer", "Veteran", "Nightmare", "Torment"],
        "auto_pickup": True,
        "show_damage_numbers": True,
        "show_health_bars": True,
        "camera_shake": True,
    },
    "interface": {
        "language": ["English", "German", "French", "Spanish", "Italian", "Polish", "Russian", "Korean", "Japanese", "Chinese"],
        "hud_scale": 1.0,
        "show_minimap": True,
        "show_quest_tracker": True,
        "colorblind_mode": False,
    },
    # ... add more categories as needed ...
}

# Input bindings for keyboard, mouse, and controller
KEYBOARD_BINDINGS: Dict[str, str] = {
    "move_up": "W",
    "move_down": "S",
    "move_left": "A",
    "move_right": "D",
    "attack": "Left Mouse Button",
    "interact": "E",
    "open_inventory": "I",
    "open_map": "M",
    "open_skills": "K",
    "use_potion": "Q",
    "mount": "Z",
    # ... add more bindings ...
}

MOUSE_SETTINGS: Dict[str, Any] = {
    "sensitivity": 1.0,
    "invert_y_axis": False,
    "mouse_acceleration": False,
}

CONTROLLER_BINDINGS: Dict[str, str] = {
    "move": "Left Stick",
    "attack": "Right Trigger",
    "interact": "A Button",
    "open_inventory": "D-Pad Up",
    "open_map": "View Button",
    "open_skills": "Y Button",
    "use_potion": "LB",
    "mount": "RB",
    # ... add more bindings ...
}

# Fetch functions for new world assets
def get_continent(continent_id: str) -> Dict[str, Any]:
    return CONTINENTS.get(continent_id, {})

def get_country(country_id: str) -> Dict[str, Any]:
    return COUNTRIES.get(country_id, {})

def get_kingdom(kingdom_id: str) -> Dict[str, Any]:
    return KINGDOMS.get(kingdom_id, {})

def get_zone(zone_id: str) -> Dict[str, Any]:
    return ZONES.get(zone_id, {})

# Example function to fetch an item by ID
def get_item(item_id: str) -> Dict[str, Any]:
    return ITEMS.get(item_id, {})

# Example function to fetch a monster by ID
def get_monster(monster_id: str) -> Dict[str, Any]:
    return MONSTERS.get(monster_id, {})

# Example function to fetch stat info by ID
def get_stat(stat_id: str) -> Dict[str, Any]:
    return STATS.get(stat_id, {})

# Extend with more asset types as needed: skills, affixes, sets, crafting mats, etc.

# Fetch functions for settings and controls
def get_game_setting(category: str) -> Dict[str, Any]:
    return GAME_SETTINGS.get(category, {})

def get_keyboard_binding(action: str) -> str:
    return KEYBOARD_BINDINGS.get(action, "")

def get_mouse_setting(setting: str) -> Any:
    return MOUSE_SETTINGS.get(setting, None)

def get_controller_binding(action: str) -> str:
    return CONTROLLER_BINDINGS.get(action, "")
