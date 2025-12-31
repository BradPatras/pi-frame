import pygame
from PIL import Image
import os
import glob
import yaml
import random
import time

# Initialize pygame
pygame.init()

# Get the script's directory for relative paths
script_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Script directory: {script_dir}")

# Get image files
images_folder = os.path.join(script_dir, "static", "images")
print(f"Looking for images in: {images_folder}")
image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.bmp"]
image_files = []
for ext in image_extensions:
    image_files.extend(glob.glob(os.path.join(images_folder, ext)))

if not image_files:
    print(f"No images found in {images_folder}")
    print(f"Directory exists: {os.path.exists(images_folder)}")
    if os.path.exists(images_folder):
        print(f"Directory contents: {os.listdir(images_folder)}")
    exit()

print(f"Found {len(image_files)} images")

# Shuffle images initially
random.shuffle(image_files)
print("Images shuffled")

# Set up fullscreen display
print("Setting up display...")
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
print(f"Screen size: {screen_width}x{screen_height}")
pygame.display.set_caption("Photo Display")

# Hide mouse cursor
pygame.mouse.set_visible(False)
print("Display setup complete")


def get_interval():
    return 3  # 3 seconds for testing
    config_path = os.path.join(script_dir, "static", "config.yml")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
                interval_hrs = config.get("image_interval_hrs", 8)
                return interval_hrs * 60 * 60  # Return in seconds
        except:
            pass
    return 8 * 60 * 60  # Default to 8 hours in seconds


def load_and_scale_image(image_path):
    try:
        img = pygame.image.load(image_path)
        img_width, img_height = img.get_size()

        # Calculate scaling to fit screen while maintaining aspect ratio
        scale = min(screen_width / img_width, screen_height / img_height)

        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        scaled_img = pygame.transform.scale(img, (new_width, new_height))

        return scaled_img
    except Exception as e:
        print(f"Error loading {image_path}: {e}")
        return None


# Display settings
clock = pygame.time.Clock()
image_index = 0
last_change = time.time()
current_surface = None
next_surface = None  # Preload next image

# Load first image
current_surface = load_and_scale_image(image_files[image_index])

# Preload second image
if len(image_files) > 1:
    next_surface = load_and_scale_image(image_files[1])

# Main loop
running = True
loop_count = 0
while running:
    loop_count += 1
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Check if it's time to change image
    interval = get_interval()
    if time.time() - last_change >= interval:

        image_index += 1

        # When we reach the end, shuffle and restart
        if image_index >= len(image_files):

            image_index = 0
            random.shuffle(image_files)

        # Use preloaded image if available
        if next_surface:
            current_surface = next_surface

        else:

            current_surface = load_and_scale_image(image_files[image_index])

        # Preload next image
        next_index = (image_index + 1) % len(image_files)

        next_surface = load_and_scale_image(image_files[next_index])

        last_change = time.time()

    # Clear screen with black
    screen.fill((0, 0, 0))

    # Draw current image centered
    if current_surface:
        img_rect = current_surface.get_rect(
            center=(screen_width // 2, screen_height // 2)
        )
        screen.blit(current_surface, img_rect)

    pygame.display.flip()
    clock.tick(1)  # 1 FPS

pygame.quit()
