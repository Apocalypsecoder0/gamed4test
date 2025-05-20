# Main entry point for the ARPG game application
# Launches the main menu and integrates all major game systems

from main_menu import MainMenuGUI
import tkinter as tk

if __name__ == "__main__":
    from main_menu import CharacterSelectGUI
    class StartMenu:
        def __init__(self, root):
            self.root = root
            self.root.title("Arcane Engine - Start Menu")
            self.root.geometry("1024x640")
            self.root.configure(bg="#181818")
            title_font = ("Georgia", 32, "bold")
            subtitle_font = ("Georgia", 14, "italic")
            label_fg = "#e0c080"
            tk.Label(root, text="ARCANE ENGINE: ETERNAL QUEST", font=title_font, fg=label_fg, bg="#181818").pack(pady=(60,10))
            tk.Label(root, text="by Shadow Studios", font=subtitle_font, fg="#b0a080", bg="#181818").pack(pady=(0,20))
            tk.Label(root, text="Press Start to Begin", font=("Georgia", 16), fg="#fffbe6", bg="#181818").pack(pady=(0,30))
            self.start_btn = tk.Button(root, text="Start Game", font=("Georgia", 18, "bold"), bg="#23201a", fg="#e0c080", activebackground="#40351a", activeforeground="#fffbe6", relief=tk.FLAT, cursor="hand2", width=16, height=2, command=self.start_game)
            self.start_btn.pack()
            self.root.bind('<Return>', lambda e: self.start_game())
        def start_game(self):
            self.root.withdraw()
            # Load character list from file
            import pickle
            try:
                with open("characters.pkl", "rb") as f:
                    char_list = pickle.load(f)
            except Exception:
                char_list = []
            def on_select(character):
                self.root.destroy()
                new_root = tk.Tk()
                new_root.geometry("1024x640")
                menu = MainMenuGUI()
                menu.character = character
                new_root.mainloop()
            CharacterSelectGUI(self.root, char_list, on_select)
    try:
        root = tk.Tk()
        start_menu = StartMenu(root)
        root.mainloop()
    except Exception as e:
        print(f"An error occurred while launching the game: {e}")
        root = tk.Tk()
        root.title("ARPG Game Window")
        root.geometry("800x600")
        root.mainloop()