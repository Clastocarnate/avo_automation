import tkinter as tk
from PIL import Image, ImageTk, ImageFont, ImageDraw
import subprocess
import os
import cv2
import numpy as np
import glob

def main_window():
    # Create the main root window
    root = tk.Tk()
    root.geometry("700x820")
    root.bind("<Configure>", lambda event: resize_elements(root))

    # Set background image
    bg_image = Image.open("assets/flat_bg.png")
    bg_image = bg_image.resize((700, 820), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
    bg_label.place(relwidth=1, relheight=1)

    # Add start button
    start_image = Image.open("assets/start.jpg")
    start_image = start_image.resize((200, 75), Image.LANCZOS)
    start_photo = ImageTk.PhotoImage(start_image)
    start_button = tk.Button(root, image=start_photo, command=lambda: goto_main_menu(root), borderwidth=0)
    start_button.image = start_photo
    start_button.place(relx=0.5, rely=0.7, anchor="center")

    root.mainloop()

def resize_elements(root):
    # Adjust elements based on window resizing
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label) and hasattr(widget, 'image'):
            widget.image = ImageTk.PhotoImage(Image.open("assets/flat_bg.png").resize((root.winfo_width(), root.winfo_height()), Image.LANCZOS))
            widget.config(image=widget.image)
        elif isinstance(widget, tk.Button) and hasattr(widget, 'image'):
            widget_width = root.winfo_width() // 3
            widget_height = root.winfo_height() // 12
            widget_image = Image.open("assets/start.jpg").resize((widget_width, widget_height), Image.LANCZOS)
            widget.image = ImageTk.PhotoImage(widget_image)
            widget.config(image=widget.image)
            widget.place(relx=0.5, rely=0.7, anchor="center")

def goto_main_menu(root):
    # Destroy the welcome window
    root.destroy()

    # Create the main menu window
    main_menu = tk.Tk()
    main_menu.geometry("700x820")
    main_menu.bind("<Configure>", lambda event: resize_elements(main_menu))

    # Set background image
    bg_image = Image.open("assets/flat_bg.png")
    bg_image = bg_image.resize((700, 820), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(main_menu, image=bg_photo)
    bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
    bg_label.place(relwidth=1, relheight=1)

    # Add buttons for each menu item with 50 px spacing between them
    buttons = [
        ("assets/New.jpg", open_new_dataset),
        ("assets/select_brush.jpg", open_select_brush),
        ("assets/train.jpg", open_train),
        ("assets/Daily_Operations.jpg", open_daily_operations),
    ]

    for i, (image_path, command) in enumerate(buttons):
        button_image = Image.open(image_path)
        button_image = button_image.resize((200, 75), Image.LANCZOS)
        button_photo = ImageTk.PhotoImage(button_image)
        button = tk.Button(main_menu, image=button_photo, command=lambda c=command: c(main_menu), borderwidth=0)
        button.image = button_photo
        button.place(relx=0.5, y=260 + i * 150, anchor="n")

    main_menu.protocol("WM_DELETE_WINDOW", lambda: on_close(main_menu))
    main_menu.mainloop()

def open_new_dataset(main_menu):
    # Run the new_dataset.py script
    subprocess.Popen(["python", "new_dataset.py"])

def open_select_brush():
    # Open a new window for Select Brush
    select_brush_window()

def open_train():
    # Open a new window for Train
    new_window("Train")
    subprocess.Popen(["python", "train.py"])

def open_daily_operations():
    # Open a new window for Daily Operations
    new_window("Daily Operations")

def select_brush_window():
    # Create a new window for Select Brush
    window = tk.Toplevel()
    window.title("Select Brush")
    window.geometry("700x820")
    window.bind("<Configure>", lambda event: resize_elements(window))

    # Set background image
    bg_image = Image.open("assets/Technology Wallpaper.jpg")
    bg_image = bg_image.resize((700, 820), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(window, image=bg_photo)
    bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
    bg_label.place(relwidth=1, relheight=1)

    # List all dataset folders and create buttons with custom font and image
    dataset_folders = [folder for folder in os.listdir('.') if os.path.isdir(folder) and folder.startswith('dataset_')]
    font_path = "assets/Loubag-Bold.ttf"
    font_size = 70
    font = ImageFont.truetype(font_path, font_size)
    button_image_path = "assets/Button.jpg"

    # Calculate button placement dynamically
    button_width = 200
    button_height = 75
    max_buttons_per_column = (820 - 20) // (button_height + 20)
    num_columns = (len(dataset_folders) + max_buttons_per_column - 1) // max_buttons_per_column

    for idx, folder in enumerate(dataset_folders):
        # Load the button image using OpenCV
        image = cv2.imread(button_image_path)
        if image is None:
            print("Failed to load the image. Please check the path.")
            continue

        # Convert OpenCV image (BGR) to PIL format (RGB)
        image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Prepare to draw on the image
        draw = ImageDraw.Draw(image_pil)
        draw.text((70, 25), folder, font=font, fill="white")

        # Save the image with text
        image_with_text_path = f"assets/{folder}_button.jpg"
        image_pil.save(image_with_text_path)

        # Load the image with text for Tkinter
        button_img_pil = Image.open(image_with_text_path)
        button_img_pil = button_img_pil.resize((200, 75), Image.LANCZOS)
        button_photo = ImageTk.PhotoImage(button_img_pil)

        # Calculate button position
        column = idx // max_buttons_per_column
        row = idx % max_buttons_per_column
        x_position = 20 + column * (button_width + 20)
        y_position = 20 + row * (button_height + 20)

        # Create button
        button = tk.Button(window, image=button_photo, borderwidth=0)
        button.image = button_photo
        button.place(x=x_position, y=y_position)

    window.protocol("WM_DELETE_WINDOW", lambda: on_close(window))
    window.mainloop()

def new_window(title):
    # Create a new window with the given title
    window = tk.Toplevel()
    window.title(title)
    window.geometry("700x820")
    window.bind("<Configure>", lambda event: resize_elements(window))

    # Set background image
    bg_image = Image.open("assets/flat_bg.png")
    bg_image = bg_image.resize((700, 820), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(window, image=bg_photo)
    bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
    bg_label.place(relwidth=1, relheight=1)

    window.protocol("WM_DELETE_WINDOW", lambda: on_close(window))
    window.mainloop()

def on_close(window):
    # Close the window
    window.destroy()
    # Delete all generated button images
    for file_path in glob.glob("assets/dataset_*_button.jpg"):
        os.remove(file_path)

if __name__ == "__main__":
    main_window()
