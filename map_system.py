import tkinter as tk
from tkinter import messagebox
from typing import List, Dict, Optional

class MapSystem:
    def __init__(self):
        self.locations: List[str] = []
        self.current_location: Optional[str] = None

    def add_location(self, name: str):
        self.locations.append(name)

    def set_current_location(self, name: str):
        if name in self.locations:
            self.current_location = name

    def list_locations(self) -> List[str]:
        return self.locations

class MapSystemGUI:
    def __init__(self, map_system: MapSystem):
        self.map_system = map_system
        self.root = tk.Tk()
        self.root.title("Map Menu")
        self.listbox = tk.Listbox(self.root, width=40)
        self.listbox.pack(padx=10, pady=10)
        self.set_button = tk.Button(self.root, text="Set as Current", command=self.set_current)
        self.set_button.pack(pady=5)
        self.refresh_button = tk.Button(self.root, text="Refresh", command=self.refresh_list)
        self.refresh_button.pack(pady=5)
        self.refresh_list()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for loc in self.map_system.list_locations():
            marker = " (Current)" if loc == self.map_system.current_location else ""
            self.listbox.insert(tk.END, loc + marker)

    def set_current(self):
        selection = self.listbox.curselection()
        if selection:
            idx = selection[0]
            name = self.map_system.list_locations()[idx]
            self.map_system.set_current_location(name)
            self.refresh_list()
        else:
            messagebox.showinfo("Info", "No location selected.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    map_system = MapSystem()
    map_system.add_location("Kyovashad")
    map_system.add_location("Fractured Peaks")
    map_system.add_location("Hawezar")
    map_system.set_current_location("Kyovashad")
    gui = MapSystemGUI(map_system)
    gui.run()
