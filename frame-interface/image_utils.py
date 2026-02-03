"""Image processing utilities for the photo frame."""

import pygame
from PIL import Image


def load_and_scale_image(image_path, screen_width, screen_height):
    """
    Load an image and scale it to fit the screen while maintaining aspect ratio.

    Args:
        image_path: Path to the image file
        screen_width: Target screen width
        screen_height: Target screen height

    Returns:
        Scaled pygame surface or None if loading fails
    """
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


# thanks https://stackoverflow.com/a/11888449
def adjust_image_temp(image, temp):
    """
    Convert image color temperature using Kelvin values.

    Args:
        image: PIL Image object
        temp: Temperature in Kelvin (1000-10000)

    Returns:
        PIL Image with adjusted color temperature
    """
    kelvin_table = {
        1000: (255, 56, 0),
        1500: (255, 109, 0),
        2000: (255, 137, 18),
        2500: (255, 161, 72),
        3000: (255, 180, 107),
        3500: (255, 196, 137),
        4000: (255, 209, 163),
        4500: (255, 219, 186),
        5000: (255, 228, 206),
        5500: (255, 236, 224),
        6000: (255, 243, 239),
        6500: (255, 249, 253),
        7000: (245, 243, 255),
        7500: (235, 238, 255),
        8000: (227, 233, 255),
        8500: (220, 229, 255),
        9000: (214, 225, 255),
        9500: (208, 222, 255),
        10000: (204, 219, 255),
    }

    kelvin_key = list(kelvin_table.keys())[0]
    for key in sorted(kelvin_table.keys()):
        if temp <= key:
            kelvin_key = key
            break

    r, g, b = kelvin_table[kelvin_key]
    matrix = (
        r / 255.0,
        0.0,
        0.0,
        0.0,
        0.0,
        g / 255.0,
        0.0,
        0.0,
        0.0,
        0.0,
        b / 255.0,
        0.0,
    )
    return image.convert("RGB", matrix)
