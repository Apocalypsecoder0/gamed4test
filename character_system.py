import tkinter as tk
from tkinter import messagebox
from typing import List, Dict, Optional, TYPE_CHECKING
import importlib.util
import sys
import random

# Dynamically import Item for runtime and type hints
item_mod_name = 'from typing import List, Dict, Optional'
item_mod_path = 'from typing import List, Dict, Optional.py'
spec = importlib.util.spec_from_file_location(item_mod_name, item_mod_path)
if spec and spec.loader:
    item_mod = importlib.util.module_from_spec(spec)
    sys.modules[item_mod_name] = item_mod
    spec.loader.exec_module(item_mod)
    Item = item_mod.Item
else:
    class Item:
        pass

# Character class for the system
class Character:
    D4_CLASSES = [
        "Barbarian", "Sorceress", "Druid", "Rogue", "Necromancer"
    ]
    D4_RACES = [
        "Human"
    ]
    WOW_CLASSES = [
        "Warrior", "Paladin", "Hunter", "Rogue", "Priest", "Death Knight", "Shaman", "Mage", "Warlock", "Monk", "Druid", "Demon Hunter", "Evoker"
    ]
    WOW_RACES = [
        "Human", "Orc", "Dwarf", "Night Elf", "Undead", "Tauren", "Gnome", "Troll", "Goblin", "Blood Elf", "Draenei", "Worgen", "Pandaren", "Nightborne", "Highmountain Tauren", "Void Elf", "Lightforged Draenei", "Zandalari Troll", "Kul Tiran", "Dark Iron Dwarf", "Mag'har Orc", "Vulpera", "Mechagnome", "Dracthyr"
    ]

    def __init__(self, name: str, char_class: str, level: int = 1, stats: Optional[Dict[str, int]] = None, race: Optional[str] = None, hardcore: bool = False):
        self.name = name
        self.char_class = char_class
        self.level = level
        self.race = race
        self.hardcore = hardcore  # Add hardcore mode flag
        self.stats = stats if stats else {"Strength": 10, "Dexterity": 10, "Intelligence": 10, "Vitality": 10}
        self.equipment = Equipment()

    def __repr__(self):
        mode = "Hardcore" if getattr(self, 'hardcore', False) else "Normal"
        return f"{self.name} (Class: {self.char_class}, Race: {self.race or 'Unknown'}, Level: {self.level}, Mode: {mode}, Stats: {self.stats})"

    def equip_item(self, item: 'Item') -> bool:
        return self.equipment.equip(item)

    def unequip_item(self, item_type: str):
        self.equipment.unequip(item_type)

    def get_equipped(self):
        return self.equipment.get_equipped()

class Equipment:
    def __init__(self):
        self.weapon = None
        self.armor = None

    def equip(self, item):
        if hasattr(item, 'item_type') and item.item_type == 'Weapon':
            self.weapon = item
            return True
        elif hasattr(item, 'item_type') and item.item_type == 'Armor':
            self.armor = item
            return True
        return False

    def unequip(self, item_type):
        if item_type == 'Weapon':
            self.weapon = None
        elif item_type == 'Armor':
            self.armor = None

    def get_equipped(self):
        return {'Weapon': self.weapon, 'Armor': self.armor}

class LootSystem:
    RARITIES = ['Common', 'Rare', 'Legendary', 'Mythic']
    GEAR_CLASSES = Character.D4_CLASSES + Character.WOW_CLASSES

    @staticmethod
    def generate_loot(char_class):
        import random
        item_mod = sys.modules.get('from typing import List, Dict, Optional')
        if not item_mod:
            import importlib.util
            spec = importlib.util.spec_from_file_location('from typing import List, Dict, Optional', 'from typing import List, Dict, Optional.py')
            if spec and spec.loader:
                item_mod = importlib.util.module_from_spec(spec)
                sys.modules['from typing import List, Dict, Optional'] = item_mod
                spec.loader.exec_module(item_mod)
        Item = getattr(item_mod, 'Item', None)
        item_type = random.choice(['Weapon', 'Armor'])
        rarity = random.choice(LootSystem.RARITIES)
        name = f"{rarity} {item_type} of {char_class}"
        stats = {"Power": random.randint(10, 100)}
        if Item:
            return Item(name, item_type, rarity, stats)
        else:
            return None

class CharacterSystem:
    def __init__(self):
        self.characters: List[Character] = []

    def add_character(self, character: Character):
        self.characters.append(character)

    def remove_character(self, character: Character):
        if character in self.characters:
            self.characters.remove(character)

    def get_character(self, name: str) -> Optional[Character]:
        for char in self.characters:
            if char.name == name:
                return char
        return None

    def list_characters(self) -> List[Character]:
        return self.characters

