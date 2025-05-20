# Main entry point for the ARPG game application
# Launches the main menu and integrates all major game systems

from main_menu import MainMenuGUI
import tkinter as tk

if __name__ == "__main__":
    try:
        root = tk.Tk()
        menu = MainMenuGUI()
        root.mainloop()  # Start the Tkinter main loop using the root window
    except Exception as e:
        print(f"An error occurred while launching the game: {e}")
        root = tk.Tk()
        root.title("ARPG Game Window")
        root.geometry("800x600")
        root.mainloop()