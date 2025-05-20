import random
import time
import os
import pickle
import sys
import importlib.util
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk

# Import referenced subsystems (if available)
try:
    import character_system
except ImportError:
    character_system = None
try:
    import skills_system
except ImportError:
    skills_system = None
try:
    import quests_system
except ImportError:
    quests_system = None
try:
    import social_system
except ImportError:
    social_system = None
try:
    import settings_system
except ImportError:
    settings_system = None

# === CRAFTING SYSTEM (Last Epoch & Diablo 4 inspired) ===
class CraftingSystem:
    def __init__(self):
        self.materials = {
            'Iron Ore': 10,
            'Leather': 8,
            'Arcane Dust': 5,
            'Crystal Shard': 2,
            'Gold': 1000
        }
        self.crafting_recipes = [
            {'name': 'Iron Sword', 'materials': {'Iron Ore': 3, 'Leather': 1}, 'base_item': 'Iron Sword'},
            {'name': 'Magic Staff', 'materials': {'Arcane Dust': 3, 'Crystal Shard': 1}, 'base_item': 'Ancient Staff'},
            {'name': 'Leather Armor', 'materials': {'Leather': 4, 'Iron Ore': 1}, 'base_item': 'Leather Armor'},
            {'name': 'Enchanted Ring', 'materials': {'Arcane Dust': 2, 'Gold': 200}, 'base_item': 'Ring of Power'},
        ]
        self.affix_pool = GEAR_PREFIXES + GEAR_SUFFIXES

    def can_craft(self, recipe_name):
        recipe = next((r for r in self.crafting_recipes if r['name'] == recipe_name), None)
        if not recipe:
            return False
        for mat, amt in recipe['materials'].items():
            if self.materials.get(mat, 0) < amt:
                return False
        return True

    def craft(self, recipe_name):
        recipe = next((r for r in self.crafting_recipes if r['name'] == recipe_name), None)
        if not recipe or not self.can_craft(recipe_name):
            return None
        # Deduct materials
        for mat, amt in recipe['materials'].items():
            self.materials[mat] -= amt
        # Add random affixes (prefix and suffix)
        import random
        prefix = random.choice(GEAR_PREFIXES)
        suffix = random.choice(GEAR_SUFFIXES)
        crafted_item = {
            'name': f"{prefix['name']} {recipe['base_item']} {suffix['name']}",
            'type': next((l['type'] for l in LOOT_TABLE if l['item'] == recipe['base_item']), 'Unknown'),
            'rarity': 'Crafted',
            'prefix': prefix['effect'],
            'suffix': suffix['effect']
        }
        return crafted_item

    def add_materials(self, mat, amt):
        self.materials[mat] = self.materials.get(mat, 0) + amt

    def get_materials(self):
        return self.materials.copy()

    def get_recipes(self):
        return [r['name'] for r in self.crafting_recipes]

class CombatSystem:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turn = 'player'  # or 'enemy'
        self.log = []
        self.player_hp = player.get('stats', {}).get('hp', 100)
        self.enemy_hp = enemy.get('hp', 50)
        self.player_max_hp = player.get('stats', {}).get('max_hp', 100)
        self.enemy_max_hp = enemy.get('hp', 50)
        self.player_mana = player.get('stats', {}).get('mana', 50)
        self.player_max_mana = player.get('stats', {}).get('max_mana', 50)
        self.status = {'player': [], 'enemy': []}
        self.result = None

    def player_attack(self):
        base = self.player.get('stats', {}).get('attack', 10)
        speed = self.player.get('stats', {}).get('attack_speed', 1.0)
        crit = self.player.get('stats', {}).get('crit_chance', 0.05)
        crit_mult = self.player.get('stats', {}).get('crit_mult', 2.0)
        dmg = DPSCalculator.calculate(base, speed, crit, crit_mult)
        dmg = int(dmg * random.uniform(0.8, 1.2))
        self.enemy_hp -= dmg
        self.log.append(f"Player attacks for {dmg} damage!")
        if self.enemy_hp <= 0:
            self.enemy_hp = 0
            self.result = 'win'
            self.log.append("Enemy defeated!")
        self.turn = 'enemy'

    def enemy_attack(self):
        base = self.enemy.get('attack', 8)
        speed = self.enemy.get('attack_speed', 1.0)
        crit = self.enemy.get('crit_chance', 0.05)
        crit_mult = self.enemy.get('crit_mult', 1.5)
        dmg = DPSCalculator.calculate(base, speed, crit, crit_mult)
        dmg = int(dmg * random.uniform(0.8, 1.2))
        self.player_hp -= dmg
        self.log.append(f"Enemy attacks for {dmg} damage!")
        if self.player_hp <= 0:
            self.player_hp = 0
            self.result = 'lose'
            self.log.append("You have been defeated!")
        self.turn = 'player'

    def use_skill(self, skill):
        # Example: skills cost mana, deal extra damage
        cost = skill.get('mana_cost', 10)
        if self.player_mana < cost:
            self.log.append("Not enough mana!")
            return
        self.player_mana -= cost
        base = self.player.get('stats', {}).get('attack', 10) + skill.get('power', 10)
        dmg = int(base * random.uniform(1.1, 1.5))
        self.enemy_hp -= dmg
        self.log.append(f"Player uses {skill['name']} for {dmg} damage!")
        if self.enemy_hp <= 0:
            self.enemy_hp = 0
            self.result = 'win'
            self.log.append("Enemy defeated!")
        self.turn = 'enemy'

    def is_over(self):
        return self.result is not None

    def get_log(self):
        return '\n'.join(self.log[-6:])

class CombatSystemGUI:
    def __init__(self, root, player, enemy):
        self.root = tk.Toplevel(root)
        self.root.title("Combat Encounter")
        self.combat = CombatSystem(player, enemy)
        self._draw_ui()
        self._update_ui()

    def _draw_ui(self):
        self.info = tk.Label(self.root, text="", font=("Arial", 12, "bold"))
        self.info.pack(pady=5)
        self.player_bar = tk.Label(self.root, text="", fg="#0a0")
        self.player_bar.pack()
        self.enemy_bar = tk.Label(self.root, text="", fg="#a00")
        self.enemy_bar.pack()
        self.log = tk.Label(self.root, text="", justify='left', anchor='w')
        self.log.pack(pady=5)
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(pady=5)
        self.attack_btn = tk.Button(self.btn_frame, text="Attack", width=14, command=self._attack)
        self.attack_btn.grid(row=0, column=0, padx=2)
        self.skill_btn = tk.Button(self.btn_frame, text="Use Skill", width=14, command=self._use_skill)
        self.skill_btn.grid(row=0, column=1, padx=2)
        self.end_btn = tk.Button(self.btn_frame, text="End Turn", width=14, command=self._end_turn)
        self.end_btn.grid(row=0, column=2, padx=2)
        self.close_btn = tk.Button(self.root, text="Close", command=self.root.destroy)
        self.close_btn.pack(pady=5)

    def _update_ui(self):
        c = self.combat
        self.info.config(text=f"Player HP: {c.player_hp}/{c.player_max_hp} | Mana: {c.player_mana}/{c.player_max_mana}\nEnemy HP: {c.enemy_hp}/{c.enemy_max_hp}")
        self.player_bar.config(text=f"Player: {c.player['name']} ({c.player.get('class', 'Hero')})")
        self.enemy_bar.config(text=f"Enemy: {c.enemy['name']} (Lv{c.enemy.get('level', 1)})")
        self.log.config(text=c.get_log())
        if c.is_over():
            self.attack_btn.config(state='disabled')
            self.skill_btn.config(state='disabled')
            self.end_btn.config(state='disabled')
            if c.result == 'win':
                self.info.config(text="Victory! You defeated the enemy.")
            else:
                self.info.config(text="Defeat! You have fallen.")
        elif c.turn == 'player':
            self.attack_btn.config(state='normal')
            self.skill_btn.config(state='normal')
            self.end_btn.config(state='normal')
        else:
            self.attack_btn.config(state='disabled')
            self.skill_btn.config(state='disabled')
            self.end_btn.config(state='disabled')
            self.root.after(1200, self._enemy_turn)

    def _attack(self):
        self.combat.player_attack()
        self._update_ui()

    def _use_skill(self):
        # Use first available skill for demo
        skills = self.combat.player.get('skills', [])
        if not skills:
            skills = DIABLO4_SKILLS.get(self.combat.player.get('class', 'Barbarian'), [])
        if skills:
            skill = skills[0].copy()
            # Remove type restriction: ensure skill dict can accept int for 'power' and 'mana_cost'
            # If skill dict is type-restricted, use a new dict for combat logic
            skill = dict(skill)
            self.combat.use_skill(skill)
        else:
            self.combat.log.append("No skills available!")
        self._update_ui()

    def _end_turn(self):
        self.combat.turn = 'enemy'
        self._update_ui()

    def _enemy_turn(self):
        if not self.combat.is_over():
            self.combat.enemy_attack()
            self._update_ui()