class CharacterSystemGUI:
    def __init__(self, char_system: CharacterSystem):
        self.char_system = char_system
        self.root = tk.Tk()
        self.root.title("Character System Menu")
        self.listbox = tk.Listbox(self.root, width=50)
        self.listbox.pack(padx=10, pady=10)
        self.add_button = tk.Button(self.root, text="Add Character", command=self.add_character_window)
        self.add_button.pack(pady=5)
        self.remove_button = tk.Button(self.root, text="Remove Selected", command=self.remove_selected)
        self.remove_button.pack(pady=5)
        self.refresh_button = tk.Button(self.root, text="Refresh", command=self.refresh_list)
        self.refresh_button.pack(pady=5)
        self.refresh_list()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for char in self.char_system.list_characters():
            eq = char.get_equipped()
            eq_str = f" | Weapon: {eq['Weapon']} | Armor: {eq['Armor']}"
            self.listbox.insert(tk.END, str(char) + eq_str)
        self.listbox.bind('<Double-1>', self.on_double_click)

    def add_character_window(self):
        win = tk.Toplevel(self.root)
        win.title("Add Character")
        tk.Label(win, text="Name:").grid(row=0, column=0)
        name_entry = tk.Entry(win)
        name_entry.grid(row=0, column=1)
        tk.Label(win, text="Class:").grid(row=1, column=0)
        class_entry = tk.Entry(win)
        class_entry.grid(row=1, column=1)
        tk.Label(win, text="Level:").grid(row=2, column=0)
        level_entry = tk.Entry(win)
        level_entry.grid(row=2, column=1)
        tk.Label(win, text="Race:").grid(row=3, column=0)
        race_entry = tk.Entry(win)
        race_entry.grid(row=3, column=1)
        # Hardcore mode checkbox
        hardcore_var = tk.BooleanVar(win)
        tk.Checkbutton(win, text="Hardcore Mode (Permanent Death)", variable=hardcore_var).grid(row=4, column=0, columnspan=2)
        def submit():
            name = name_entry.get()
            char_class = class_entry.get()
            race = race_entry.get()
            try:
                level = int(level_entry.get())
            except ValueError:
                level = 1
            hardcore = hardcore_var.get()
            if name and char_class:
                char = Character(name, char_class, level, race=race, hardcore=hardcore)
                self.char_system.add_character(char)
                self.refresh_list()
                win.destroy()
            else:
                messagebox.showerror("Error", "Name and Class required.")
        tk.Button(win, text="Add", command=submit).grid(row=5, column=0, columnspan=2)

    def show_equip_window(self, char):
        win = tk.Toplevel(self.root)
        win.title(f"Equip {char.name}")
        tk.Label(win, text="Weapon:").grid(row=0, column=0)
        tk.Label(win, text=str(char.equipment.weapon) if char.equipment.weapon else "None").grid(row=0, column=1)
        tk.Label(win, text="Armor:").grid(row=1, column=0)
        tk.Label(win, text=str(char.equipment.armor) if char.equipment.armor else "None").grid(row=1, column=1)
        def loot():
            item = LootSystem.generate_loot(char.char_class)
            if char.equip_item(item):
                messagebox.showinfo("Loot", f"Equipped: {item}")
            else:
                messagebox.showinfo("Loot", f"Looted: {item} (Not equipped)")
            self.refresh_list()
            win.destroy()
        tk.Button(win, text="Loot & Equip Random", command=loot).grid(row=2, column=0, columnspan=2)

    def remove_selected(self):
        selection = self.listbox.curselection()
        if selection:
            idx = selection[0]
            char = self.char_system.list_characters()[idx]
            self.char_system.remove_character(char)
            self.refresh_list()
        else:
            messagebox.showinfo("Info", "No character selected.")

    def on_double_click(self, event):
        selection = self.listbox.curselection()
        if selection:
            idx = selection[0]
            char = self.char_system.list_characters()[idx]
            self.show_equip_window(char)

    def run(self):
        self.root.mainloop()

# Monster, NPC, Dungeon, Raid, and Trial definitions
class Monster:
    TYPES = [
        "Beast", "Undead", "Demon", "Construct", "Dragon", "Elemental", "Human", "Aberration"
    ]
    CLASSES = [
        "Minion", "Elite", "Boss", "World Boss", "Rare", "Champion"
    ]
    def __init__(self, name: str, mtype: str, mclass: str, level: int = 1):
        self.name = name
        self.type = mtype
        self.mclass = mclass
        self.level = level
    def __repr__(self):
        return f"{self.name} ({self.type} {self.mclass}, Level {self.level})"

