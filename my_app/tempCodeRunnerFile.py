import tkinter as tk
from PIL import Image, ImageTk
import tkinter.font as tkFont
from matplotlib import font_manager

def main_window():
    # Create the main root window
    root = tk.Tk()
    root.geometry("700x820")

    # Set background image
    bg_image = Image.open("assets/Your paragraph text-2.png")
    bg_image = bg_image.resize((700, 820), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

    # Register custom font
    font_path = "assets/Praxis-Regular Regular.otf"
    font_manager.fontManager.addfont(font_path)
    custom_font = tkFont.Font(family="Praxis Regular", size=16)
    
    # Add 'Get Started' button as a transparent white rectangle
    get_started_button = tk.Button(root, borderwidth=0, command=lambda: goto_main_menu(root), width=30, height=6)
    get_started_button.place(relx=0.5, rely=1.0, anchor='s', y=-110, x=20)

    root.mainloop()

def goto_main_menu(root):
    # Destroy the welcome window
    root.destroy()

    # Create the main menu window
    main_menu = tk.Tk()
    main_menu.title("Main Menu")
    main_menu.geometry("700x820")

    # Add buttons for different operations
    tk.Label(main_menu, text="Main Menu", font=("Arial", 16)).pack(pady=20)
    tk.Button(main_menu, text="New Dataset", state=tk.DISABLED).pack(pady=10)
    tk.Button(main_menu, text="Select Brush", state=tk.DISABLED).pack(pady=10)
    tk.Button(main_menu, text="Train", state=tk.DISABLED).pack(pady=10)
    tk.Button(main_menu, text="Daily Operations", state=tk.DISABLED).pack(pady=10)

    main_menu.mainloop()

if __name__ == "__main__":
    main_window()