class SocialSystem:
    def __init__(self):
        self.friends = []
        self.blocked = []
        self.party = None

    def add_friend(self, player_name):
        if player_name not in self.friends:
            self.friends.append(player_name)

    def remove_friend(self, player_name):
        if player_name in self.friends:
            self.friends.remove(player_name)

    def block_player(self, player_name):
        if player_name not in self.blocked:
            self.blocked.append(player_name)
        if player_name in self.friends:
            self.friends.remove(player_name)  # Unfriend if blocked

    def unblock_player(self, player_name):
        if player_name in self.blocked:
            self.blocked.remove(player_name)

    def create_party(self, leader):
        self.party = {'leader': leader, 'members': [leader]}

    def join_party(self, player_name):
        if self.party and player_name not in self.party['members']:
            self.party['members'].append(player_name)

    def leave_party(self, player_name):
        if self.party and player_name in self.party['members']:
            self.party['members'].remove(player_name)
        if self.party and self.party['leader'] == player_name:
            self.party = None  # Dissolve party if leader leaves

    def get_party_members(self):
        return self.party['members'] if self.party else []

    def is_blocked(self, player_name):
        return player_name in self.blocked

    def is_friend(self, player_name):
        return player_name in self.friends

class PartySystem:
    def __init__(self):
        self.parties = {}  # Active parties {party_id: party_data}
        self.next_party_id = 1

    def create_party(self, leader):
        party_id = self.next_party_id
        self.parties[party_id] = {'id': party_id, 'leader': leader, 'members': [leader]}
        self.next_party_id += 1
        return party_id

    def join_party(self, party_id, player_name):
        if party_id in self.parties:
            party = self.parties[party_id]
            if player_name not in party['members']:
                party['members'].append(player_name)
                return True
        return False

    def leave_party(self, party_id, player_name):
        if party_id in self.parties:
            party = self.parties[party_id]
            if player_name in party['members']:
                party['members'].remove(player_name)
                if party['leader'] == player_name:
                    self.dissolve_party(party_id)  # Dissolve if leader leaves
                return True
        return False

    def dissolve_party(self, party_id):
        if party_id in self.parties:
            del self.parties[party_id]

    def get_party(self, party_id):
        return self.parties.get(party_id, None)

    def is_in_party(self, player_name):
        for party in self.parties.values():
            if player_name in party['members']:
                return party
        return None

class SocialSystemGUI:
    def __init__(self, root, social_system):
        self.root = tk.Toplevel(root)
        self.root.title("Social System")
        self.social_system = social_system
        self._draw_ui()

    def _draw_ui(self):
        tk.Label(self.root, text="Friends:", font=("Arial", 12, "bold")).pack(pady=5)
        self.friends_list = tk.Listbox(self.root)
        self.friends_list.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        tk.Button(self.root, text="Add Friend", command=self._add_friend).pack(pady=5)
        tk.Button(self.root, text="Remove Friend", command=self._remove_friend).pack(pady=5)
        tk.Button(self.root, text="Block Player", command=self._block_player).pack(pady=5)
        tk.Button(self.root, text="Unblock Player", command=self._unblock_player).pack(pady=5)
        tk.Button(self.root, text="Close", command=self.root.destroy).pack(pady=5)
        self._update_friends_list()

    def _update_friends_list(self):
        self.friends_list.delete(0, tk.END)
        for friend in self.social_system.friends:
            self.friends_list.insert(tk.END, friend)

    def _add_friend(self):
        name = self._prompt_player_name("Add Friend")
        if name:
            self.social_system.add_friend(name)
            self._update_friends_list()

    def _remove_friend(self):
        selected = self.friends_list.curselection()
        if selected:
            friend = self.friends_list.get(selected)
            self.social_system.remove_friend(friend)
            self._update_friends_list()

    def _block_player(self):
        name = self._prompt_player_name("Block Player")
        if name:
            self.social_system.block_player(name)

    def _unblock_player(self):
        name = self._prompt_player_name("Unblock Player")
        if name:
            self.social_system.unblock_player(name)

    def _prompt_player_name(self, action):
        name = simpledialog.askstring("Player Name", f"Enter the name of the player to {action.lower()}:")
        return name.strip() if name else None

class RaidSystem:
    def __init__(self):
        self.raids = [
            {'name': 'Sanctum of Shadows', 'level': 30, 'boss': 'Shadow Lord', 'min_party': 4, 'max_party': 8},
            {'name': 'Citadel of Storms', 'level': 45, 'boss': 'Tempest Queen', 'min_party': 6, 'max_party': 12},
            {'name': 'Infernal Depths', 'level': 60, 'boss': 'Hellfire Behemoth', 'min_party': 8, 'max_party': 16},
        ]
        self.active_raid = None
    def list_raids(self):
        return self.raids
    def start_raid(self, raid_name, party):
        raid = next((r for r in self.raids if r['name'] == raid_name), None)
        if raid and len(party) >= raid['min_party']:
            self.active_raid = {'raid': raid, 'party': party, 'progress': 0}
            return True
        return False
    def complete_raid(self):
        if self.active_raid:
            raid = self.active_raid['raid']
            self.active_raid = None
            return f"Raid '{raid['name']}' completed! Boss '{raid['boss']}' defeated!"
        return "No active raid."

class TrialSystem:
    def __init__(self):
        self.trials = [
            {'name': 'Trial of Valor', 'level': 10, 'type': 'Solo'},
            {'name': 'Trial of Endurance', 'level': 20, 'type': 'Party'},
            {'name': 'Trial of Elements', 'level': 35, 'type': 'Solo'},
            {'name': 'Trial of Champions', 'level': 50, 'type': 'Party'},
        ]
        self.active_trial = None
    def list_trials(self):
        return self.trials
    def start_trial(self, trial_name, party):
        trial = next((t for t in self.trials if t['name'] == trial_name), None)
        if trial and (trial['type'] == 'Solo' or (party and len(party) > 1)):
            self.active_trial = {'trial': trial, 'party': party, 'progress': 0}
            return True
        return False
    def complete_trial(self):
        if self.active_trial:
            trial = self.active_trial['trial']
            self.active_trial = None
            return f"Trial '{trial['name']}' completed!"
        return "No active trial."

class DungeonSystem:
    def __init__(self):
        self.dungeons = [
            {'name': 'Crypt of the Fallen', 'level': 5, 'boss': 'Bone Warden'},
            {'name': 'Spider Lair', 'level': 12, 'boss': 'Broodmother'},
            {'name': 'Sunken Catacombs', 'level': 20, 'boss': 'Drowned King'},
            {'name': 'Frost Cavern', 'level': 28, 'boss': 'Ice Revenant'},
            {'name': 'Obsidian Halls', 'level': 35, 'boss': 'Obsidian Golem'},
            {'name': 'Temple of Light', 'level': 42, 'boss': 'Radiant Seraph'},
            {'name': 'Infernal Depths', 'level': 60, 'boss': 'Hellfire Behemoth'},
        ]
        self.active_dungeon = None
    def list_dungeons(self):
        return self.dungeons
    def start_dungeon(self, dungeon_name, party):
        dungeon = next((d for d in self.dungeons if d['name'] == dungeon_name), None)
        if dungeon:
            self.active_dungeon = {'dungeon': dungeon, 'party': party, 'progress': 0}
            return True
        return False
    def complete_dungeon(self):
        if self.active_dungeon:
            dungeon = self.active_dungeon['dungeon']
            self.active_dungeon = None
            return f"Dungeon '{dungeon['name']}' completed! Boss '{dungeon['boss']}' defeated!"
        return "No active dungeon."

class PartyFinderSystem:
    def __init__(self, party_system, dungeon_system):
        self.party_system = party_system
        self.dungeon_system = dungeon_system
        self.lfg_queue = []  # List of {'player': name, 'dungeon': dungeon_name}
    def join_lfg(self, player_name, dungeon_name):
        self.lfg_queue.append({'player': player_name, 'dungeon': dungeon_name})
    def find_party(self, dungeon_name):
        # Group players queued for the same dungeon into parties of 4
        queued = [q['player'] for q in self.lfg_queue if q['dungeon'] == dungeon_name]
        parties = [queued[i:i+4] for i in range(0, len(queued), 4)]
        formed = []
        for party in parties:
            if len(party) == 4:
                party_id = self.party_system.create_party(party[0])
                for member in party[1:]:
                    self.party_system.join_party(party_id, member)
                formed.append({'party_id': party_id, 'members': party})
                # Remove from queue
                self.lfg_queue = [q for q in self.lfg_queue if q['player'] not in party]
        return formed

