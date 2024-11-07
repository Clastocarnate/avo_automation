import tkinter as tk
from PIL import Image, ImageTk

def main_window():
    # Create the main root window
    root = tk.Tk()
    root.geometry("700x820")

    # Set background image
    bg_image = Image.open("assets/HomePage.png")
    bg_image = bg_image.resize((700, 820), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
    bg_label.place(relwidth=1, relheight=1)

    # Bind click event to open a new window if clicked in a specific region
    root.bind("<Button-1>", lambda event: check_click(event, root))

    root.mainloop()

def check_click(event, root):
    # Check if the click is inside the specified rectangular area
    if 239 <= event.x <= 505 and 585 <= event.y <= 674:
        goto_main_menu(root)

def goto_main_menu(root):
    # Destroy the welcome window
    root.destroy()

    # Create the main menu window
    main_menu = tk.Tk()
    main_menu.geometry("700x820")

    # Set background image
    bg_image = Image.open("assets/Menu Page.png")
    bg_image = bg_image.resize((700, 820), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(main_menu, image=bg_photo)
    bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
    bg_label.place(relwidth=1, relheight=1)

    main_menu.mainloop()

if __name__ == "__main__":
    main_window()
