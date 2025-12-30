import tkinter as tk
from PIL import Image, ImageTk
import os
import glob
import yaml
import random

# Get image files
images_folder = os.path.join("static", "images")
image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp']
image_files = []
for ext in image_extensions:
    image_files.extend(glob.glob(os.path.join(images_folder, ext)))

if not image_files:
    print(f"No images found in {images_folder}")
    exit()

# Shuffle images initially
random.shuffle(image_files)

# Create fullscreen window
root = tk.Tk()
root.attributes('-fullscreen', True)
root.configure(background='black')
root.bind('<Escape>', lambda e: root.quit())

label = tk.Label(root, bg='black')
label.pack(expand=True)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

image_index = 0

def get_interval():
    config_path = 'static/config.yml'
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            interval_hrs = config.get('image_interval_hrs', 8)
            interval_ms = interval_hrs * 60 * 60 * 1000
    else:
        interval_ms = 8 * 60 * 60 * 1000  # Default to 8 hours
    return interval_ms

def show_next_image():
    global image_index
    
    # Load and resize image
    img = Image.open(image_files[image_index])
    img.thumbnail((screen_width, screen_height), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    
    label.configure(image=photo)
    label.image = photo  # Keep a reference
    
    image_index += 1
    
    # When we reach the end, shuffle and restart
    if image_index >= len(image_files):
        image_index = 0
        random.shuffle(image_files)
    
    interval_ms = get_interval()
    root.after(interval_ms, show_next_image)  # Next image after interval

show_next_image()
root.mainloop()