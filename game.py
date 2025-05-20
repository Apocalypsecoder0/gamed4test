# Main entry point for the ARPG game application
# Launches the main menu and integrates all major game systems

from main_menu import MainMenuGUI

if __name__ == "__main__":
    try:
        menu = MainMenuGUI()
        menu.run()  # Assumes MainMenuGUI has a run() or similar method to start the GUI
    except Exception as e:
        print(f"An error occurred while launching the game: {e}")
