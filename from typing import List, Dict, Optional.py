from typing import List, Dict, Optional
import tkinter as tk
from tkinter import messagebox

# diablo4_inventory.py


class Item:
    def __init__(self, name: str, item_type: str, rarity: str, stats: Dict[str, int], size: tuple = (1,1)):
        self.name = name
        self.item_type = item_type  # e.g., 'Weapon', 'Armor', 'Potion'
        self.rarity = rarity        # e.g., 'Common', 'Rare', 'Legendary'
        self.stats = stats
        self.size = size            # (width, height) for grid placement

    def __repr__(self):
        return f"{self.rarity} {self.name} ({self.item_type}) {self.stats}"

class Inventory:
    def __init__(self, width: int = 10, height: int = 4):
        self.width = width
        self.height = height
        self.grid: List[List[Optional[Item]]] = [[None for _ in range(width)] for _ in range(height)]
        self.items: List[Item] = []

    def can_place(self, item: Item, x: int, y: int) -> bool:
        for dx in range(item.size[0]):
            for dy in range(item.size[1]):
                if x+dx >= self.width or y+dy >= self.height:
                    return False
                if self.grid[y+dy][x+dx] is not None:
                    return False
        return True

    def add_item(self, item: Item) -> bool:
        for y in range(self.height):
            for x in range(self.width):
                if self.can_place(item, x, y):
                    for dx in range(item.size[0]):
                        for dy in range(item.size[1]):
                            self.grid[y+dy][x+dx] = item
                    self.items.append(item)
                    return True
        return False

    def remove_item(self, item: Item) -> bool:
        if item in self.items:
            for y in range(self.height):
                for x in range(self.width):
                    if self.grid[y][x] == item:
                        self.grid[y][x] = None
            self.items.remove(item)
            return True
        return False

    def list_items(self) -> List[Item]:
        return self.items

    def find_item(self, name: str) -> Optional[Item]:
        for item in self.items:
            if item.name == name:
                return item
        return None

    def sort_items(self, key: str = "rarity"):
        self.items.sort(key=lambda item: getattr(item, key))

    def display(self):
        for row in self.grid:
            print(" | ".join([item.name[:2] if item else "  " for item in row]))

class InventoryGUI:
    def __init__(self, inventory: Inventory):
        self.inventory = inventory
        self.root = tk.Tk()
        self.root.title("Inventory GUI")
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(padx=10, pady=10)
        self.refresh_button = tk.Button(self.root, text="Refresh", command=self.display_grid)
        self.refresh_button.pack(pady=5)
        self.items_listbox = tk.Listbox(self.root, width=40)
        self.items_listbox.pack(padx=10, pady=10)
        self.display_grid()
        self.display_items()

    def display_grid(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        for y, row in enumerate(self.inventory.grid):
            for x, item in enumerate(row):
                name = item.name[:2] if item else "  "
                label = tk.Label(self.grid_frame, text=name, width=4, height=2, borderwidth=1, relief="solid")
                label.grid(row=y, column=x, padx=1, pady=1)
        self.display_items()

    def display_items(self):
        self.items_listbox.delete(0, tk.END)
        for item in self.inventory.items:
            self.items_listbox.insert(tk.END, str(item))

    def run(self):
        self.root.mainloop()

# Example usage:
if __name__ == "__main__":
    inv = Inventory()
    sword = Item("Sword of Doom", "Weapon", "Legendary", {"Damage": 100}, (2,1))
    helm = Item("Iron Helm", "Armor", "Rare", {"Armor": 20}, (2,2))
    potion = Item("Health Potion", "Potion", "Common", {"Heal": 50}, (1,1))

    inv.add_item(sword)
    inv.add_item(helm)
    inv.add_item(potion)

    inv.display()
    print(inv.list_items())

    # Launch GUI
    gui = InventoryGUI(inv)
    gui.run()