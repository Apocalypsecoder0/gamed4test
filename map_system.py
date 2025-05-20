import tkinter as tk
from tkinter import messagebox
from typing import List, Dict, Optional, Tuple

class MapRegion:
    def __init__(self, name: str, region_type: str, coords: Tuple[int, int, int, int], color: str, parent: Optional[str] = None):
        self.name = name
        self.region_type = region_type  # e.g., 'continent', 'country', 'kingdom', 'town', 'zone'
        self.coords = coords  # (x1, y1, x2, y2) rectangle for simplicity
        self.color = color
        self.parent = parent

class MapSystem:
    def __init__(self):
        self.regions: Dict[str, MapRegion] = {}
        self.current_location: Optional[str] = None
        self._init_default_world()

    def _init_default_world(self):
        # Example world structure (expand as needed)
        self.add_region('Sanctuary', 'continent', (20, 20, 380, 280), '#b0c4de')
        self.add_region('Fractured Peaks', 'country', (60, 60, 180, 180), '#e0e0e0', parent='Sanctuary')
        self.add_region('Kyovashad', 'town', (100, 100, 130, 130), '#c0a060', parent='Fractured Peaks')
        self.add_region('Hawezar', 'country', (200, 150, 350, 250), '#a0cfa0', parent='Sanctuary')
        self.add_region('Zarbinzet', 'town', (250, 200, 280, 230), '#c0a0c0', parent='Hawezar')
        self.set_current_location('Kyovashad')

    def add_region(self, name: str, region_type: str, coords: Tuple[int, int, int, int], color: str, parent: Optional[str] = None):
        self.regions[name] = MapRegion(name, region_type, coords, color, parent)

    def set_current_location(self, name: str):
        if name in self.regions:
            self.current_location = name

    def list_regions(self, region_type: Optional[str] = None) -> List[str]:
        if region_type:
            return [r.name for r in self.regions.values() if r.region_type == region_type]
        return list(self.regions.keys())

    def get_region(self, name: str) -> Optional[MapRegion]:
        return self.regions.get(name)

class MapSystemGUI:
    def __init__(self, map_system: MapSystem):
        self.map_system = map_system
        self.root = tk.Tk()
        self.root.title("Arcane Engine - World Map")
        self.canvas = tk.Canvas(self.root, width=400, height=300, bg='#222')
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        self.info_label = tk.Label(self.root, text="", width=40, anchor='w', justify='left')
        self.info_label.pack(padx=10, pady=5)
        self.legend = tk.Label(self.root, text=self._legend_text(), anchor='w', justify='left')
        self.legend.pack(padx=10, pady=5)
        self._draw_map()
        self.canvas.bind('<Motion>', self._on_hover)
        self.canvas.bind('<Button-1>', self._on_left_click)
        self.canvas.bind('<Button-3>', self._on_right_click)
        self.hovered_region = None

    def _legend_text(self):
        return "Legend:\nContinent: Blue\nCountry: Gray/Green\nTown: Gold/Purple"

    def _draw_map(self):
        self.canvas.delete('all')
        for region in self.map_system.regions.values():
            x1, y1, x2, y2 = region.coords
            outline = 'yellow' if region.name == self.map_system.current_location else 'black'
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=region.color, outline=outline, width=2)
            self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text=region.name, fill='black')

    def _find_region_at(self, x, y) -> Optional[MapRegion]:
        for region in self.map_system.regions.values():
            x1, y1, x2, y2 = region.coords
            if x1 <= x <= x2 and y1 <= y <= y2:
                return region
        return None

    def _on_hover(self, event):
        region = self._find_region_at(event.x, event.y)
        if region:
            info = f"{region.name} ({region.region_type.capitalize()})"
            if region.parent:
                info += f"\nParent: {region.parent}"
            if region.name == self.map_system.current_location:
                info += "\n(Current Location)"
            self.info_label.config(text=info)
            self.hovered_region = region
        else:
            self.info_label.config(text="")
            self.hovered_region = None

    def _on_left_click(self, event):
        region = self._find_region_at(event.x, event.y)
        if region:
            info = f"You are viewing {region.name} ({region.region_type})"
            if region.parent:
                info += f"\nParent: {region.parent}"
            messagebox.showinfo("Region Info", info)

    def _on_right_click(self, event):
        region = self._find_region_at(event.x, event.y)
        if region and region.region_type in ('town', 'kingdom', 'country'):
            self.map_system.set_current_location(region.name)
            self._draw_map()
            self.info_label.config(text=f"Traveled to {region.name}!")
        elif region:
            self.info_label.config(text=f"Cannot travel directly to {region.name}.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    map_system = MapSystem()
    gui = MapSystemGUI(map_system)
    gui.run()