# Place new system class definitions BEFORE MainMenuGUI
class InstanceBaseSystem:
    """
    ARPG Instance Base System: Handles instanced dungeons, raids, and world events for parties.
    """
    def __init__(self):
        self.instances = []  # List of {'type': 'dungeon'|'raid'|'event', 'name': str, 'party': list, 'instance_id': int}
        self.next_instance_id = 1
    def create_instance(self, instance_type, name, party):
        instance = {
            'type': instance_type,
            'name': name,
            'party': party,
            'instance_id': self.next_instance_id
        }
        self.instances.append(instance)
        self.next_instance_id += 1
        return instance['instance_id']
    def get_instance(self, instance_id):
        for inst in self.instances:
            if inst['instance_id'] == instance_id:
                return inst
        return None
    def close_instance(self, instance_id):
        self.instances = [inst for inst in self.instances if inst['instance_id'] != instance_id]
    def list_instances(self):
        return self.instances.copy()

class DungeonFinderSystem:
    """
    Dungeon Finder: Queue for dungeons, auto-match parties, and teleport to instance.
    """
    def __init__(self, party_system, dungeon_system, instance_base_system):
        self.party_system = party_system
        self.dungeon_system = dungeon_system
        self.instance_base_system = instance_base_system
        self.lfd_queue = []  # [{'player': name, 'dungeon': dungeon_name}]
    def join_lfd(self, player_name, dungeon_name):
        self.lfd_queue.append({'player': player_name, 'dungeon': dungeon_name})
    def match_parties(self, dungeon_name):
        queued = [q['player'] for q in self.lfd_queue if q['dungeon'] == dungeon_name]
        parties = [queued[i:i+4] for i in range(0, len(queued), 4)]
        formed = []
        for party in parties:
            if len(party) == 4:
                party_id = self.party_system.create_party(party[0])
                for member in party[1:]:
                    self.party_system.join_party(party_id, member)
                instance_id = self.instance_base_system.create_instance('dungeon', dungeon_name, party)
                formed.append({'party_id': party_id, 'members': party, 'instance_id': instance_id})
                self.lfd_queue = [q for q in self.lfd_queue if q['player'] not in party]
        return formed

class TeleportSystem:
    """
    Teleport System: Allows teleporting to towns, dungeons, or party/instance locations.
    """
    def __init__(self, world_map):
        self.world_map = world_map  # Dict of (x, y): location dict
    def get_teleport_locations(self):
        # Return all towns, cities, dungeons, and instance entrances
        locs = []
        for loc in self.world_map.values():
            if loc['type'] in ['Town', 'City', 'Kingdom', 'Dungeon']:
                locs.append(loc)
        return locs
    def teleport(self, player, location_name):
        # For demo: just return the location name as the new zone
        return f"Teleported {player} to {location_name}!"

# (Duplicate style_button definition removed)

# (Duplicate style_submenu definition removed)

