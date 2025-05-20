import tkinter as tk
from tkinter import messagebox
import random
import time

class MainMenuGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Diablo 4 Main Menu")
        self.character = None  # Store the current character
        self.show_loading_screen()
        self.create_menu()

    def show_loading_screen(self):
        loading = tk.Toplevel(self.root)
        loading.title("Loading...")
        loading.geometry("400x250")
        tk.Label(loading, text="DIABLO 4: ETERNAL QUEST", font=("Arial", 20, "bold"), fg="#B22222").pack(pady=20)
        tk.Label(loading, text="by Shadow Studios", font=("Arial", 12)).pack(pady=5)
        tk.Label(loading, text="Engine: PyTkEngine v1.0", font=("Arial", 10, "italic")).pack(pady=5)
        tk.Label(loading, text="Loading... Please wait", font=("Arial", 12)).pack(pady=30)
        self.root.update()
        self.root.after(1800, loading.destroy)

    def create_menu(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        tk.Label(frame, text="DIABLO 4: ETERNAL QUEST", font=("Arial", 18, "bold"), fg="#B22222").pack(pady=5)
        tk.Label(frame, text="by Shadow Studios", font=("Arial", 10)).pack()
        tk.Label(frame, text="Engine: PyTkEngine v1.0", font=("Arial", 9, "italic")).pack(pady=2)
        tk.Button(frame, text="New Game", width=30, command=self.new_game).pack(pady=5)
        tk.Button(frame, text="Continue", width=30, command=self.continue_game).pack(pady=5)
        tk.Button(frame, text="Load Game", width=30, command=self.load_game).pack(pady=5)
        tk.Button(frame, text="Save Game", width=30, command=self.save_game).pack(pady=5)
        tk.Button(frame, text="Patch Notes", width=30, command=self.show_patch_notes).pack(pady=5)
        tk.Button(frame, text="Character System", width=30, command=self.launch_character).pack(pady=5)
        tk.Button(frame, text="Inventory System", width=30, command=self.launch_inventory).pack(pady=5)
        tk.Button(frame, text="Skills System", width=30, command=self.launch_skills).pack(pady=5)
        tk.Button(frame, text="Quests System", width=30, command=self.launch_quests).pack(pady=5)
        tk.Button(frame, text="Map System", width=30, command=self.launch_map).pack(pady=5)
        tk.Button(frame, text="Social System", width=30, command=self.launch_social).pack(pady=5)
        tk.Button(frame, text="Settings", width=30, command=self.launch_settings).pack(pady=5)
        tk.Button(frame, text="Game Credits", width=30, command=self.show_credits).pack(pady=5)
        tk.Button(frame, text="Exit", width=30, command=self.root.quit).pack(pady=20)

    def new_game(self):
        # Initialize/reset game stats for a new game
        self.game_stats = {
            'characters_created': 0,
            'monsters_defeated': 0,
            'bosses_defeated': 0,
            'quests_completed': 0,
            'dungeons_cleared': 0,
            'raids_completed': 0,
            'trials_completed': 0,
            'items_looted': 0,
            'gold_earned': 0,
            'play_time_minutes': 0,
            'highest_level': 1,
            'world_tier': 1,
            'season_number': 0,
            'paragon_points_earned': 0
        }
        # Generate a random seed for the game engine
        self.seed = int(time.time() * 1000) ^ random.randint(0, 2**32-1)
        random.seed(self.seed)
        # Character creation dialog
        self.create_character_dialog()

    def create_character_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Create New Character")
        tk.Label(dialog, text="Enter Character Name:").grid(row=0, column=0, sticky="e")
        name_entry = tk.Entry(dialog)
        name_entry.grid(row=0, column=1)
        tk.Label(dialog, text="Select Class:").grid(row=1, column=0, sticky="e")
        class_var = tk.StringVar(dialog)
        class_var.set("Barbarian")
        class_options = ["Barbarian", "Sorcerer", "Druid", "Rogue", "Necromancer"]
        class_menu = tk.OptionMenu(dialog, class_var, *class_options)
        class_menu.grid(row=1, column=1)
        # Hardcore mode option
        tk.Label(dialog, text="Hardcore Mode:").grid(row=2, column=0, sticky="e")
        hardcore_var = tk.BooleanVar(dialog)
        hardcore_check = tk.Checkbutton(dialog, variable=hardcore_var, text="Permanent death (Hardcore)")
        hardcore_check.grid(row=2, column=1, sticky="w")
        def confirm():
            name = name_entry.get().strip()
            char_class = class_var.get()
            is_hardcore = hardcore_var.get()
            if not name:
                messagebox.showerror("Error", "Please enter a character name.")
                return
            self.character = {
                'name': name,
                'class': char_class,
                'level': 1,
                'xp': 0,
                'stats': {},
                'inventory': [],
                'skills': [],
                'quests': [],
                'hardcore': is_hardcore
            }
            self.game_stats['characters_created'] += 1
            dialog.destroy()
            self.start_campaign_story()
        tk.Button(dialog, text="Create", command=confirm).grid(row=3, column=0, columnspan=2, pady=10)

    def start_campaign_story(self):
        if not self.character:
            messagebox.showerror("Error", "No character found. Please create a character first.")
            return
        intro = (
            f"Welcome, {self.character['name']} the {self.character['class']}!\n\n"
            f"Mode: {'Hardcore' if self.character.get('hardcore') else 'Normal'}\n\n"
            "Your journey begins in the snow-swept wilds of Sanctuary.\n"
            "Darkness stirs, and the fate of the world rests on your shoulders.\n\n"
            "[Prologue: The First Steps]\n\n"
            "You awaken in a ruined village, the distant howls of monsters echoing in the night...\n"
            "(Campaign story mode started!)"
        )
        messagebox.showinfo("Campaign Start", intro)

    def continue_game(self):
        # Continue logic for resuming last character and campaign
        if not hasattr(self, 'character') or not self.character:
            messagebox.showinfo("Continue", "No saved character found. Please start a new game.")
            return
        # Show full stats and launch gameplay
        stats = self.character.get('stats', {})
        stats_str = '\n'.join([f"{k}: {v}" for k, v in stats.items()]) if stats else 'No stats.'
        info = (
            f"Continuing your adventure as {self.character['name']} the {self.character['class']}!\n"
            f"Mode: {'Hardcore' if self.character.get('hardcore') else 'Normal'}\n"
            f"Level: {self.character.get('level', 1)}\nXP: {self.character.get('xp', 0)}\n"
            f"Stats:\n{stats_str}\n"
            f"Inventory: {len(self.character.get('inventory', []))} items\n"
            f"Quests: {len(self.character.get('quests', []))} active\n"
            f"Skills: {len(self.character.get('skills', []))} unlocked\n"
            "\n(Implement full state restore and gameplay logic here.)"
        )
        messagebox.showinfo("Continue", info)
        self.launch_campaign_gameplay()

    def launch_campaign_gameplay(self):
        # Main gameplay window with world creation after new game
        if not self.character:
            messagebox.showerror("Error", "No character loaded.")
            return
        gameplay = tk.Toplevel(self.root)
        gameplay.title("Campaign Gameplay")
        tk.Label(gameplay, text=f"{self.character['name']} the {self.character['class']} - {'Hardcore' if self.character.get('hardcore') else 'Normal'}", font=("Arial", 14, "bold")).pack(pady=10)
        # Show stats
        stats = self.character.get('stats', {})
        stats_str = '\n'.join([f"{k}: {v}" for k, v in stats.items()]) if stats else 'No stats.'
        tk.Label(gameplay, text=f"Level: {self.character.get('level', 1)} | XP: {self.character.get('xp', 0)}").pack()
        tk.Label(gameplay, text=f"Stats:\n{stats_str}").pack()
        # Show inventory, quests, skills summary
        tk.Label(gameplay, text=f"Inventory: {len(self.character.get('inventory', []))} items").pack()
        tk.Label(gameplay, text=f"Quests: {len(self.character.get('quests', []))} active").pack()
        tk.Label(gameplay, text=f"Skills: {len(self.character.get('skills', []))} unlocked").pack()
        # World creation/summary after new game
        if not hasattr(self, 'game_world') or not self.game_world:
            self.create_game_world()
        tk.Label(gameplay, text=f"Current Zone: {self.game_world.get('zone', 'Unknown')}").pack(pady=5)
        tk.Label(gameplay, text=f"World Tier: {self.game_world.get('world_tier', 1)}").pack()
        # Gameplay actions
        tk.Button(gameplay, text="Open Map", command=self.launch_map).pack(pady=2)
        tk.Button(gameplay, text="Open Inventory", command=self.launch_inventory).pack(pady=2)
        tk.Button(gameplay, text="Open Quests", command=self.launch_quests).pack(pady=2)
        tk.Button(gameplay, text="Open Skills", command=self.launch_skills).pack(pady=2)
        tk.Button(gameplay, text="Open Social", command=self.launch_social).pack(pady=2)
        tk.Button(gameplay, text="Open Settings", command=self.launch_settings).pack(pady=2)
        tk.Button(gameplay, text="Exit to Main Menu", command=gameplay.destroy).pack(pady=10)

    def create_game_world(self):
        # Create a new game world after new game
        # Generate a world seed for reproducibility
        self.world_seed = int(time.time() * 1000) ^ random.randint(0, 2**32-1)
        random.seed(self.world_seed)
        # Define a grid-based world map (10x10 for example)
        self.world_map = {}
        towns = [
            {'name': 'Kyovashad', 'type': 'Town', 'x': 2, 'y': 7},
            {'name': 'Yelesna', 'type': 'Town', 'x': 4, 'y': 8},
            {'name': 'Margrave', 'type': 'Town', 'x': 1, 'y': 6},
            {'name': 'Backwater', 'type': 'Town', 'x': 7, 'y': 2},
            {'name': 'Gea Kul', 'type': 'City', 'x': 8, 'y': 1},
            {'name': 'Jirandai', 'type': 'Town', 'x': 6, 'y': 3},
            {'name': 'Westmarch', 'type': 'City', 'x': 9, 'y': 9},
            {'name': 'Caldeum', 'type': 'City', 'x': 3, 'y': 1},
        ]
        zones = [
            {'name': 'Blood Marsh', 'type': 'Wilderness', 'x': 5, 'y': 5},
            {'name': 'Dismal Foothills', 'type': 'Wilderness', 'x': 2, 'y': 2},
            {'name': 'Forgotten Ruins', 'type': 'Ruins', 'x': 7, 'y': 7},
        ]
        # Fill the world map grid
        for t in towns:
            self.world_map[(t['x'], t['y'])] = t
        for z in zones:
            self.world_map[(z['x'], z['y'])] = z
        # Example: assign starting zone, world tier, and other world state
        self.game_world = {
            'zone': 'Kyovashad',  # Starting city/zone
            'zone_coords': (2, 7),
            'world_tier': self.game_stats.get('world_tier', 1),
            'difficulty': 'World Tier 1',
            'time_of_day': 'Morning',
            'weather': 'Clear',
            'events': [],
            'npcs': ['Blacksmith', 'Alchemist', 'Banker', 'Tree of Whispers'],
            'vendors': ['General Goods', 'Jeweler', 'Purveyor of Curiosities'],
            'bank': {'slots': 20, 'items': []},
            'tree_of_whispers': {'grim_favors': 0, 'rewards': []},
            'world_seed': self.world_seed,
            'world_map': self.world_map
        }

    def load_game(self):
        import pickle
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(title="Load Game", filetypes=[("Save Files", "*.d4save")])
        if file_path:
            try:
                with open(file_path, "rb") as f:
                    game_state = pickle.load(f)
                messagebox.showinfo("Load Game", f"Game loaded from {file_path}\n(Implement state restore)")
            except Exception as e:
                messagebox.showerror("Load Error", f"Failed to load: {e}")

    def save_game(self):
        import pickle
        from tkinter import filedialog
        file_path = filedialog.asksaveasfilename(title="Save Game", defaultextension=".d4save", filetypes=[("Save Files", "*.d4save")])
        if file_path:
            try:
                game_state = {}  # Replace with actual game state
                with open(file_path, "wb") as f:
                    pickle.dump(game_state, f)
                messagebox.showinfo("Save Game", f"Game saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save: {e}")

    def launch_character(self):
        import character_system
        character_system.CharacterSystemGUI(character_system.CharacterSystem()).run()

    def launch_inventory(self):
        import importlib.util
        import sys
        inv_mod_name = 'from typing import List, Dict, Optional'
        inv_mod_path = 'from typing import List, Dict, Optional.py'
        spec = importlib.util.spec_from_file_location(inv_mod_name, inv_mod_path)
        if spec and spec.loader:
            inv_mod = importlib.util.module_from_spec(spec)
            sys.modules[inv_mod_name] = inv_mod
            spec.loader.exec_module(inv_mod)
            inv = inv_mod.Inventory()
            inv.add_item(inv_mod.Item("Sword of Doom", "Weapon", "Legendary", {"Damage": 100}, (2,1)))
            inv.add_item(inv_mod.Item("Iron Helm", "Armor", "Rare", {"Armor": 20}, (2,2)))
            inv.add_item(inv_mod.Item("Health Potion", "Potion", "Common", {"Heal": 50}, (1,1)))
            inv_mod.InventoryGUI(inv).run()
        else:
            from tkinter import messagebox
            messagebox.showerror("Error", "Could not load Inventory module.")

    def launch_skills(self):
        import skills_system
        skills_system.SkillsSystemGUI(skills_system.SkillsSystem()).run()

    def launch_quests(self):
        import quests_system
        quests_system.QuestsSystemGUI(quests_system.QuestsSystem()).run()

    def launch_map(self):
        # Show a simple world map with towns, cities, and zones on a grid
        map_win = tk.Toplevel(self.root)
        map_win.title("World Map")
        canvas = tk.Canvas(map_win, width=400, height=400, bg="#222")
        canvas.pack()
        grid_size = 10
        cell = 40
        # Draw grid
        for i in range(grid_size+1):
            canvas.create_line(cell, cell+i*cell, cell+grid_size*cell, cell+i*cell, fill="#444")
            canvas.create_line(cell+i*cell, cell, cell+i*cell, cell+grid_size*cell, fill="#444")
        # Draw towns/cities/zones
        for (x, y), loc in self.game_world['world_map'].items():
            color = "#FFD700" if loc['type'] == 'City' else ("#00FF00" if loc['type'] == 'Town' else "#FF6347")
            canvas.create_oval(cell+x*cell-10, cell+y*cell-10, cell+x*cell+10, cell+y*cell+10, fill=color)
            canvas.create_text(cell+x*cell, cell+y*cell-15, text=loc['name'], fill="#FFF", font=("Arial", 8, "bold"))
            canvas.create_text(cell+x*cell, cell+y*cell+15, text=f"({x},{y})", fill="#AAA", font=("Arial", 7))
        # Show current location
        zx, zy = self.game_world.get('zone_coords', (2, 7))
        canvas.create_rectangle(cell+zx*cell-14, cell+zy*cell-14, cell+zx*cell+14, cell+zy*cell+14, outline="#00BFFF", width=2)
        tk.Label(map_win, text=f"World Seed: {self.game_world.get('world_seed')}").pack()

    def show_credits(self):
        credits = (
            "Game Credits\n"
            "-----------------------------\n"
            "Lead Developer: Shadow\n"
            "Gameplay Design: Shadow\n"
            "UI/UX: Shadow\n"
            "Systems & Lore: Shadow\n"
            "Testing: Shadow\n"
            "Special Thanks: OpenAI, Diablo & WoW Communities\n"
            "Engine: PyTkEngine v1.0\n"
            "\nAll content is fan-made and non-commercial."
        )
        messagebox.showinfo("Game Credits", credits)

    def show_patch_notes(self):
        try:
            with open('PATCH_NOTES.md', 'r', encoding='utf-8') as f:
                notes = f.read()
            messagebox.showinfo("Patch Notes", notes)
        except Exception as e:
            messagebox.showerror("Patch Notes", f"Could not load patch notes: {e}")

    def run(self):
        self.root.mainloop()

# Gameplay Modes, Realms, Battle Pass, Auction House, and Factions
class GameplayMode:
    MODES = ["Offline", "Online"]
    def __init__(self, mode: str = "Offline"):
        self.mode = mode if mode in self.MODES else "Offline"
    def set_mode(self, mode: str):
        if mode in self.MODES:
            self.mode = mode
    def __repr__(self):
        return f"Gameplay Mode: {self.mode}"

class SeasonMode:
    def __init__(self, is_season: bool = False, season_number: int = 0):
        self.is_season = is_season
        self.season_number = season_number
    def start_season(self, number: int):
        self.is_season = True
        self.season_number = number
    def end_season(self):
        self.is_season = False
        self.season_number = 0
    def __repr__(self):
        return f"Season Mode: {'Season ' + str(self.season_number) if self.is_season else 'Eternal Realm'}"

class EternalRealm:
    def __init__(self):
        self.active = True
    def __repr__(self):
        return "Eternal Realm (Non-seasonal)"

class BattlePass:
    def __init__(self, level: int = 1, max_level: int = 100):
        self.level = level
        self.max_level = max_level
        self.rewards = {}
    def add_reward(self, level: int, reward: str):
        self.rewards[level] = reward
    def claim_reward(self, level: int):
        return self.rewards.get(level, None)
    def progress(self, amount: int = 1):
        self.level = min(self.level + amount, self.max_level)
    def __repr__(self):
        return f"Battle Pass: Level {self.level}/{self.max_level}"

class AuctionHouse:
    def __init__(self):
        self.listings = []  # Each listing: {item, seller, price}
    def list_item(self, item, seller, price):
        self.listings.append({"item": item, "seller": seller, "price": price})
    def buy_item(self, index: int, buyer):
        if 0 <= index < len(self.listings):
            listing = self.listings.pop(index)
            return listing
        return None
    def __repr__(self):
        return f"Auction House: {len(self.listings)} listings"

class Faction:
    FACTIONS = ["Merchant Guild", "Circle of Fortune"]
    def __init__(self, name: str):
        if name in self.FACTIONS:
            self.name = name
        else:
            self.name = self.FACTIONS[0]
    def __repr__(self):
        return f"Faction: {self.name}"

# Last Epoch-style Skill Tree, Passives Tree, DPS Calculation, Character Level/XP, and Paragon System
class SkillNode:
    def __init__(self, name: str, description: str, required_points: int = 1, unlocked: bool = False):
        self.name = name
        self.description = description
        self.required_points = required_points
        self.unlocked = unlocked
    def __repr__(self):
        return f"SkillNode({self.name}, Unlocked: {self.unlocked})"

class SkillTree:
    def __init__(self):
        self.nodes = []  # List[SkillNode]
        self.points = 0
    def add_node(self, node: SkillNode):
        self.nodes.append(node)
    def unlock(self, node_name: str):
        for node in self.nodes:
            if node.name == node_name and self.points >= node.required_points:
                node.unlocked = True
                self.points -= node.required_points
                return True
        return False
    def __repr__(self):
        return f"SkillTree: {[n.name for n in self.nodes if n.unlocked]}"

class PassiveNode:
    def __init__(self, name: str, effect: str, required_points: int = 1, unlocked: bool = False):
        self.name = name
        self.effect = effect
        self.required_points = required_points
        self.unlocked = unlocked
    def __repr__(self):
        return f"PassiveNode({self.name}, Unlocked: {self.unlocked})"

class PassivesTree:
    def __init__(self):
        self.nodes = []  # List[PassiveNode]
        self.points = 0
    def add_node(self, node: PassiveNode):
        self.nodes.append(node)
    def unlock(self, node_name: str):
        for node in self.nodes:
            if node.name == node_name and self.points >= node.required_points:
                node.unlocked = True
                self.points -= node.required_points
                return True
        return False
    def __repr__(self):
        return f"PassivesTree: {[n.name for n in self.nodes if n.unlocked]}"

class CharacterLevel:
    def __init__(self, level: int = 1, xp: int = 0):
        self.level = level
        self.xp = xp
        self.max_level = 100
    def add_xp(self, amount: int):
        self.xp += amount
        while self.level < self.max_level and self.xp >= self.xp_to_next():
            self.xp -= self.xp_to_next()
            self.level += 1
    def xp_to_next(self):
        return 100 + (self.level - 1) * 25  # Example curve
    def __repr__(self):
        return f"Level {self.level} (XP: {self.xp}/{self.xp_to_next()})"

class ParagonSystem:
    def __init__(self):
        self.points = 0
        self.max_points = 200
        self.bonuses = {}
    def add_point(self, stat: str):
        if self.points < self.max_points:
            self.bonuses[stat] = self.bonuses.get(stat, 0) + 1
            self.points += 1
    def __repr__(self):
        return f"Paragon: {self.points}/{self.max_points} ({self.bonuses})"

# DPS Calculation utility
class DPSCalculator:
    @staticmethod
    def calculate(base_damage: int, attack_speed: float, crit_chance: float, crit_mult: float, flat_bonus: int = 0, percent_bonus: float = 0.0):
        crit = 1 + (crit_chance * (crit_mult - 1))
        dps = ((base_damage + flat_bonus) * (1 + percent_bonus)) * attack_speed * crit
        return dps

if __name__ == "__main__":
    MainMenuGUI().run()
