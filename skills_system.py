import tkinter as tk
from tkinter import messagebox
from typing import List, Dict, Optional

class SkillsSystem:
    def __init__(self):
        self.skills: Dict[str, int] = {}

    def add_skill(self, name: str, level: int = 1):
        self.skills[name] = level

    def remove_skill(self, name: str):
        if name in self.skills:
            del self.skills[name]

    def list_skills(self) -> Dict[str, int]:
        return self.skills

class SkillsSystemGUI:
    def __init__(self, skills_system: SkillsSystem):
        self.skills_system = skills_system
        self.root = tk.Tk()
        self.root.title("Skills Menu")
        self.listbox = tk.Listbox(self.root, width=40)
        self.listbox.pack(padx=10, pady=10)
        self.add_button = tk.Button(self.root, text="Add Skill", command=self.add_skill_window)
        self.add_button.pack(pady=5)
        self.remove_button = tk.Button(self.root, text="Remove Selected", command=self.remove_selected)
        self.remove_button.pack(pady=5)
        self.refresh_button = tk.Button(self.root, text="Refresh", command=self.refresh_list)
        self.refresh_button.pack(pady=5)
        self.refresh_list()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for name, level in self.skills_system.list_skills().items():
            self.listbox.insert(tk.END, f"{name} (Level {level})")

    def add_skill_window(self):
        win = tk.Toplevel(self.root)
        win.title("Add Skill")
        tk.Label(win, text="Skill Name:").grid(row=0, column=0)
        name_entry = tk.Entry(win)
        name_entry.grid(row=0, column=1)
        tk.Label(win, text="Level:").grid(row=1, column=0)
        level_entry = tk.Entry(win)
        level_entry.grid(row=1, column=1)
        def submit():
            name = name_entry.get()
            try:
                level = int(level_entry.get())
            except ValueError:
                level = 1
            if name:
                self.skills_system.add_skill(name, level)
                self.refresh_list()
                win.destroy()
            else:
                messagebox.showerror("Error", "Skill name required.")
        tk.Button(win, text="Add", command=submit).grid(row=2, column=0, columnspan=2)

    def remove_selected(self):
        selection = self.listbox.curselection()
        if selection:
            idx = selection[0]
            name = list(self.skills_system.list_skills().keys())[idx]
            self.skills_system.remove_skill(name)
            self.refresh_list()
        else:
            messagebox.showinfo("Info", "No skill selected.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    skills_system = SkillsSystem()
    skills_system.add_skill("Whirlwind", 3)
    skills_system.add_skill("Fireball", 5)
    gui = SkillsSystemGUI(skills_system)
    gui.run()
