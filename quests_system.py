import tkinter as tk
from tkinter import messagebox
from typing import List, Dict, Optional

class QuestsSystem:
    def __init__(self):
        self.quests: List[Dict[str, str]] = []

    def add_quest(self, name: str, status: str = "Active"):
        self.quests.append({"name": name, "status": status})

    def remove_quest(self, name: str):
        self.quests = [q for q in self.quests if q["name"] != name]

    def list_quests(self) -> List[Dict[str, str]]:
        return self.quests

class QuestsSystemGUI:
    def __init__(self, quests_system: QuestsSystem):
        self.quests_system = quests_system
        self.root = tk.Tk()
        self.root.title("Quests Menu")
        self.listbox = tk.Listbox(self.root, width=50)
        self.listbox.pack(padx=10, pady=10)
        self.add_button = tk.Button(self.root, text="Add Quest", command=self.add_quest_window)
        self.add_button.pack(pady=5)
        self.remove_button = tk.Button(self.root, text="Remove Selected", command=self.remove_selected)
        self.remove_button.pack(pady=5)
        self.refresh_button = tk.Button(self.root, text="Refresh", command=self.refresh_list)
        self.refresh_button.pack(pady=5)
        self.refresh_list()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for quest in self.quests_system.list_quests():
            self.listbox.insert(tk.END, f"{quest['name']} ({quest['status']})")

    def add_quest_window(self):
        win = tk.Toplevel(self.root)
        win.title("Add Quest")
        tk.Label(win, text="Quest Name:").grid(row=0, column=0)
        name_entry = tk.Entry(win)
        name_entry.grid(row=0, column=1)
        tk.Label(win, text="Status:").grid(row=1, column=0)
        status_entry = tk.Entry(win)
        status_entry.grid(row=1, column=1)
        def submit():
            name = name_entry.get()
            status = status_entry.get() or "Active"
            if name:
                self.quests_system.add_quest(name, status)
                self.refresh_list()
                win.destroy()
            else:
                messagebox.showerror("Error", "Quest name required.")
        tk.Button(win, text="Add", command=submit).grid(row=2, column=0, columnspan=2)

    def remove_selected(self):
        selection = self.listbox.curselection()
        if selection:
            idx = selection[0]
            name = self.quests_system.list_quests()[idx]["name"]
            self.quests_system.remove_quest(name)
            self.refresh_list()
        else:
            messagebox.showinfo("Info", "No quest selected.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    quests_system = QuestsSystem()
    quests_system.add_quest("Defeat the Butcher", "Active")
    quests_system.add_quest("Find the Lost Artifact", "Completed")
    gui = QuestsSystemGUI(quests_system)
    gui.run()
