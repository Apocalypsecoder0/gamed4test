import tkinter as tk
from tkinter import messagebox
from typing import List, Dict, Optional

class SocialSystem:
    def __init__(self):
        self.friends: List[str] = []
        self.clan: Optional[str] = None

    def add_friend(self, name: str):
        if name not in self.friends:
            self.friends.append(name)

    def remove_friend(self, name: str):
        if name in self.friends:
            self.friends.remove(name)

    def set_clan(self, clan_name: str):
        self.clan = clan_name

    def list_friends(self) -> List[str]:
        return self.friends

class SocialSystemGUI:
    def __init__(self, social_system: SocialSystem):
        self.social_system = social_system
        self.root = tk.Tk()
        self.root.title("Social Menu")
        self.friends_listbox = tk.Listbox(self.root, width=40)
        self.friends_listbox.pack(padx=10, pady=10)
        self.add_button = tk.Button(self.root, text="Add Friend", command=self.add_friend_window)
        self.add_button.pack(pady=5)
        self.remove_button = tk.Button(self.root, text="Remove Selected", command=self.remove_selected)
        self.remove_button.pack(pady=5)
        self.clan_label = tk.Label(self.root, text="Clan: None")
        self.clan_label.pack(pady=5)
        self.set_clan_button = tk.Button(self.root, text="Set Clan", command=self.set_clan_window)
        self.set_clan_button.pack(pady=5)
        self.refresh_list()

    def refresh_list(self):
        self.friends_listbox.delete(0, tk.END)
        for friend in self.social_system.list_friends():
            self.friends_listbox.insert(tk.END, friend)
        self.clan_label.config(text=f"Clan: {self.social_system.clan or 'None'}")

    def add_friend_window(self):
        win = tk.Toplevel(self.root)
        win.title("Add Friend")
        tk.Label(win, text="Friend Name:").grid(row=0, column=0)
        name_entry = tk.Entry(win)
        name_entry.grid(row=0, column=1)
        def submit():
            name = name_entry.get()
            if name:
                self.social_system.add_friend(name)
                self.refresh_list()
                win.destroy()
            else:
                messagebox.showerror("Error", "Friend name required.")
        tk.Button(win, text="Add", command=submit).grid(row=1, column=0, columnspan=2)

    def remove_selected(self):
        selection = self.friends_listbox.curselection()
        if selection:
            idx = selection[0]
            name = self.social_system.list_friends()[idx]
            self.social_system.remove_friend(name)
            self.refresh_list()
        else:
            messagebox.showinfo("Info", "No friend selected.")

    def set_clan_window(self):
        win = tk.Toplevel(self.root)
        win.title("Set Clan")
        tk.Label(win, text="Clan Name:").grid(row=0, column=0)
        clan_entry = tk.Entry(win)
        clan_entry.grid(row=0, column=1)
        def submit():
            clan = clan_entry.get()
            if clan:
                self.social_system.set_clan(clan)
                self.refresh_list()
                win.destroy()
            else:
                messagebox.showerror("Error", "Clan name required.")
        tk.Button(win, text="Set", command=submit).grid(row=1, column=0, columnspan=2)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    social_system = SocialSystem()
    social_system.add_friend("Deckard Cain")
    social_system.add_friend("Lorath Nahr")
    social_system.set_clan("Wanderers")
    gui = SocialSystemGUI(social_system)
    gui.run()