# === MAIN MENU GUI ===
class MainMenuGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Arcane Engine - Main Menu")
        self.character = None
        self.game_world = None
        self.game_stats = {'characters_created': 0}
        self.season_manager = SeasonManager()
        self.nightmare_manager = NightmareDungeonManager()
        self.social_system = SocialSystem()
        self.party_system = PartySystem()
        self.raid_system = RaidSystem()
        self.trial_system = TrialSystem()
        self.dungeon_system = DungeonSystem()
        self.instance_base_system = InstanceBaseSystem()
        self.party_finder = PartyFinderSystem(self.party_system, self.dungeon_system)
        self.dungeon_finder = DungeonFinderSystem(self.party_system, self.dungeon_system, self.instance_base_system)
        self.teleport_system = None
        self._bg_img = None
        self.show_loading_screen()
        self.create_menu()

    def launch_inventory(self):
        win = tk.Toplevel(self.root)
        win.title("Inventory System")
        self._style_submenu(win)
        tk.Label(win, text="Inventory System (Demo)").pack(pady=5)
        tk.Label(win, text="Feature not implemented yet.").pack(pady=5)
        tk.Button(win, text="Close", command=win.destroy).pack(pady=10)

    def launch_skills(self):
        win = tk.Toplevel(self.root)
        win.title("Skills System")
        self._style_submenu(win)
        tk.Label(win, text="Skills System (Demo)").pack(pady=5)
        tk.Label(win, text="Feature not implemented yet.").pack(pady=5)
        tk.Button(win, text="Close", command=win.destroy).pack(pady=10)

    def launch_quests(self):
        win = tk.Toplevel(self.root)
        win.title("Quests System")
        self._style_submenu(win)
        tk.Label(win, text="Quests System (Demo)").pack(pady=5)
        tk.Label(win, text="Feature not implemented yet.").pack(pady=5)
        tk.Button(win, text="Close", command=win.destroy).pack(pady=10)

    def launch_social(self):
        # Launch the Social System GUI
        SocialSystemGUI(self.root, self.social_system)

    def run(self):
        self.root.mainloop()

    def create_game_world(self):
        # Minimal implementation for demo purposes
        self.game_world = {
            'zone': 'Sanctuary',
            'world_tier': 1
        }
        # Optionally, initialize teleport_system with a dummy world map
        world_map = {
            (0, 0): {'name': 'Sanctuary', 'type': 'Town'},
            (1, 0): {'name': 'Shadow Crypt', 'type': 'Dungeon'},
            (0, 1): {'name': 'Frost Cavern', 'type': 'Dungeon'},
        }
        self.teleport_system = TeleportSystem(world_map)

    def start_campaign_story(self):
        # Placeholder: Launch campaign gameplay window
        self.launch_campaign_gameplay()

    def load_character_list(self):
        # Loads the character list from a file, or returns an empty list if not found
        try:
            with open("characters.pkl", "rb") as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError, pickle.PickleError):
            return []

    def save_character_list(self, char_list):
        # Saves the character list to a file
        try:
            with open("characters.pkl", "wb") as f:
                pickle.dump(char_list, f)
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save character list: {e}")

    def save_game(self):
        # Save the current character to the character list file
        if not self.character:
            messagebox.showinfo("Save Game", "No character loaded to save.")
            return
        char_list = self.load_character_list()
        # Update or add the current character
        updated = False
        for i, char in enumerate(char_list):
            if char.get('name') == self.character.get('name'):
                char_list[i] = self.character
                updated = True
                break
        if not updated:
            char_list.append(self.character)
        try:
            with open("characters.pkl", "wb") as f:
                pickle.dump(char_list, f)
            messagebox.showinfo("Save Game", "Game saved successfully!")
        except Exception as e:
            messagebox.showerror("Save Game", f"Failed to save game: {e}")

    def continue_game(self):
        # Attempt to load the most recent character and start the campaign
        char_list = self.load_character_list()
        if char_list:
            self.character = char_list[-1]  # Continue with the last character
            self.start_campaign_story()
        else:
            messagebox.showinfo("Continue", "No saved characters found. Please create a new game.")

    def new_game(self):
        # Example implementation: open character creation dialog
        self.create_character_dialog()

    def load_game(self):
        # Placeholder implementation for loading a game
        char_list = self.load_character_list()
        if char_list:
            # Let user select a character to load
            def on_select(character):
                self.character = character
                self.start_campaign_story()
            CharacterSelectGUI(self.root, char_list, on_select)
        else:
            messagebox.showinfo("Load Game", "No saved characters found. Please create a new game.")

    def show_loading_screen(self, message="Loading... Please wait", duration=1800):
        loading = tk.Toplevel(self.root)
        loading.title("Loading...")
        loading.geometry("420x260")
        loading.configure(bg="#181818")
        # Themed fonts/colors
        title_font = ("Georgia", 22, "bold")
        subtitle_font = ("Georgia", 12, "italic")
        label_fg = "#e0c080"
        # Title/logo
        tk.Label(loading, text="ARCANE ENGINE: ETERNAL QUEST", font=title_font, fg=label_fg, bg="#181818").pack(pady=(22,2))
        tk.Label(loading, text="by Shadow Studios", font=subtitle_font, fg="#b0a080", bg="#181818").pack()
        tk.Label(loading, text="Engine: Arcane Engine v1.0", font=("Georgia", 10, "italic"), fg="#b0a080", bg="#181818").pack(pady=(0,18))
        # Animated loading dots
        loading_var = tk.StringVar(value=message)
        label = tk.Label(loading, textvariable=loading_var, font=("Georgia", 13), fg="#fffbe6", bg="#181818")
        label.pack(pady=10)
        # Progress bar (simple animation)
        progress = tk.Canvas(loading, width=260, height=18, bg="#23201a", highlightthickness=0)
        progress.pack(pady=10)
        bar = progress.create_rectangle(2, 2, 2, 16, fill="#e0c080", width=0)
        # Animate progress bar and dots
        steps = 30
        interval = max(30, duration // steps)
        def animate(i=0):
            if i <= steps:
                progress.coords(bar, 2, 2, 2 + (256 * i // steps), 16)
                dots = '.' * ((i // 3) % 4)
                loading_var.set(f"{message}{dots}")
                loading.update_idletasks()
                loading.after(interval, lambda: animate(i+1))
            else:
                loading.destroy()
        animate()
        self.root.update()

    def create_menu(self):
        self.root.geometry("1024x640")
        self.root.title("Arcane Engine - Main Menu")
        self.root.configure(bg="#181818")
        # --- Add subtle vignette background image if available ---
        vignette_path = os.path.join(os.path.dirname(__file__), "vignette_bg.png")
        if os.path.exists(vignette_path):
            img = Image.open(vignette_path).resize((1024, 640), Image.LANCZOS)
            self._bg_img = ImageTk.PhotoImage(img)
            bg_label = tk.Label(self.root, image=self._bg_img, borderwidth=0)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        frame = tk.Frame(self.root, bg="#181818")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        # Title
        tk.Label(frame, text="ARCANE ENGINE", font=("Georgia", 36, "bold"), fg="#e0c080", bg="#181818").pack(pady=(30, 8))
        tk.Label(frame, text="Eternal Quest", font=("Georgia", 18, "italic"), fg="#b0a080", bg="#181818").pack(pady=(0, 24))
        # Menu buttons with icons
        menu_buttons = [
            ("New Game", self.new_game, "icon_newgame.png"),
            ("Continue", self.continue_game, "icon_continue.png"),
            ("Load Game", self.load_game, "icon_load.png"),
            ("Save Game", self.save_game, "icon_save.png"),
            ("Patch Notes", self.show_patch_notes, "icon_patch.png"),
            ("Character System", lambda: messagebox.showinfo("Character System", "Character system not implemented."), "icon_character.png"),
            ("Inventory System", self.launch_inventory, "icon_inventory.png"),
            ("Skills System", self.launch_skills, "icon_skills.png"),
            ("Quests System", self.launch_quests, "icon_quests.png"),
            # ("Map System", self.launch_map, "icon_map.png"),
            ("Social System", self.launch_social, "icon_social.png"),
            ("Settings", self.launch_settings, "icon_settings.png"),
            ("Game Credits", self.show_credits, "icon_credits.png"),
            ("Exit", self.root.quit, "icon_exit.png"),
            ("Help / Tutorial", lambda: show_help_window(self.root), "icon_help.png"),
            ("Season Mode", self.show_season_window, "icon_season.png"),
            ("Pit of Artificers", self.show_pit_window, "icon_pit.png"),
            ("Nightmare Dungeons", self.show_nightmare_window, "icon_nightmare.png"),
            ("Raids", self.launch_raids, "icon_raid.png"),
            ("Trials", self.launch_trials, "icon_trial.png"),
            ("Dungeons", self.launch_dungeons, "icon_dungeon.png"),
            ("Party Finder", self.launch_party_finder, "icon_party.png"),
            ("Dungeon Finder", self.launch_dungeon_finder, "icon_dungeonfinder.png"),
            ("Teleport", self.launch_teleport, "icon_teleport.png"),
            ("Codex (Legendary Items)", self.launch_codex, "icon_codex.png"),
        ]
        for text, cmd, icon in menu_buttons:
            btn = tk.Button(frame, text=text, width=24, height=2, command=cmd)
            style_button(btn, icon_path=os.path.join(os.path.dirname(__file__), icon))
            btn.pack(pady=4)
        # Footer
        tk.Label(frame, text="Inspired by Diablo 4, Last Epoch, and classic ARPGs.", font=("Georgia", 10, "italic"), fg="#b0a080", bg="#181818").pack(pady=(24, 8))

    def show_patch_notes(self):
        messagebox.showinfo("Patch Notes", "Patch Notes:\n\n- Initial release of Arcane Engine Main Menu.\n- Added character creation, campaign, and basic systems.\n- More features coming soon!")

    def show_credits(self):
        messagebox.showinfo("Game Credits", "Arcane Engine: Eternal Quest\n\nDeveloped by Shadow Studios\nInspired by Diablo 4, Last Epoch, and classic ARPGs.\n\nProgramming & Design: Shadow\nSpecial Thanks: The ARPG Community")

    def show_pit_window(self):
        win = tk.Toplevel(self.root)
        win.title("Pit of Artificers")
        self._style_submenu(win)
        pit = PitOfArtificers()
        tk.Label(win, text=pit.get_challenge()).pack(pady=5)
        tk.Label(win, text="Defeat the Artificer to earn masterwork materials!").pack(pady=5)
        tk.Button(win, text="Close", command=win.destroy).pack(pady=10)

    def show_nightmare_window(self):
        win = tk.Toplevel(self.root)
        win.title("Nightmare Dungeons")
        self._style_submenu(win)
        dungeons = self.nightmare_manager.list_dungeons()
        tk.Label(win, text="Available Nightmare Dungeons:").pack(pady=5)
        for dungeon in dungeons:
            tk.Label(win, text=f"{dungeon['name']} (Tier {dungeon['tier']})").pack(anchor='w')
        tk.Button(win, text="Close", command=win.destroy).pack(pady=10)

    def show_season_window(self):
        win = tk.Toplevel(self.root)
        win.title("Season Mode")
        self._style_submenu(win)
        current_season = self.season_manager.get_current_season()
        tk.Label(win, text=f"Current Season: {current_season['name']}").pack(pady=5)
        tk.Label(win, text=f"Season Number: {current_season['number']}").pack()
        tk.Label(win, text=f"Start: {current_season['start']}  End: {current_season['end']}").pack()
        tk.Label(win, text="Features: " + ", ".join(current_season.get('features', []))).pack(pady=5)
        tk.Button(win, text="Close", command=win.destroy).pack(pady=10)

    def launch_settings(self):
        win = tk.Toplevel(self.root)
        win.title("Settings")
        self._style_submenu(win)
        tk.Label(win, text="Settings (Demo)").pack(pady=5)
        tk.Label(win, text="Feature not implemented yet.").pack(pady=5)
        tk.Button(win, text="Close", command=win.destroy).pack(pady=10)

    # --- Submenu styling helper ---
    def _style_submenu(self, win):
        style_submenu(win)

    # Patch all submenus to use _style_submenu
    def launch_raids(self):
        win = tk.Toplevel(self.root)
        win.title("Raids")
        self._style_submenu(win)
        raids = self.raid_system.list_raids()
        tk.Label(win, text="Available Raids:").pack(pady=5)
        for raid in raids:
            tk.Label(win, text=raid['name']).pack(anchor='w')
        tk.Button(win, text="Close", command=win.destroy).pack(pady=5)

    def launch_trials(self):
        win = tk.Toplevel(self.root)
        win.title("Trials")
        self._style_submenu(win)
        trials = self.trial_system.list_trials()
        tk.Label(win, text="Available Trials:").pack(pady=5)
        for trial in trials:
            tk.Label(win, text=trial['name']).pack(anchor='w')
        tk.Button(win, text="Close", command=win.destroy).pack(pady=5)

    def launch_dungeons(self):
        win = tk.Toplevel(self.root)
        win.title("Dungeons")
        self._style_submenu(win)
        dungeons = self.dungeon_system.list_dungeons()
        tk.Label(win, text="Available Dungeons:").pack(pady=5)
        for dungeon in dungeons:
            tk.Label(win, text=dungeon['name']).pack(anchor='w')
        tk.Button(win, text="Close", command=win.destroy).pack(pady=5)

    def launch_party_finder(self):
        win = tk.Toplevel(self.root)
        win.title("Party Finder (LFG)")
        self._style_submenu(win)
        tk.Label(win, text="Join Party Finder for a Dungeon:").pack(pady=5)
        dungeons = self.dungeon_system.list_dungeons()
        dungeon_var = tk.StringVar(win)
        dungeon_var.set(dungeons[0]['name'] if dungeons else "")
        tk.OptionMenu(win, dungeon_var, *[d['name'] for d in dungeons]).pack(pady=5)
        name_entry = tk.Entry(win)
        name_entry.pack(pady=5)
        def join_lfg():
            player_name = name_entry.get().strip() or "You"
            dungeon_name = dungeon_var.get()
            self.party_finder.join_lfg(player_name, dungeon_name)
            messagebox.showinfo("LFG", f"{player_name} joined LFG for {dungeon_name}!")
        tk.Button(win, text="Join LFG", command=join_lfg).pack(pady=5)
        def form_parties():
            dungeon_name = dungeon_var.get()
            formed = self.party_finder.find_party(dungeon_name)
            if formed:
                msg = "\n".join([f"Party formed: {', '.join(p['members'])}" for p in formed])
                messagebox.showinfo("Party Formed", msg)
            else:
                messagebox.showinfo("Party Formed", "Not enough players to form a party yet.")
        tk.Button(win, text="Form Parties", command=form_parties).pack(pady=5)
        tk.Button(win, text="Close", command=win.destroy).pack(pady=5)

    def launch_dungeon_finder(self):
        win = tk.Toplevel(self.root)
        win.title("Dungeon Finder (LFD)")
        self._style_submenu(win)
        tk.Label(win, text="Queue for a Dungeon:").pack(pady=5)
        dungeons = self.dungeon_system.list_dungeons()
        dungeon_var = tk.StringVar(win)
        dungeon_var.set(dungeons[0]['name'] if dungeons else "")
        tk.OptionMenu(win, dungeon_var, *[d['name'] for d in dungeons]).pack(pady=5)
        name_entry = tk.Entry(win)
        name_entry.pack(pady=5)
        def join_lfd():
            player_name = name_entry.get().strip() or "You"
            dungeon_name = dungeon_var.get()
            self.dungeon_finder.join_lfd(player_name, dungeon_name)
            messagebox.showinfo("LFD", f"{player_name} joined Dungeon Finder for {dungeon_name}!")
        tk.Button(win, text="Join Dungeon Finder", command=join_lfd).pack(pady=5)
        def match_parties():
            dungeon_name = dungeon_var.get()
            formed = self.dungeon_finder.match_parties(dungeon_name)
            if formed:
                msg = "\n".join([f"Party formed: {', '.join(p['members'])} (Instance {p['instance_id']})" for p in formed])
                messagebox.showinfo("Dungeon Instance Created", msg)
            else:
                messagebox.showinfo("Dungeon Instance", "Not enough players to form a party yet.")
        tk.Button(win, text="Form Parties & Create Instance", command=match_parties).pack(pady=5)
        tk.Button(win, text="Close", command=win.destroy).pack(pady=5)

    def launch_teleport(self):
        if not self.teleport_system or not callable(getattr(self.teleport_system, 'teleport', None)):
            messagebox.showerror("Teleport", "World not initialized yet.")
            return
        win = tk.Toplevel(self.root)
        win.title("Teleport")
        self._style_submenu(win)
        tk.Label(win, text="Teleport to:").pack(pady=5)
        locs = self.teleport_system.get_teleport_locations()
        loc_var = tk.StringVar(win)
        loc_var.set(locs[0]['name'] if locs else "")
        tk.OptionMenu(win, loc_var, *[l['name'] for l in locs]).pack(pady=5)
        name_entry = tk.Entry(win)
        name_entry.pack(pady=5)
        def do_teleport():
            player = name_entry.get().strip() or "You"
            loc = loc_var.get()
            if self.teleport_system is not None and callable(getattr(self.teleport_system, 'teleport', None)):
                result = self.teleport_system.teleport(player, loc)
                messagebox.showinfo("Teleport", result)
            else:
                messagebox.showerror("Teleport", "Teleport system not available.")
        tk.Button(win, text="Teleport", command=do_teleport).pack(pady=5)
        tk.Button(win, text="Close", command=win.destroy).pack(pady=5)

    def launch_combat_menu(self):
        # Simple combat menu placeholder
        win = tk.Toplevel(self.root)
        win.title("Combat Menu")
        self._style_submenu(win)
        tk.Label(win, text="Combat System (Demo)").pack(pady=5)
        tk.Label(win, text="Feature not implemented yet.").pack(pady=5)
        tk.Button(win, text="Close", command=win.destroy).pack(pady=10)

    def launch_crafting_menu(self):
        # Simple crafting menu placeholder
        win = tk.Toplevel(self.root)
        win.title("Crafting Menu")
        self._style_submenu(win)
        tk.Label(win, text="Crafting System (Demo)").pack(pady=5)
        tk.Label(win, text="Feature not implemented yet.").pack(pady=5)
        tk.Button(win, text="Close", command=win.destroy).pack(pady=10)

    def launch_codex(self):
        win = tk.Toplevel(self.root)
        win.title("Codex (Legendary Items)")
        self._style_submenu(win)
        tk.Label(win, text="Legendary & Unique Items Codex").pack(pady=5)
        codex_frame = tk.Frame(win, bg="#181818")
        codex_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        for item in CODEX_ITEMS:
            item_str = f"{item['name']} ({item['type']}, {item['rarity']})\n" \
                       f"Stats: {', '.join(item['stats'])}\n" \
                       f"{item['description']}\n"
            tk.Label(codex_frame, text=item_str, anchor='w', justify='left').pack(anchor='w', pady=2)
        tk.Button(win, text="Close", command=win.destroy).pack(pady=10)

    # --- Update all submenus to use _style_submenu ---
    def launch_campaign_gameplay(self):
        if not self.character:
            messagebox.showerror("Error", "No character loaded.")
            return
        gameplay = tk.Toplevel(self.root)
        gameplay.title("Campaign Gameplay")
        self._style_submenu(gameplay)
        tk.Label(gameplay, text=f"{self.character['name']} the {self.character['class']} - {'Hardcore' if self.character.get('hardcore') else 'Normal'}").pack(pady=10)
        stats = self.character.get('stats', {}) if isinstance(self.character, dict) else {}
        stats_str = '\n'.join([f"{k}: {v}" for k, v in stats.items()]) if isinstance(stats, dict) and bool(stats) else 'No stats.'
        tk.Label(gameplay, text=f"Level: {self.character.get('level', 1)} | XP: {self.character.get('xp', 0)}").pack()
        tk.Label(gameplay, text=f"Stats:\n{stats_str}").pack()
        tk.Label(gameplay, text=f"Inventory: {len(self.character.get('inventory', []))} items").pack()
        tk.Label(gameplay, text=f"Quests: {len(self.character.get('quests', []))} active").pack()
        tk.Label(gameplay, text=f"Skills: {len(self.character.get('skills', []))} unlocked").pack()
        if not hasattr(self, 'game_world') or not self.game_world:
            self.create_game_world()
        zone = self.game_world['zone'] if self.game_world and isinstance(self.game_world, dict) and 'zone' in self.game_world else 'Unknown'
        tk.Label(gameplay, text=f"Current Zone: {zone}").pack(pady=5)
        world_tier = self.game_world['world_tier'] if self.game_world and isinstance(self.game_world, dict) and 'world_tier' in self.game_world else 1
        tk.Label(gameplay, text=f"World Tier: {world_tier}").pack()
        # --- Bottom action bar (Diablo 4 style) ---
        action_bar = tk.Frame(gameplay, bg="#181818")
        action_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        # Health orb
        health_canvas = tk.Canvas(action_bar, width=64, height=64, bg="#181818", highlightthickness=0)
        health_canvas.pack(side=tk.LEFT, padx=16)
        health_canvas.create_oval(4, 4, 60, 60, fill="#b4002a", outline="#e0c080", width=3)
        health_canvas.create_text(32, 32, text="HP", fill="#fffbe6", font=("Georgia", 12, "bold"))
        # Quick slots
        for i in range(5):
            slot = tk.Label(action_bar, text=f"{i+1}", width=4, height=2, bg="#23201a", fg="#e0c080", font=("Georgia", 14, "bold"), relief=tk.RIDGE, borderwidth=2)
            slot.pack(side=tk.LEFT, padx=6)
        # Mana orb
        mana_canvas = tk.Canvas(action_bar, width=64, height=64, bg="#181818", highlightthickness=0)
        mana_canvas.pack(side=tk.RIGHT, padx=16)
        mana_canvas.create_oval(4, 4, 60, 60, fill="#2a3ab4", outline="#e0c080", width=3)
        mana_canvas.create_text(32, 32, text="MP", fill="#fffbe6", font=("Georgia", 12, "bold"))

    def create_character_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Create New Character")
        self._style_submenu(dialog)
        tk.Label(dialog, text="Enter Character Name:").grid(row=0, column=0, sticky="e")
        name_entry = tk.Entry(dialog)
        name_entry.grid(row=0, column=1)
        tk.Label(dialog, text="Select Class:").grid(row=1, column=0, sticky="e")
        class_var = tk.StringVar(dialog)
        class_var.set("Barbarian")
        class_options = ["Barbarian", "Sorcerer", "Druid", "Rogue", "Necromancer"]
        class_menu = tk.OptionMenu(dialog, class_var, *class_options)
        class_menu.grid(row=1, column=1)
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
            new_char = {
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
            char_list = self.load_character_list()
            if len(char_list) < 12:
                char_list.append(new_char)
                self.save_character_list(char_list)
                self.character = new_char
                self.game_stats['characters_created'] += 1
                dialog.destroy()
                self.start_campaign_story()
            else:
                messagebox.showerror("Error", "All 12 character slots are full. Delete a character to create a new one.")
        tk.Button(dialog, text="Create", command=confirm).grid(row=3, column=0, columnspan=2, pady=10)

# ... existing code ...
class StartMenu:
    def __init__(self, root, on_start):
        self.root = root
        self.on_start = on_start
        self._bg_img = None
        self._draw_ui()

    def _draw_ui(self):
        self.root.geometry("1024x640")
        self.root.title("Arcane Engine - Start Menu")
        self.root.configure(bg="#181818")
        # Optional: background vignette
        vignette_path = os.path.join(os.path.dirname(__file__), "vignette_bg.png")
        if os.path.exists(vignette_path):
            img = Image.open(vignette_path).resize((1024, 640), Image.LANCZOS)
            self._bg_img = ImageTk.PhotoImage(img)
            bg_label = tk.Label(self.root, image=self._bg_img, borderwidth=0)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        frame = tk.Frame(self.root, bg="#181818")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        tk.Label(frame, text="ARCANE ENGINE", font=("Georgia", 44, "bold"), fg="#e0c080", bg="#181818").pack(pady=(60, 10))
        tk.Label(frame, text="Eternal Quest", font=("Georgia", 20, "italic"), fg="#b0a080", bg="#181818").pack(pady=(0, 30))
        tk.Label(frame, text="by Shadow Studios", font=("Georgia", 14, "italic"), fg="#b0a080", bg="#181818").pack(pady=(0, 30))
        start_btn = tk.Button(frame, text="Start", width=18, height=2, command=self.on_start)
        style_button(start_btn, icon_path=os.path.join(os.path.dirname(__file__), "icon_start.png"))
        start_btn.pack(pady=16)
        tk.Label(frame, text="Inspired by Diablo 4, Last Epoch, and classic ARPGs.", font=("Georgia", 10, "italic"), fg="#b0a080", bg="#181818").pack(pady=(40, 8))

# --- Helper for Diablo 4-style button styling ---
def style_button(btn, icon_path=None):
    btn.config(
        font=("Georgia", 14, "bold"),
        bg="#23201a",
        fg="#e0c080",
        activebackground="#40351a",
        activeforeground="#fffbe6",
        relief=tk.FLAT,
        bd=0,
        cursor="hand2",
        highlightthickness=0,
        padx=8,
        pady=4,
        compound=tk.LEFT if icon_path else None
    )
    if icon_path and os.path.exists(icon_path):
        img = Image.open(icon_path).resize((28, 28), Image.LANCZOS)
        btn._icon = ImageTk.PhotoImage(img)
        btn.config(image=btn._icon)

# --- Helper for Diablo 4-style submenu window styling ---
def style_submenu(win):
    win.configure(bg="#181818")
    for widget in win.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(bg="#181818", fg="#e0c080", font=("Georgia", 13))
        elif isinstance(widget, tk.Button):
            style_button(widget)
        elif isinstance(widget, tk.Entry):
            widget.config(bg="#23201a", fg="#e0c080", insertbackground="#e0c080", font=("Georgia", 12))
        elif isinstance(widget, tk.OptionMenu):
            widget.config(bg="#23201a", fg="#e0c080", font=("Georgia", 12))
        elif isinstance(widget, tk.Listbox):
            widget.config(bg="#23201a", fg="#e0c080", selectbackground="#40351a", selectforeground="#fffbe6", font=("Georgia", 12))

# === CHARACTER CREATION, SELECTION, AND GAMEPLAY ===
# Character selection GUI
class CharacterSelectGUI:
    def __init__(self, root, character_list, on_select):
        self.root = tk.Toplevel(root)
        self.root.title("Select Your Character")
        self.character_list = character_list
        self.on_select = on_select
        self.selected_idx = None
        self.buttons = []
        self._draw_slots()
        tk.Button(self.root, text="Confirm Selection", command=self._confirm).pack(pady=8)
        tk.Button(self.root, text="Cancel", command=self.root.destroy).pack(pady=2)
    def _draw_slots(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)
        for i in range(12):
            char = self.character_list[i] if i < len(self.character_list) else None
            btn_text = char['name'] if char else f"Empty Slot {i+1}"
            btn = tk.Button(frame, text=btn_text, width=18, height=2,
                            command=lambda idx=i: self._select(idx))
            btn.grid(row=i//4, column=i%4, padx=5, pady=5)
            self.buttons.append(btn)
    def _select(self, idx):
        self.selected_idx = idx
        for i, btn in enumerate(self.buttons):
            btn.config(relief=tk.SUNKEN if i == idx else tk.RAISED)
    def _confirm(self):
        if self.selected_idx is not None and self.selected_idx < len(self.character_list):
            self.on_select(self.character_list[self.selected_idx])
            self.root.destroy()
        else:
            messagebox.showinfo("Select Character", "Please select a valid character slot.")

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

# === SKILLS AND PASSIVES DATA (Diablo  4 & Last Epoch inspired) ===

# Example skills for each class (expand as needed)
DIABLO4_SKILLS = {
    'Barbarian': [
        {'name': 'Bash', 'desc': 'Bash enemies with your weapon.'},
        {'name': 'Hammer of the Ancients', 'desc': 'Smash the ground with a mighty hammer.'},
        {'name': 'Whirlwind', 'desc': 'Spin and deal damage to nearby enemies.'},
        {'name': 'Rend', 'desc': 'Bleed enemies in front of you.'},
        {'name': 'Iron Skin', 'desc': 'Gain a barrier that absorbs damage.'},
        {'name': 'Wrath of the Berserker', 'desc': 'Enter a berserk rage, increasing damage.'},
    ],
    'Sorcerer': [
        {'name': 'Fire Bolt', 'desc': 'Hurl a bolt of fire.'},
        {'name': 'Frost Nova', 'desc': 'Freeze nearby enemies.'},
        {'name': 'Chain Lightning', 'desc': 'Zap enemies with lightning.'},
        {'name': 'Ice Shards', 'desc': 'Launch shards of ice.'},
        {'name': 'Teleport', 'desc': 'Blink to a new location.'},
        {'name': 'Inferno', 'desc': 'Summon a fiery serpent.'},
    ],
    'Druid': [
        {'name': 'Earth Spike', 'desc': 'Erupt the ground beneath enemies.'},
        {'name': 'Storm Strike', 'desc': 'Strike with lightning.'},
        {'name': 'Shred', 'desc': 'Transform into a werewolf and slash.'},

        {'name': 'Landslide', 'desc': 'Crush enemies with earth.'},
        {'name': 'Hurricane', 'desc': 'Summon a storm around you.'},
        {'name': 'Grizzly Rage', 'desc': 'Transform into a werebear.'},
    ],
    'Rogue': [
        {'name': 'Puncture', 'desc': 'Throw blades that slow enemies.'},
        {'name': 'Flurry', 'desc': 'Stab rapidly in front of you.'},
        {'name': 'Penetrating Shot', 'desc': 'Fire a powerful arrow.'},
        {'name': 'Shadow Step', 'desc': 'Dash through shadows.'},
        {'name': 'Rain of Arrows', 'desc': 'Barrage an area with arrows.'},
        {'name': 'Death Trap', 'desc': 'Set a deadly trap.'},
    ],
    'Necromancer': [
        {'name': 'Bone Splinters', 'desc': 'Fire bone projectiles.'},
        {'name': 'Sever', 'desc': 'Cleave with a scythe.'},
        {'name': 'Blood Surge', 'desc': 'Drain life from enemies.'},
        {'name': 'Corpse Explosion', 'desc': 'Explode corpses.'},
        {'name': 'Bone Prison', 'desc': 'Trap enemies in bone.'},
        {'name': 'Army of the Dead', 'desc': 'Summon a skeletal army.'},
    ],
    'Sentinel': [
        {'name': 'Rive', 'desc': 'Slash enemies with your weapon.'},
        {'name': 'Vengeance', 'desc': 'Counterattack enemies.'},
        {'name': 'Lunge', 'desc': 'Dash to an enemy.'},
        {'name': 'Warpath', 'desc': 'Spin and deal damage.'},
        {'name': 'Smite', 'desc': 'Call down a bolt of holy power.'},
    ],
    'Mage': [
        {'name': 'Elemental Nova', 'desc': 'Blast enemies with elemental energy.'},
        {'name': 'Fireball', 'desc': 'Launch a fireball.'},
        {'name': 'Teleport', 'desc': 'Instantly move to a new location.'},
        {'name': 'Lightning Blast', 'desc': 'Zap enemies with lightning.'},
        {'name': 'Glacier', 'desc': 'Summon a glacier to crush enemies.'},
    ],
}

LAST_EPOCH_SKILLS = {
    'Sentinel': [
        {'name': 'Rive', 'desc': 'Slash enemies with your weapon.'},
        {'name': 'Vengeance', 'desc': 'Counterattack enemies.'},
        {'name': 'Lunge', 'desc': 'Dash to an enemy.'},
        {'name': 'Warpath', 'desc': 'Spin and deal damage.'},
        {'name': 'Smite', 'desc': 'Call down a bolt of holy power.'},
    ],
    'Mage': [
        {'name': 'Elemental Nova', 'desc': 'Blast enemies with elemental energy.'},
        {'name': 'Fireball', 'desc': 'Launch a fireball.'},
        {'name': 'Teleport', 'desc': 'Instantly move to a new location.'},
        {'name': 'Lightning Blast', 'desc': 'Zap enemies with lightning.'},
        {'name': 'Glacier', 'desc': 'Summon a glacier to crush enemies.'},
    ],
    # ...add more classes as needed...
}

# Example passives (Diablo 4 & Last Epoch inspired)
DIABLO4_PASSIVES = [
    {'name': 'Unbridled Rage', 'effect': 'Increase Fury generation.'},
    {'name': 'Devastation', 'effect': 'Increase maximum resource.'},
    {'name': 'Imposing Presence', 'effect': 'Increase maximum life.'},
    {'name': 'Tough as Nails', 'effect': 'Increase armor.'},
    {'name': 'Quick Impulses', 'effect': 'Increase movement speed.'},
    {'name': 'Resilience', 'effect': 'Reduce damage taken.'},
]

LAST_EPOCH_PASSIVES = [
    {'name': 'Juggernaut', 'effect': 'Gain armor per point.'},
    {'name': 'Time and Faith', 'effect': 'Gain health on hit.'},
    {'name': 'Arcane Insight', 'effect': 'Increase spell damage.'},
    {'name': 'Swift Recovery', 'effect': 'Increase health regen.'},
    {'name': 'Elemental Affinity', 'effect': 'Increase elemental resistances.'},
]

# === SKILL TREE AND PASSIVE TREE EXAMPLES ===

def build_example_skill_tree():
    tree = SkillTree()
    # Add nodes (example for Barbarian)
    tree.add_node(SkillNode('Bash', 'Bash enemies with your weapon.', required_points=1))
    tree.add_node(SkillNode('Hammer of the Ancients', 'Smash the ground with a mighty hammer.', required_points=2))
    tree.add_node(SkillNode('Whirlwind', 'Spin and deal damage to nearby enemies.', required_points=3))
    # ...add more nodes and dependencies as needed...
    tree.points = 5  # Example: 5 skill points to spend
    return tree

def build_example_passives_tree():
    tree = PassivesTree()
    tree.add_node(PassiveNode('Unbridled Rage', 'Increase Fury generation.', required_points=1))
    tree.add_node(PassiveNode('Devastation', 'Increase maximum resource.', required_points=2))
    tree.add_node(PassiveNode('Imposing Presence', 'Increase maximum life.', required_points=2))
    # ...add more nodes and dependencies as needed...
    tree.points = 4  # Example: 4 passive points to spend
    return tree

# Example usage (can be used in character creation or skills system)
EXAMPLE_SKILL_TREE = build_example_skill_tree()
EXAMPLE_PASSIVES_TREE = build_example_passives_tree()

# === MONSTERS, CREATURES, ANIMALS DATA (Diablo 4 inspired) ===

MONSTERS = [
    {'name': 'Fallen', 'type': 'Demon', 'level': 1, 'hp': 20, 'attack': 5},
    {'name': 'Skeleton', 'type': 'Undead', 'level': 2, 'hp': 25, 'attack': 7},
    {'name': 'Goatman', 'type': 'Beastman', 'level': 3, 'hp': 30, 'attack': 9},
    {'name': 'Drowned', 'type': 'Undead', 'level': 4, 'hp': 35, 'attack': 11},
    {'name': 'Wraith', 'type': 'Ghost', 'level': 5, 'hp': 28, 'attack': 13},
    {'name': 'Vampire', 'type': 'Demon', 'level': 6, 'hp': 40, 'attack': 15},
    {'name': 'Succubus', 'type': 'Demon', 'level': 7, 'hp': 32, 'attack': 14},
    {'name': 'Butcher', 'type': 'Boss', 'level': 10, 'hp': 120, 'attack': 30},
]

CREATURES = [
    {'name': 'Dire Wolf', 'type': 'Beast', 'level': 2, 'hp': 22, 'attack': 6},
    {'name': 'Giant Spider', 'type': 'Beast', 'level': 3, 'hp': 18, 'attack': 8},
    {'name': 'Swamp Toad', 'type': 'Beast', 'level': 1, 'hp': 10, 'attack': 3},
    {'name': 'Carrion Bat', 'type': 'Beast', 'level': 2, 'hp': 12, 'attack': 4},
    {'name': 'Razorback Boar', 'type': 'Beast', 'level': 4, 'hp': 28, 'attack': 10},
]

ANIMALS = [
    {'name': 'Deer', 'type': 'Animal', 'level': 1, 'hp': 8, 'attack': 0},
    {'name': 'Rabbit', 'type': 'Animal', 'level': 1, 'hp': 4, 'attack': 0},
    {'name': 'Bear', 'type': 'Animal', 'level': 5, 'hp': 50, 'attack': 18},
    {'name': 'Wolf', 'type': 'Animal', 'level': 2, 'hp': 14, 'attack': 5},
    {'name': 'Hawk', 'type': 'Animal', 'level': 1, 'hp': 6, 'attack': 2},
]

# === BASIC ENEMY AI SYSTEM ===

class EnemyAI:
    STATES = ['idle', 'patrol', 'chase', 'attack', 'flee']
    def __init__(self, enemy, patrol_points=None):
        self.enemy = enemy
        self.state = 'idle'
        self.patrol_points = patrol_points or []
        self.current_patrol_index = 0
        self.position = getattr(enemy, 'position', (0, 0))
    def update(self, player_pos):
        # Simple AI: chase if close, patrol otherwise
        if self._distance_to(player_pos) < 5:
            self.state = 'chase'
        elif self.patrol_points:
            self.state = 'patrol'
        else:
            self.state = 'idle'
    def _distance_to(self, pos):
        ex, ey = self.position
        px, py = pos
        return ((ex - px) ** 2 + (ey - py) ** 2) ** 0.5
    def _patrol(self):
        if not self.patrol_points:
            return
        self.current_patrol_index = (self.current_patrol_index + 1) % len(self.patrol_points)
        self.position = self.patrol_points[self.current_patrol_index]
    def act(self):
        if self.state == 'patrol':
            self._patrol()
        elif self.state == 'chase':
            # Move towards player (not implemented)
            pass
        elif self.state == 'attack':
            # Attack logic (not implemented)
            pass
        elif self.state == 'flee':
            # Flee logic (not implemented)
            pass
        # else idle

# === LOOT RARITIES, CLASSES, TYPES (define before use) ===
LOOT_RARITIES = [
    {'name': 'Common', 'color': '#bbb', 'weight': 60},
   
    {'name': 'Magic', 'color': '#4b8cff', 'weight': 25},
    {'name': 'Rare', 'color': '#ffe14b', 'weight': 10},
    {'name': 'Legendary', 'color': '#ff7f27', 'weight': 4},
    {'name': 'Unique', 'color': '#b400ff', 'weight': 1},
]

LOOT_CLASSES = [
    'Barbarian', 'Sorcerer', 'Druid', 'Rogue', 'Necromancer',
    'Sentinel', 'Mage', 'Primalist', 'Acolyte', 'Marksman'
]

LOOT_TYPES = [
    'Weapon', 'Armor', 'Amulet', 'Ring', 'Relic', 'Potion', 'Offhand', 'Helmet', 'Boots', 'Gloves', 'Belt', 'Shield',
    'Handheld', 'Sword', 'Bladed', 'Ranged', 'Exotic'
]

# === ARCHETYPES (Character Classes) ===
ARCHETYPES = [
    {
        'name': 'Barbarian',
        'desc': 'A brutal melee warrior with immense strength.',
        'starting_stats': {'Strength': 10, 'Dexterity': 5, 'Intelligence': 2, 'Vitality': 8},
        'special': 'Berserker Rage',
    },
    {
        'name': 'Sorcerer',
        'desc': 'A master of elemental magic.',
        'starting_stats': {'Strength': 2, 'Dexterity': 5, 'Intelligence': 12, 'Vitality': 6},
        'special': 'Elemental Mastery',
    },
    {
        'name': 'Druid',
        'desc': 'A shapeshifter who commands nature.',
        'starting_stats': {'Strength': 6, 'Dexterity': 6, 'Intelligence': 7, 'Vitality': 8},
        'special': 'Shapeshift',
    },
    {
        'name': 'Rogue',
        'desc': 'A swift and deadly assassin.',
        'starting_stats': {'Strength': 4, 'Dexterity': 12, 'Intelligence': 4, 'Vitality': 6},
        'special': 'Shadowstep',
    },
    {
        'name': 'Necromancer',
        'desc': 'A summoner of the dead.',
        'starting_stats': {'Strength': 3, 'Dexterity': 4, 'Intelligence': 11, 'Vitality': 7},
        'special': 'Raise Skeletons',
    },
    # ...add more archetypes as needed...
]

# === BOSSES ===
BOSSES = [
    {'name': 'The Butcher', 'level': 10, 'hp': 1200, 'attack': 90, 'special': 'Charge, Cleaver Slam'},
    {'name': 'Lilith', 'level': 30, 'hp': 3500, 'attack': 180, 'special': 'Blood Nova, Seduction'},
    {'name': 'Duriel', 'level': 25, 'hp': 2800, 'attack': 150, 'special': 'Poison Swarm, Burrow'},
    {'name': 'The Artificer', 'level': 20, 'hp': 2000, 'attack': 120, 'special': 'Summon Constructs, Arcane Blast'},
    # ...add more bosses as needed...
]

# === WEAPONS ===
WEAPONS = [
    {'name': 'Iron Sword', 'type': 'Sword', 'damage': 12, 'class': ['Barbarian', 'Sentinel'], 'rarity': 'Common'},
    {'name': 'Ancient Staff', 'type': 'Staff', 'damage': 9, 'class': ['Sorcerer', 'Mage', 'Necromancer'], 'rarity': 'Magic'},
    {'name': 'Wolf Bow', 'type': 'Bow', 'damage': 11, 'class': ['Rogue', 'Marksman'], 'rarity': 'Rare'},
    {'name': 'Bear Claws', 'type': 'Claws', 'damage': 10, 'class': ['Druid'], 'rarity': 'Magic'},
    {'name': 'Shadow Dagger', 'type': 'Dagger', 'damage': 8, 'class': ['Rogue', 'Acolyte'], 'rarity': 'Legendary'},
    {'name': 'Blood Scythe', 'type': 'Scythe', 'damage': 15, 'class': ['Necromancer'], 'rarity': 'Unique'},
    # ...add more weapons as needed...
]

# === ARMORS ===
ARMORS = [
    {'name': 'Leather Armor', 'type': 'Chest', 'defense': 8, 'class': ['Rogue', 'Druid'], 'rarity': 'Common'},
    {'name': 'Plate Mail', 'type': 'Chest', 'defense': 15, 'class': ['Barbarian', 'Sentinel'], 'rarity': 'Rare'},
    {'name': 'Mystic Robe', 'type': 'Chest', 'defense': 6, 'class': ['Sorcerer', 'Mage', 'Necromancer'], 'rarity': 'Magic'},
    {'name': 'Wolf Pelt', 'type': 'Helmet', 'defense': 5, 'class': ['Druid'], 'rarity': 'Magic'},
    {'name': 'Shadow Hood', 'type': 'Helmet', 'defense': 4, 'class': ['Rogue', 'Acolyte'], 'rarity': 'Legendary'},
    {'name': 'Bone Shield', 'type': 'Shield', 'defense': 10, 'class': ['Necromancer', 'Sentinel'], 'rarity': 'Unique'},
    # ...add more armors as needed...
]

# === CODEX: WEAPONS, ARMOR, AND LEGENDARY ITEMS ===
CODEX_ITEMS = [
    {
        'name': "The Grandfather",
        'type': "Sword",
        'rarity': "Unique",
        'stats': ['+Damage', '+Max Life', '+All Stats'],
        'description': "A legendary blade said to outlast its wielder."
    },
    {
        'name': "Harlequin Crest",
        'type': "Helmet",
        'rarity': "Unique",
        'stats': ['+All Stats', '+Cooldown Reduction', '+Damage Reduction'],
        'description': "A mysterious helm that grants wisdom and resilience."
    },
    {
        'name': "Doombringer",
        'type': "Sword",
        'rarity': "Unique",
        'stats': ['+Shadow Damage', '+Lucky Hit', '+Max Life'],
        'description': "A cursed blade that brings doom to its foes."
    },
    {
        'name': "Andariel's Visage",
        'type': "Helmet",
        'rarity': "Unique",
        'stats': ['+Poison Damage', '+Attack Speed', '+Life Steal'],
        'description': "The demonic mask of the Maiden of Anguish."
    },
    {
        'name': "Tyrael's Might",
        'type': "Armor",
        'rarity': "Unique",
        'stats': ['+All Resistances', '+Movement Speed', '+Damage to Demons'],
        'description': "Heavenly armor once worn by the Archangel Tyrael."
    },
    {
        'name': "Stormshield",
        'type': "Shield",
        'rarity': "Legendary",
        'stats': ['+Block Chance', '+Damage Reduction', '+Lightning Resist'],
        'description': "A shield that crackles with the power of storms."
    },
    {
        'name': "Windforce",
        'type': "Bow",
        'rarity': "Legendary",
        'stats': ['+Attack Speed', '+Knockback', '+Critical Hit Chance'],
        'description': "A bow that fires with the force of a hurricane."
    },
    {
        'name': "Death's Web",
        'type': "Wand",
        'rarity': "Legendary",
        'stats': ['+Poison Damage', '+Life Leech', '+Curse Power'],
        'description': "A wand woven with the power of death and decay."
    },
    {
        'name': "Stone of Jordan",
        'type': "Ring",
        'rarity': "Legendary",
        'stats': ['+Skill Levels', '+Mana', '+Elemental Damage'],
        'description': "A ring coveted by mages for its arcane power."
    },
    {
        'name': "Frostburn",
        'type': "Gloves",
        'rarity': "Legendary",
        'stats': ['+Cold Damage', '+Mana', '+Freeze Chance'],
        'description': "Gloves that chill the air and freeze the soul."
    },
    {
        'name': "Thunderfury, Blessed Blade of the Windseeker",
        'type': "Sword",
        'rarity': "Legendary",
        'stats': ['+Lightning Damage', '+Chain Lightning Proc', '+Attack Speed'],
        'description': "A blade that calls down the fury of the storm."
    },
    {
        'name': "Bloodraven's Charge",
        'type': "Bow",
        'rarity': "Legendary",
        'stats': ['+Summon Power', '+Attack Speed', '+Poison Damage'],
        'description': "A bow once wielded by the fallen ranger Bloodraven."
    },
    {
        'name': "Arkaine's Valor",
        'type': "Armor",
        'rarity': "Legendary",
        'stats': ['+Life', '+Damage Reduction', '+Skill Cooldown'],
        'description': "Armor that inspires valor in its wearer."
    },
    {
        'name': "Raven Frost",
        'type': "Ring",
        'rarity': "Legendary",
        'stats': ['+Cold Resist', '+Cannot Be Frozen', '+Dexterity'],
        'description': "A ring that protects against the harshest cold."
    },
    {
        'name': "Dracul's Grasp",
        'type': "Gloves",
        'rarity': "Legendary",
        'stats': ['+Life Leech', '+Open Wounds', '+Strength'],
        'description': "Gloves that thirst for the blood of enemies."
    },
    {
        'name': "Crown of Ages",
        'type': "Helmet",
        'rarity': "Legendary",
        'stats': ['+All Resistances', '+Damage Reduction', '+Sockets'],
        'description': "A crown worn by ancient kings and heroes."
    },
    # ...add more codex items as needed...
]

# Dummy/fallback definitions for missing constants and classes to prevent NameError
GEAR_PREFIXES = [{'name': 'Mighty', 'effect': '+5 Strength'}, {'name': 'Arcane', 'effect': '+5 Intelligence'}]
GEAR_SUFFIXES = [{'name': 'of Power', 'effect': '+10 Damage'}, {'name': 'of the Bear', 'effect': '+10 Vitality'}]
LOOT_TABLE = [{'item': 'Iron Sword', 'type': 'Weapon'}, {'item': 'Ancient Staff', 'type': 'Weapon'}, {'item': 'Leather Armor', 'type': 'Armor'}, {'item': 'Ring of Power', 'type': 'Accessory'}]
class SeasonManager:
    def __init__(self):
        self.seasons = [{'number': 1, 'name': 'Season of Shadows', 'start': '2025-01-01', 'end': '2025-03-31', 'features': ['New Quests', 'Unique Items']}]
        self.current = 0
    def get_current_season(self):
        return self.seasons[self.current]
   
    def set_season(self, n):
        self.current = max(0, min(n-1, len(self.seasons)-1))
    def list_seasons(self):
        return self.seasons
class NightmareDungeonManager:
    class Dungeon:
        def __init__(self, name, tier=1):
            self.name = name
            self.tier = tier
        def get_difficulty(self):
            return 'Nightmare'
        def complete(self):
            pass
        def get_rewards(self):
            return {'gold': 100, 'xp': 500, 'glyphs': 1}
    def __init__(self):
        self.dungeons = [self.Dungeon('Shadow Crypt', 1), self.Dungeon('Frost Cavern', 2)]
    def list_dungeons(self):
        # Return a list of dicts with name and tier for GUI display
        return [{'name': d.name, 'tier': d.tier} for d in self.dungeons]
    def get_dungeon(self, idx):
        return self.dungeons[idx] if 0 <= idx < len(self.dungeons) else None
    def get_nightmare_dungeons(self):
        # Return the actual Dungeon objects
        return self.dungeons
    def run_dungeon(self, dungeon):
        # Simulate running a dungeon and returning a result string
        rewards = dungeon.get_rewards()
        return f"Completed {dungeon.name}! Rewards: Gold {rewards['gold']}, XP {rewards['xp']}, Glyphs {rewards['glyphs']}"
class PitOfArtificers:
    def __init__(self, tier=1):
        self.tier = tier
    def get_challenge(self):
        return f"Pit of Artificers Tier {self.tier}: Defeat the Artificer!"
    def complete(self):
        pass
    def get_rewards(self):
        return {'gold': 200, 'xp': 1000, 'masterwork_materials': 3}
def show_help_window(root):
    messagebox.showinfo("Help / Tutorial", "Welcome to Arcane Engine! Use the menu to explore features.")

if __name__ == "__main__":
    gui = MainMenuGUI()
    gui.run()