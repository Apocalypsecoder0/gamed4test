# Main entry point for the ARPG game application
# Launches the main menu and integrates all major game systems

from main_menu import MainMenuGUI, StartMenu
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Arcane Engine")  # Set window title
    root.geometry("1280x720")    # Set window size for a modern ARPG look
    root.configure(bg="#181818") # Dark background for Diablo 4 style

    # Optional: Add a splash or logo image (requires Pillow and an image file)
    try:
        from PIL import Image, ImageTk
        logo_img = Image.open("logo.png")  # Place your logo image in the project folder
        logo_img = logo_img.resize((400, 120))
        logo_photo = ImageTk.PhotoImage(logo_img)
        logo_label = tk.Label(root, image=logo_photo, bg="#181818")
        logo_label.image = logo_photo
        logo_label.place(relx=0.5, rely=0.25, anchor="center")
    except Exception:
        logo_label = tk.Label(root, text="Arcane Engine", font=("Georgia", 48, "bold"), fg="#e0c080", bg="#181818")
        logo_label.place(relx=0.5, rely=0.25, anchor="center")

    subtitle = tk.Label(root, text="A Modern ARPG Experience", font=("Georgia", 20, "italic"), fg="#b0a080", bg="#181818")
    subtitle.place(relx=0.5, rely=0.35, anchor="center")

    def launch_main_menu():
        root.withdraw()
        menu = MainMenuGUI()
        menu.run()

    # Stylized Start button
    start_btn = tk.Button(
        root, text="Start Game", font=("Georgia", 20, "bold"),
        bg="#23201a", fg="#e0c080", activebackground="#3a2f1a", activeforeground="#fff",
        bd=0, padx=40, pady=15, cursor="hand2", command=launch_main_menu
    )
    start_btn.place(relx=0.5, rely=0.55, anchor="center")

    # Optionally, add Quit button
    quit_btn = tk.Button(
        root, text="Quit", font=("Georgia", 14),
        bg="#23201a", fg="#b0a080", activebackground="#3a2f1a", activeforeground="#fff",
        bd=0, padx=30, pady=8, cursor="hand2", command=root.destroy
    )
    quit_btn.place(relx=0.5, rely=0.65, anchor="center")

    root.mainloop()

if __name__ == "__main__":
    main()