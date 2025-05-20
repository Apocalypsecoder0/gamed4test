import tkinter as tk
from tkinter import messagebox
from typing import List, Dict, Optional
from game_assets import GAME_SETTINGS, KEYBOARD_BINDINGS, MOUSE_SETTINGS, CONTROLLER_BINDINGS

class SettingsSystem:
    def __init__(self):
        # Initialize with all available settings from GAME_SETTINGS
        self.settings = {}
        for category, options in GAME_SETTINGS.items():
            for key, value in options.items():
                # Use the first option if value is a list, else the value itself
                self.settings[key] = value[0] if isinstance(value, list) else value
        # Add input bindings
        self.keyboard_bindings = KEYBOARD_BINDINGS.copy()
        self.mouse_settings = MOUSE_SETTINGS.copy()
        self.controller_bindings = CONTROLLER_BINDINGS.copy()

    def set_setting(self, key: str, value):
        self.settings[key] = value

    def get_setting(self, key: str):
        return self.settings.get(key)

    def list_settings(self):
        return self.settings.items()

    def set_keyboard_binding(self, action: str, key: str):
        self.keyboard_bindings[action] = key

    def get_keyboard_binding(self, action: str):
        return self.keyboard_bindings.get(action, "")

    def set_mouse_setting(self, setting: str, value):
        self.mouse_settings[setting] = value

    def get_mouse_setting(self, setting: str):
        return self.mouse_settings.get(setting, None)

    def set_controller_binding(self, action: str, button: str):
        self.controller_bindings[action] = button

    def get_controller_binding(self, action: str):
        return self.controller_bindings.get(action, "")

class SettingsSystemGUI:
    def __init__(self, settings_system: SettingsSystem):
        self.settings_system = settings_system
        self.root = tk.Tk()
        self.root.title("Settings Menu")
        self.entries = {}
        row = 0
        # General settings
        for key, value in self.settings_system.list_settings():
            tk.Label(self.root, text=key+":").grid(row=row, column=0, sticky="e")
            entry = tk.Entry(self.root)
            entry.insert(0, str(value))
            entry.grid(row=row, column=1)
            self.entries[key] = entry
            row += 1
        # Keyboard bindings
        tk.Label(self.root, text="Keyboard Bindings:", font=("Arial", 10, "bold")).grid(row=row, column=0, columnspan=2, pady=(10,0))
        row += 1
        self.kb_entries = {}
        for action, key in self.settings_system.keyboard_bindings.items():
            tk.Label(self.root, text=action+":").grid(row=row, column=0, sticky="e")
            entry = tk.Entry(self.root)
            entry.insert(0, str(key))
            entry.grid(row=row, column=1)
            self.kb_entries[action] = entry
            row += 1
        # Mouse settings
        tk.Label(self.root, text="Mouse Settings:", font=("Arial", 10, "bold")).grid(row=row, column=0, columnspan=2, pady=(10,0))
        row += 1
        self.mouse_entries = {}
        for setting, value in self.settings_system.mouse_settings.items():
            tk.Label(self.root, text=setting+":").grid(row=row, column=0, sticky="e")
            entry = tk.Entry(self.root)
            entry.insert(0, str(value))
            entry.grid(row=row, column=1)
            self.mouse_entries[setting] = entry
            row += 1
        # Controller bindings
        tk.Label(self.root, text="Controller Bindings:", font=("Arial", 10, "bold")).grid(row=row, column=0, columnspan=2, pady=(10,0))
        row += 1
        self.controller_entries = {}
        for action, button in self.settings_system.controller_bindings.items():
            tk.Label(self.root, text=action+":").grid(row=row, column=0, sticky="e")
            entry = tk.Entry(self.root)
            entry.insert(0, str(button))
            entry.grid(row=row, column=1)
            self.controller_entries[action] = entry
            row += 1
        tk.Button(self.root, text="Save", command=self.save).grid(row=row, column=0, columnspan=2, pady=10)

    def save(self):
        for key, entry in self.entries.items():
            value = entry.get()
            self.settings_system.set_setting(key, value)
        for action, entry in self.kb_entries.items():
            self.settings_system.set_keyboard_binding(action, entry.get())
        for setting, entry in self.mouse_entries.items():
            val = entry.get()
            # Try to convert to float or bool if possible
            if val.lower() in ["true", "false"]:
                val = val.lower() == "true"
            else:
                try:
                    val = float(val)
                except ValueError:
                    pass
            self.settings_system.set_mouse_setting(setting, val)
        for action, entry in self.controller_entries.items():
            self.settings_system.set_controller_binding(action, entry.get())
        messagebox.showinfo("Settings", "Settings saved!")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    settings_system = SettingsSystem()
    gui = SettingsSystemGUI(settings_system)
    gui.run()