NPC_NAMES = [
    "Deckard Cain", "Lorath Nahr", "Prava", "Donan", "Taissa", "Rathma", "Lilith", "Inarius", "Tyrael", "Adria", "Zoltun Kulle", "Akara", "Griswold", "Wirt"
]

DUNGEONS = [
    "Forgotten Depths", "Shadowed Catacombs", "Frostworn Cavern", "Blood Crypts", "Sunken Ruins", "Ancient Tunnels"
]

RAIDS = [
    "Siege of Hell's Gate", "The Black Citadel", "Stormspire Ascent", "Vault of the Ancients"
]

TRIALS = [
    "Trial of the Ancients", "Endless Arena", "Gauntlet of Shadows", "Sanctum of the Elements"
]

# Open World Zone, Kingdom, Town, and City system
class Zone:
    def __init__(self, name: str, zone_type: str, kingdom: Optional[str] = None):
        self.name = name
        self.zone_type = zone_type  # e.g., 'Town', 'City', 'Wilderness', 'Ruins', etc.
        self.kingdom = kingdom
    def __repr__(self):
        return f"{self.name} ({self.zone_type}{', ' + self.kingdom if self.kingdom else ''})"

KINGDOMS = [
    "Sanctuary", "Westmarch", "Kehjistan", "Scosglen", "Hawezar", "Fractured Peaks", "Dry Steppes", "Arreat", "Kurast"
]

TOWNS = [
    Zone("Kyovashad", "Town", "Fractured Peaks"),
    Zone("Yelesna", "Town", "Fractured Peaks"),
    Zone("Margrave", "Town", "Fractured Peaks"),
    Zone("Backwater", "Town", "Hawezar"),
    Zone("Gea Kul", "Town", "Kehjistan"),
    Zone("Jirandai", "Town", "Dry Steppes")
]

CITIES = [
    Zone("Westmarch", "City", "Sanctuary"),
    Zone("Caldeum", "City", "Kehjistan"),
    Zone("Kurast", "City", "Kurast"),
    Zone("Scosglen City", "City", "Scosglen")
]

OPEN_WORLD_ZONES = TOWNS + CITIES + [
    Zone("Blood Marsh", "Wilderness", "Hawezar"),
    Zone("Dismal Foothills", "Wilderness", "Fractured Peaks"),
    Zone("Forgotten Ruins", "Ruins", "Kehjistan")
]

# Codex system for lore, monsters, items, and locations
class Codex:
    def __init__(self):
        self.entries = {}
    def add_entry(self, category: str, name: str, description: str):
        if category not in self.entries:
            self.entries[category] = {}
        self.entries[category][name] = description
    def get_entry(self, category: str, name: str):
        return self.entries.get(category, {}).get(name, None)
    def list_entries(self, category: str):
        return list(self.entries.get(category, {}).keys())

# Party, Trial, and Raid group systems
class Party:
    def __init__(self, members=None):
        self.members = members if members else []  # up to 4
    def add_member(self, character):
        if len(self.members) < 4:
            self.members.append(character)
    def remove_member(self, character):
        if character in self.members:
            self.members.remove(character)
    def __repr__(self):
        return f"Party: {[m.name for m in self.members]}"

class TrialGroup:
    def __init__(self, members=None):
        self.members = members if members else []  # up to 6
    def add_member(self, character):
        if len(self.members) < 6:
            self.members.append(character)
    def remove_member(self, character):
        if character in self.members:
            self.members.remove(character)
    def __repr__(self):
        return f"Trial Group: {[m.name for m in self.members]}"

class RaidGroup:
    def __init__(self, members=None):
        self.members = members if members else []  # up to 12
    def add_member(self, character):
        if len(self.members) < 12:
            self.members.append(character)
    def remove_member(self, character):
        if character in self.members:
            self.members.remove(character)
    def __repr__(self):
        return f"Raid Group: {[m.name for m in self.members]}"

# Nemesis system (inspired by Shadow of Mordor)
class Nemesis:
    RANKS = ["Grunt", "Captain", "Warchief", "Overlord"]
    ABILITIES = [
        "Poison Weapon", "Fire Aura", "Regeneration", "Teleport", "Summon Minions", "Fearless", "Enrage", "Berserk", "Stealth", "Explosive Death"
    ]
    def __init__(self, name: str, rank: Optional[str] = None, abilities: Optional[list] = None, level: int = 1):
        self.name = name
        self.rank = rank if rank is not None else random.choice(Nemesis.RANKS)
        self.abilities = abilities if abilities is not None else random.sample(Nemesis.ABILITIES, k=random.randint(1, 3))
        self.level = level
        self.is_alive = True
    def promote(self):
        idx = Nemesis.RANKS.index(self.rank)
        if idx < len(Nemesis.RANKS) - 1:
            self.rank = Nemesis.RANKS[idx + 1]
    def add_ability(self, ability: str):
        if ability not in self.abilities and ability in Nemesis.ABILITIES:
            self.abilities.append(ability)
    def defeat(self):
        self.is_alive = False
    def __repr__(self):
        return f"Nemesis: {self.name} (Rank: {self.rank}, Level: {self.level}, Abilities: {', '.join(self.abilities)}, Alive: {self.is_alive})"

