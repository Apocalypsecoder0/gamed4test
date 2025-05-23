import random
import time
import os
import pickle
import sys
import importlib.util
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

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

# === MAIN MENU GUI ===
class MainMenuGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Arcane Engine Main Menu")
        self.character = None  # Store the current character
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
        self.teleport_system = None  # Will be set after world creation
        self.show_loading_screen()
        self.create_menu()

    def show_loading_screen(self):
        loading = tk.Toplevel(self.root)
        loading.title("Loading...")
        loading.geometry("400x250")
        tk.Label(loading, text="ARCANE ENGINE: ETERNAL QUEST", font=("Arial", 20, "bold"), fg="#B22222").pack(pady=20)
        tk.Label(loading, text="by Shadow Studios", font=("Arial", 12)).pack(pady=5)
        tk.Label(loading, text="Engine: Arcane Engine v1.0", font=("Arial", 10, "italic")).pack(pady=5)
        tk.Label(loading, text="Loading... Please wait", font=("Arial", 12)).pack(pady=30)
        self.root.update()
        self.root.after(1800, loading.destroy)

    def create_menu(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        tk.Label(frame, text="ARCANE ENGINE: ETERNAL QUEST", font=("Arial", 18, "bold"), fg="#B22222").pack(pady=5)
        tk.Label(frame, text="by Shadow Studios", font=("Arial", 10)).pack()
        tk.Label(frame, text="Engine: Arcane Engine v1.0", font=("Arial", 9, "italic")).pack(pady=2)
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
        # Fix line 41: add missing methods if not present
        if not hasattr(self, 'launch_social'):
            self.launch_social = lambda: messagebox.showinfo("Social System", "Social system not implemented.")
        if not hasattr(self, 'launch_settings'):
            self.launch_settings = lambda: messagebox.showinfo("Settings", "Settings system not implemented.")
        tk.Button(frame, text="Social System", width=30, command=self.launch_social).pack(pady=5)
        tk.Button(frame, text="Settings", width=30, command=self.launch_settings).pack(pady=5)
        tk.Button(frame, text="Game Credits", width=30, command=self.show_credits).pack(pady=5)
        tk.Button(frame, text="Exit", width=30, command=self.root.quit).pack(pady=20)
        tk.Button(frame, text="Help / Tutorial", command=lambda: show_help_window(self.root)).pack(pady=3)
        tk.Button(frame, text="Season Mode", command=self.show_season_window).pack(pady=3)
        tk.Button(frame, text="Pit of Artificers", command=self.show_pit_window).pack(pady=3)
        tk.Button(frame, text="Nightmare Dungeons", command=self.show_nightmare_window).pack(pady=3)
        tk.Button(frame, text="Character Select", command=self.launch_character_select).pack(pady=3)
        tk.Button(frame, text="Raids", width=30, command=self.launch_raids).pack(pady=3)
        tk.Button(frame, text="Trials", width=30, command=self.launch_trials).pack(pady=3)
        tk.Button(frame, text="Dungeons", width=30, command=self.launch_dungeons).pack(pady=3)
        tk.Button(frame, text="Party Finder", width=30, command=self.launch_party_finder).pack(pady=3)
        tk.Button(frame, text="Dungeon Finder", width=30, command=self.launch_dungeon_finder).pack(pady=3)
        tk.Button(frame, text="Teleport", width=30, command=self.launch_teleport).pack(pady=3)

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

    def load_character_list(self):
        # Load up to 12 characters from a save file
        try:
            if os.path.exists('characters.d4save'):
                with open('characters.d4save', 'rb') as f:
                    char_list = pickle.load(f)
                return char_list[:12]
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load character list: {e}")
        return []

    def save_character_list(self, char_list):
        try:
            with open('characters.d4save', 'wb') as f:
                pickle.dump(char_list, f)
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save character list: {e}")

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
        if not hasattr(self, 'character') or self.character is None:
            messagebox.showinfo("Continue", "No saved character found. Please start a new game.")
            return
        if not isinstance(self.character, dict):
            messagebox.showerror("Continue", "Character data is invalid.")
            return
        # Show full stats and launch gameplay
        stats = self.character.get('stats', {}) if isinstance(self.character, dict) else {}
        stats_str = '\n'.join([f"{k}: {v}" for k, v in stats.items()]) if isinstance(stats, dict) and bool(stats) else 'No stats.'
        info = (
            f"Continuing your adventure as {self.character.get('name', 'Unknown')} the {self.character.get('class', 'Unknown')}!\n"
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
        stats = self.character.get('stats', {}) if isinstance(self.character, dict) else {}
        stats_str = '\n'.join([f"{k}: {v}" for k, v in stats.items()]) if isinstance(stats, dict) and bool(stats) else 'No stats.'
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
        tk.Button(gameplay, text="Combat Menu", command=self.launch_combat_menu).pack(pady=2)
        tk.Button(gameplay, text="Crafting Menu", command=self.launch_crafting_menu).pack(pady=2)
        tk.Button(gameplay, text="Exit to Main Menu", command=gameplay.destroy).pack(pady=10)

    def create_game_world(self):
        # Create a new game world after new game
        # Generate a world seed for reproducibility
        self.world_seed = int(time.time() * 1000) ^ random.randint(0, 2**32-1)
        random.seed(self.world_seed)
        # Define a grid-based world map (10x10 for example)
        self.world_map = {}
        # Expanded world geography: continents, countries, kingdoms, zones
        continents = [
            {'name': 'Sanctuary', 'type': 'Continent', 'x': 0, 'y': 0},
            {'name': 'Westmarch Isles', 'type': 'Continent', 'x': 9, 'y': 9}
        ]
        countries = [
            {'name': 'Kehjistan', 'type': 'Country', 'x': 3, 'y': 1},
            {'name': 'Scosglen', 'type': 'Country', 'x': 1, 'y': 8},
            {'name': 'Hawezar', 'type': 'Country', 'x': 5, 'y': 5},
            {'name': 'Fractured Peaks', 'type': 'Country', 'x': 2, 'y': 7}
        ]
        kingdoms = [
            {'name': 'Kyovashad', 'type': 'Kingdom', 'x': 2, 'y': 7},
            {'name': 'Caldeum', 'type': 'Kingdom', 'x': 3, 'y': 1},
            {'name': 'Westmarch', 'type': 'Kingdom', 'x': 9, 'y': 9}
        ]
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
        # Fill the world map grid with all locations
        for c in continents:
            self.world_map[(c['x'], c['y'])] = c
        for c in countries:
            self.world_map[(c['x'], c['y'])] = c
        for k in kingdoms:
            self.world_map[(k['x'], k['y'])] = k
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
            'world_map': self.world_map,
            'continents': [c['name'] for c in continents],
            'countries': [c['name'] for c in countries],
            'kingdoms': [k['name'] for k in kingdoms],
            'towns': [t['name'] for t in towns],
            'zones': [z['name'] for z in zones],
        }
        self.teleport_system = TeleportSystem(self.world_map)

    def load_game(self):
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
        if character_system and hasattr(character_system, 'CharacterSystem') and hasattr(character_system, 'CharacterSystemGUI'):
            char_system = character_system.CharacterSystem()
            gui = character_system.CharacterSystemGUI(char_system)
            gui.run()
        else:
            messagebox.showerror("Error", "Character system module not found or incomplete.")

    def launch_inventory(self):
        mod_name = 'inventory'
        mod_path = 'inventory.py'
        try:
            spec = importlib.util.spec_from_file_location(mod_name, mod_path)
            if spec and spec.loader:
                inv_mod = importlib.util.module_from_spec(spec)
                sys.modules[mod_name] = inv_mod
                spec.loader.exec_module(inv_mod)
                inv = inv_mod.Inventory()
                inv.add_item(inv_mod.Item("Sword of Doom", "Weapon", "Legendary", {"Damage": 100}, (2,1)))
                inv.add_item(inv_mod.Item("Iron Helm", "Armor", "Rare", {"Armor": 20}, (2,2)))
                inv.add_item(inv_mod.Item("Health Potion", "Potion", "Common", {"Heal": 50}, (1,1)))
                inv_mod.InventoryGUI(inv).run()
            else:
                messagebox.showerror("Error", "Could not load Inventory module.")
        except Exception as e:
            messagebox.showerror("Error", f"Inventory system error: {e}")

    def launch_skills(self):
        if skills_system:
            skills_system.SkillsSystemGUI(skills_system.SkillsSystem()).run()
        else:
            messagebox.showerror("Error", "Skills system module not found.")

    def launch_quests(self):
        if quests_system:
            quests_system.QuestsSystemGUI(quests_system.QuestsSystem()).run()
        else:
            messagebox.showerror("Error", "Quests system module not found.")

    def launch_map(self):
        # Show a world map with continents, countries, kingdoms, towns, and zones on a grid, with interactivity
        map_win = tk.Toplevel(self.root)
        map_win.title("World Map")
        canvas = tk.Canvas(map_win, width=400, height=400, bg="#222")
        canvas.pack()
        grid_size = 10
        cell = 40
        location_tags = {}
        # Draw grid
        for i in range(grid_size+1):
            canvas.create_line(cell, cell+i*cell, cell+grid_size*cell, cell+i*cell, fill="#444")
            canvas.create_line(cell+i*cell, cell, cell+i*cell, cell+grid_size*cell, fill="#444")
        # Draw all locations with different colors and shapes, and add interactivity
        for (x, y), loc in self.game_world['world_map'].items():
            tag = f"loc_{x}_{y}"
            if loc['type'] == 'Continent':
                canvas.create_rectangle(cell+x*cell-16, cell+y*cell-16, cell+x*cell+16, cell+y*cell+16, outline="#FFD700", width=3, tags=tag)
                canvas.create_text(cell+x*cell, cell+y*cell-22, text=loc['name'], fill="#FFD700", font=("Arial", 9, "bold"), tags=tag)
            elif loc['type'] == 'Country':
                canvas.create_oval(cell+x*cell-14, cell+y*cell-14, cell+x*cell+14, cell+y*cell+14, outline="#00BFFF", width=2, tags=tag)
                canvas.create_text(cell+x*cell, cell+y*cell-18, text=loc['name'], fill="#00BFFF", font=("Arial", 8, "bold"), tags=tag)
            elif loc['type'] == 'Kingdom':
                canvas.create_oval(cell+x*cell-12, cell+y*cell-12, cell+x*cell+12, cell+y*cell+12, outline="#FF69B4", width=2, tags=tag)
                canvas.create_text(cell+x*cell, cell+y*cell-15, text=loc['name'], fill="#FF69B4", font=("Arial", 8, "bold"), tags=tag)
            elif loc['type'] == 'City':
                canvas.create_oval(cell+x*cell-10, cell+y*cell-10, cell+x*cell+10, cell+y*cell+10, fill="#FFD700", tags=tag)
                canvas.create_text(cell+x*cell, cell+y*cell-13, text=loc['name'], fill="#FFD700", font=("Arial", 8, "bold"), tags=tag)
            elif loc['type'] == 'Town':
                canvas.create_oval(cell+x*cell-8, cell+y*cell-8, cell+x*cell+8, cell+y*cell+8, fill="#00FF00", tags=tag)
                canvas.create_text(cell+x*cell, cell+y*cell-11, text=loc['name'], fill="#00FF00", font=("Arial", 7), tags=tag)
            elif loc['type'] == 'Wilderness':
                canvas.create_rectangle(cell+x*cell-7, cell+y*cell-7, cell+x*cell+7, cell+y*cell+7, fill="#8B4513", tags=tag)
                canvas.create_text(cell+x*cell, cell+y*cell-10, text=loc['name'], fill="#8B4513", font=("Arial", 7), tags=tag)
            elif loc['type'] == 'Ruins':
                canvas.create_rectangle(cell+x*cell-7, cell+y*cell-7, cell+x*cell+7, cell+y*cell+7, fill="#A9A9A9", tags=tag)
                canvas.create_text(cell+x*cell, cell+y*cell-10, text=loc['name'], fill="#A9A9A9", font=("Arial", 7), tags=tag)
            location_tags[tag] = loc
        # Show current location
        zx, zy = self.game_world.get('zone_coords', (2, 7))
        canvas.create_rectangle(cell+zx*cell-14, cell+zy*cell-14, cell+zx*cell+14, cell+zy*cell+14, outline="#00BFFF", width=2)
        # Show world seed and legend
        tk.Label(map_win, text=f"World Seed: {self.game_world.get('world_seed')}").pack()
        legend = tk.Label(map_win, text="Legend: Continent=Gold Square, Country=Blue Circle, Kingdom=Pink Circle, City=Gold, Town=Green, Wilderness=Brown, Ruins=Gray", fg="#fff", bg="#222")
        legend.pack()
        # Show lists of continents, countries, kingdoms, towns, zones
        geo_frame = tk.Frame(map_win, bg="#222")
        geo_frame.pack(pady=4)
        for label, key in [("Continents", 'continents'), ("Countries", 'countries'), ("Kingdoms", 'kingdoms'), ("Towns", 'towns'), ("Zones", 'zones')]:
            tk.Label(geo_frame, text=f"{label}: {', '.join(self.game_world.get(key, []))}", fg="#fff", bg="#222", font=("Arial", 8)).pack(anchor='w')
        # Interactivity: show info on click
        def on_location_click(event):
            x, y = (event.x - cell) // cell, (event.y - cell) // cell
            for tag, loc in location_tags.items():
                bbox = canvas.bbox(tag)
                if bbox and bbox[0] <= event.x <= bbox[2] and bbox[1] <= event.y <= bbox[3]:
                    info = f"{loc['type']}: {loc['name']}\nCoords: ({loc['x']},{loc['y']})"
                    messagebox.showinfo("Location Info", info)
                    return
        canvas.bind("<Button-1>", on_location_click)
        # Advanced: allow travel to towns/cities/kingdoms
        def travel_to_location(loc):
            if loc['type'] in ['Town', 'City', 'Kingdom']:
                self.game_world['zone'] = loc['name']
                self.game_world['zone_coords'] = (loc['x'], loc['y'])
                messagebox.showinfo("Travel", f"You have traveled to {loc['name']}!")
                map_win.destroy()
        def on_right_click(event):
            x, y = (event.x - cell) // cell, (event.y - cell) // cell
            for tag, loc in location_tags.items():
                bbox = canvas.bbox(tag)
                if bbox and bbox[0] <= event.x <= bbox[2] and bbox[1] <= event.y <= bbox[3]:
                    travel_to_location(loc)
                    return
        canvas.bind("<Button-3>", on_right_click)

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
            "Engine: Arcane Engine v1.0\n"
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

    def launch_combat_menu(self):
        # Diablo 4-style combat menu GUI for attacks, spells, health/mana, buffs/debuffs
        combat = tk.Toplevel(self.root)
        combat.title("Combat Menu")
        combat.geometry("420x340")
        # Health and Mana Pools
        char = self.character or {'name': 'Hero', 'class': 'Barbarian', 'level': 1, 'stats': {}}
        hp = char.get('stats', {}).get('hp', 100)
        mana = char.get('stats', {}).get('mana', 50)
        max_hp = char.get('stats', {}).get('max_hp', 100)
        max_mana = char.get('stats', {}).get('max_mana', 50)
        tk.Label(combat, text=f"{char['name']} the {char['class']} (Lv{char.get('level', 1)})", font=("Arial", 13, "bold")).pack(pady=5)
        hp_var = tk.IntVar(value=hp)
        mana_var = tk.IntVar(value=mana)
        tk.Label(combat, text="Health:").pack()
        hp_bar = tk.Scale(combat, from_=0, to=max_hp, orient='horizontal', variable=hp_var, length=200, fg='red', troughcolor='#800')
        hp_bar.pack()
        tk.Label(combat, text="Mana:").pack()
        mana_bar = tk.Scale(combat, from_=0, to=max_mana, orient='horizontal', variable=mana_var, length=200, fg='blue', troughcolor='#00f')
        mana_bar.pack()
        # Buffs and Debuffs
        buffs = char.get('stats', {}).get('buffs', [])
        debuffs = char.get('stats', {}).get('debuffs', [])
        tk.Label(combat, text="Buffs:").pack()
        tk.Label(combat, text=", ".join(buffs) if buffs else "None", fg="#0a0").pack()
        tk.Label(combat, text="Debuffs:").pack()
        tk.Label(combat, text=", ".join(debuffs) if debuffs else "None", fg="#a00").pack()
        # Attack and Spell Buttons
        tk.Label(combat, text="Combat Actions:", font=("Arial", 11, "bold")).pack(pady=5)
        actions_frame = tk.Frame(combat)
        actions_frame.pack()
        # Example: show up to 4 skills/spells from character
        skills = char.get('skills', [])
        if not skills:
            # Fallback: use default skills for class if available
            if 'class' in char and char['class'] in DIABLO4_SKILLS:
                skills = DIABLO4_SKILLS[char['class']]
            else:
                skills = []
        for i, skill in enumerate(skills[:4]):
            skill_name = skill['name'] if isinstance(skill, dict) and 'name' in skill else str(skill)
            tk.Button(actions_frame, text=skill_name, width=18, command=lambda s=skill: messagebox.showinfo("Skill", f"You use {s['name']}!" if isinstance(s, dict) and 'name' in s else f"You use {s}"), bg="#222", fg="#fff").grid(row=0, column=i, padx=3, pady=2)
        # Basic Attack
        tk.Button(actions_frame, text="Basic Attack", width=18, command=lambda: messagebox.showinfo("Attack", "You attack the enemy!"), bg="#444", fg="#fff").grid(row=1, column=0, padx=3, pady=2)
        # Close button
        tk.Button(combat, text="Close", command=combat.destroy).pack(pady=10)

    def launch_crafting_menu(self):
        crafting = tk.Toplevel(self.root)
        crafting.title("Crafting Menu")
        crafting.geometry("400x350")
        if not hasattr(self, 'crafting_system') or self.crafting_system is None:
            self.crafting_system = CraftingSystem()
        cs = self.crafting_system
        tk.Label(crafting, text="Available Materials:", font=("Arial", 11, "bold")).pack(pady=5)
        mats_str = '\n'.join([f"{k}: {v}" for k, v in cs.get_materials().items()])
        mats_label = tk.Label(crafting, text=mats_str)
        mats_label.pack()
        tk.Label(crafting, text="Craftable Items:", font=("Arial", 11, "bold")).pack(pady=5)
        recipes = cs.get_recipes()
        recipe_var = tk.StringVar(crafting)
        recipe_var.set(recipes[0] if recipes else "")
        tk.OptionMenu(crafting, recipe_var, *recipes).pack(pady=5)
        def do_craft():
            recipe = recipe_var.get()
            if not recipe:
                messagebox.showerror("Crafting", "No recipe selected.")
                return
            if not cs.can_craft(recipe):
                messagebox.showerror("Crafting", "Not enough materials to craft this item.")
                return
            item = cs.craft(recipe)
            if item:
                messagebox.showinfo("Crafting", f"Crafted: {item['name']}\nPrefix: {item['prefix']}\nSuffix: {item['suffix']}")
                mats_label.config(text='\n'.join([f"{k}: {v}" for k, v in cs.get_materials().items()]))
            else:
                messagebox.showerror("Crafting", "Crafting failed.")
        tk.Button(crafting, text="Craft Item", command=do_craft).pack(pady=8)
        tk.Button(crafting, text="Close", command=crafting.destroy).pack(pady=8)

    def show_season_window(self):
        win = tk.Toplevel(self.root)
        win.title("Season Mode")
        tk.Label(win, text="Season Mode", font=("Arial", 14, "bold")).pack(pady=8)
        tk.Label(win, text=f"Current Season: {self.season_manager.get_current_season()}").pack(pady=4)
        for i in range(1, 5):
            tk.Button(win, text=f"Set Season {i}", command=lambda n=i: self._set_season_and_refresh(win, n)).pack(pady=2)
        tk.Button(win, text="Close", command=win.destroy).pack(pady=8)

    def _set_season_and_refresh(self, win, number):
        self.season_manager.set_season(number)
        messagebox.showinfo("Season Mode", f"Season set to {number}!")
        win.destroy()
        self.show_season_window()

    def show_nightmare_window(self):
        win = tk.Toplevel(self.root)
        win.title("Nightmare Dungeons")
        tk.Label(win, text="Nightmare Dungeons", font=("Arial", 14, "bold")).pack(pady=8)
        dungeons = self.nightmare_manager.list_dungeons()
        for idx, dungeon in enumerate(dungeons):
            tk.Button(win, text=f"{dungeon['name']} (Tier {dungeon['tier']})", command=lambda i=idx: self._run_nightmare_dungeon(win, i)).pack(pady=2)
        tk.Button(win, text="Close", command=win.destroy).pack(pady=8)

    def _run_nightmare_dungeon(self, win, idx):
        dungeons = self.nightmare_manager.get_nightmare_dungeons()
        if 0 <= idx < len(dungeons):
            dungeon = dungeons[idx]
            result = self.nightmare_manager.run_dungeon(dungeon)
            messagebox.showinfo("Nightmare Dungeon", result)
        else:
            messagebox.showerror("Nightmare Dungeon", "Invalid dungeon selection.")
        win.destroy()

    def show_pit_window(self):
        win = tk.Toplevel(self.root)
        win.title("Pit of Artificers")
        tk.Label(win, text="Pit of Artificers", font=("Arial", 14, "bold")).pack(pady=8)
        tk.Label(win, text="(Feature coming soon!)").pack(pady=8)
        tk.Button(win, text="Close", command=win.destroy).pack(pady=8)

    def launch_character_select(self):
        char_list = self.load_character_list()
        if not char_list:
            messagebox.showinfo("Character Select", "No saved characters found. Create a new character first.")
            return
        CharacterSelectGUI(self.root, char_list, self._set_active_character)

    def _set_active_character(self, character):
        self.character = character
        # Optionally save the last selected character index
        messagebox.showinfo("Character Selected", f"You selected: {character['name']}")

    def launch_raids(self):
        win = tk.Toplevel(self.root)
        win.title("Raids")
        raids = self.raid_system.list_raids()
        tk.Label(win, text="Available Raids:", font=("Arial", 12, "bold")).pack(pady=5)
        for raid in raids:
            tk.Label(win, text=f"{raid['name']} (Lv{raid['level']}) - Boss: {raid['boss']} | Party: {raid['min_party']}-{raid['max_party']}").pack(anchor='w')
        tk.Button(win, text="Close", command=win.destroy).pack(pady=5)

    def launch_trials(self):
        win = tk.Toplevel(self.root)
        win.title("Trials")
        trials = self.trial_system.list_trials()
        tk.Label(win, text="Available Trials:", font=("Arial", 12, "bold")).pack(pady=5)
        for trial in trials:
            tk.Label(win, text=f"{trial['name']} (Lv{trial['level']}) - {trial['type']}").pack(anchor='w')
        tk.Button(win, text="Close", command=win.destroy).pack(pady=5)

    def launch_dungeons(self):
        win = tk.Toplevel(self.root)
        win.title("Dungeons")
        dungeons = self.dungeon_system.list_dungeons()
        tk.Label(win, text="Available Dungeons:", font=("Arial", 12, "bold")).pack(pady=5)
        for dungeon in dungeons:
            tk.Label(win, text=f"{dungeon['name']} (Lv{dungeon['level']}) - Boss: {dungeon['boss']}").pack(anchor='w')
        tk.Button(win, text="Close", command=win.destroy).pack(pady=5)

    def launch_party_finder(self):
        win = tk.Toplevel(self.root)
        win.title("Party Finder (LFG)")
        tk.Label(win, text="Join Party Finder for a Dungeon:", font=("Arial", 12, "bold")).pack(pady=5)
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
        tk.Label(win, text="Queue for a Dungeon:", font=("Arial", 12, "bold")).pack(pady=5)
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
        tk.Label(win, text="Teleport to:", font=("Arial", 12, "bold")).pack(pady=5)
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

# === GEAR PREFIXES, SUFFIXES, AND LOOT TABLES (Diablo 4 & Last Epoch inspired) ===

GEAR_PREFIXES = [
    {'name': 'Fiery', 'effect': '+Fire Damage'},
    {'name': 'Icy', 'effect': '+Cold Damage'},
    {'name': 'Shocking', 'effect': '+Lightning Damage'},
    {'name': 'Vampiric', 'effect': 'Life Leech'},
    {'name': 'Stalwart', 'effect': '+Armor'},
    {'name': 'Swift', 'effect': '+Attack Speed'},
    {'name': 'Deadly', 'effect': '+Critical Strike Chance'},
    {'name': 'Resilient', 'effect': '+All Resistances'},
    {'name': 'Frenzied', 'effect': '+Frenzy on Hit'},
    {'name': 'Ancient', 'effect': '+Max Life'},
]

GEAR_SUFFIXES = [
    {'name': 'of the Bear', 'effect': '+Strength'},
    {'name': 'of the Eagle', 'effect': '+Dexterity'},
    {'name': 'of the Sage', 'effect': '+Intelligence'},
    {'name': 'of the Fox', 'effect': '+Evasion'},
    {'name': 'of the Leech', 'effect': 'Life Leech'},
    {'name': 'of the Fortress', 'effect': '+Block Chance'},
    {'name': 'of the Avalanche', 'effect': '+Cold Resistance'},
    {'name': 'of the Inferno', 'effect': '+Fire Resistance'},
    {'name': 'of the Storm', 'effect': '+Lightning Resistance'},
    {'name': 'of the Titan', 'effect': '+Max Health'},
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