# Professions, Jobs, Crafting, Masterwork, and Tempering systems
class Profession:
    PROFESSIONS = [
        "Blacksmith", "Alchemist", "Jeweler", "Enchanter", "Hunter", "Fisher", "Herbalist", "Miner", "Leatherworker"
    ]
    def __init__(self, name: str, level: int = 1):
        self.name = name
        self.level = level
    def __repr__(self):
        return f"{self.name} (Level {self.level})"

class Job:
    JOBS = [
        "Mercenary", "Trader", "Explorer", "Crafter", "Guard", "Scholar", "Healer", "Farmer"
    ]
    def __init__(self, name: str):
        self.name = name
    def __repr__(self):
        return f"Job: {self.name}"

class CraftingSystem:
    def __init__(self):
        self.recipes = {}
    def add_recipe(self, name: str, ingredients: dict, result: str):
        self.recipes[name] = {"ingredients": ingredients, "result": result}
    def craft(self, name: str, inventory: dict):
        recipe = self.recipes.get(name)
        if not recipe:
            return False, "Recipe not found."
        for item, qty in recipe["ingredients"].items():
            if inventory.get(item, 0) < qty:
                return False, f"Missing {item}"
        for item, qty in recipe["ingredients"].items():
            inventory[item] -= qty
        inventory[recipe["result"]] = inventory.get(recipe["result"], 0) + 1
        return True, f"Crafted {recipe['result']}!"

class MasterworkSystem:
    def masterwork(self, item):
        if hasattr(item, 'rarity') and item.rarity in ['Legendary', 'Mythic']:
            if hasattr(item, 'stats'):
                for stat in item.stats:
                    item.stats[stat] = int(item.stats[stat] * 1.2)
            item.rarity = 'Masterwork'
            return True
        return False

class TemperingSystem:
    def temper(self, item, stat: str, amount: int):
        if hasattr(item, 'stats') and stat in item.stats:
            item.stats[stat] += amount
            return True
        return False

# World Level Difficulty System
class WorldDifficulty:
    LEVELS = [
        f"World Tier {i}" for i in range(1, 10)
    ]
    def __init__(self, level: int = 1):
        if 1 <= level <= 9:
            self.level = level
        else:
            self.level = 1
    @property
    def name(self):
        return self.LEVELS[self.level - 1]
    def set_level(self, level: int):
        if 1 <= level <= 9:
            self.level = level
    def __repr__(self):
        return f"{self.name} (Difficulty {self.level})"

# Diablo 3 Rifts, Greater Rifts, Kanai's Cube, and Set Item system
class Rift:
    def __init__(self, level: int = 1, is_greater: bool = False):
        self.level = level
        self.is_greater = is_greater
        self.completed = False
    def complete(self):
        self.completed = True
    def __repr__(self):
        rtype = "Greater Rift" if self.is_greater else "Rift"
        return f"{rtype} (Level {self.level}, Completed: {self.completed})"

class KanaiCube:
    def __init__(self):
        self.powers = {"Weapon": None, "Armor": None, "Jewelry": None}
    def extract_power(self, item):
        if hasattr(item, 'item_type') and hasattr(item, 'name'):
            if item.item_type in self.powers:
                self.powers[item.item_type] = item.name
                return True
        return False
    def get_powers(self):
        return self.powers
    def __repr__(self):
        return f"Kanai's Cube Powers: {self.powers}"

class SetItem:
    def __init__(self, name: str, set_name: str, item_type: str, stats: dict):
        self.name = name
        self.set_name = set_name
        self.item_type = item_type
        self.stats = stats
    def __repr__(self):
        return f"{self.name} (Set: {self.set_name}, Type: {self.item_type}, Stats: {self.stats})"

if __name__ == "__main__":
    char_system = CharacterSystem()
    char_system.add_character(Character("Aiden", "Barbarian", 10))
    char_system.add_character(Character("Lilith", "Sorceress", 15))
    gui = CharacterSystemGUI(char_system)
    gui.run()
