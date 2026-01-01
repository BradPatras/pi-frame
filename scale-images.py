#!/usr/bin/env python3
"""
Image Scaler - Resize all images in a directory to fit within a bounding box
while maintaining aspect ratio.
"""

from PIL import Image, ImageOps
import os
import glob
import argparse


def scale_image(input_path, output_path, max_width, max_height):
    """
    Scale an image to fit within max_width x max_height while maintaining aspect ratio.

    Args:
        input_path: Path to input image
        output_path: Path to save scaled image
        max_width: Maximum width in pixels
        max_height: Maximum height in pixels
    """
    try:
        img = Image.open(input_path)

        # Apply EXIF orientation to fix rotation
        img = ImageOps.exif_transpose(img)

        # Convert RGBA to RGB if needed (for JPEG compatibility)
        if img.mode == "RGBA":
            background = Image.new("RGB", img.size, (0, 0, 0))
            background.paste(img, mask=img.split()[3])
            img = background
        elif img.mode not in ("RGB", "L"):
            img = img.convert("RGB")

        # Get original dimensions
        orig_width, orig_height = img.size

        # Calculate scaling factor to fit within bounding box
        scale = min(max_width / orig_width, max_height / orig_height)

        # Only scale down, never scale up
        if scale < 1.0:
            new_width = int(orig_width * scale)
            new_height = int(orig_height * scale)

            # Use LANCZOS for high quality downscaling
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            print(
                f"  Scaled from {orig_width}x{orig_height} to {new_width}x{new_height}"
            )
        else:
            print(f"  Image already fits within bounds ({orig_width}x{orig_height})")

        # Save the image
        if output_path.lower().endswith(".jpg") or output_path.lower().endswith(
            ".jpeg"
        ):
            img.save(output_path, "JPEG", quality=95, optimize=True)
        else:
            img.save(output_path, optimize=True)

        return True
    except Exception as e:
        print(f"  Error: {e}")
        return False


def process_directory(input_dir, output_dir, max_width, max_height):
    """
    Process all images in a directory.

    Args:
        input_dir: Source directory containing images
        output_dir: Destination directory for scaled images
        max_width: Maximum width in pixels
        max_height: Maximum height in pixels
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Find all image files
    image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.gif", "*.tiff"]
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(input_dir, ext)))
        image_files.extend(glob.glob(os.path.join(input_dir, ext.upper())))

    if not image_files:
        print(f"No images found in {input_dir}")
        return

    print(f"Found {len(image_files)} images")
    print(f"Target size: {max_width}x{max_height}")
    print()

    success_count = 0
    for i, input_path in enumerate(image_files, 1):
        filename = os.path.basename(input_path)
        output_path = os.path.join(output_dir, filename)

        print(f"[{i}/{len(image_files)}] Processing {filename}...")

        if scale_image(input_path, output_path, max_width, max_height):
            success_count += 1

    print()
    print(f"Complete! Successfully processed {success_count}/{len(image_files)} images")
    print(f"Scaled images saved to: {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Scale all images in a directory to fit within a bounding box"
    )
    parser.add_argument("input_dir", help="Input directory containing images")
    parser.add_argument("output_dir", help="Output directory for scaled images")
    parser.add_argument(
        "--width",
        type=int,
        default=1024,
        help="Maximum width in pixels (default: 1024)",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=600,
        help="Maximum height in pixels (default: 600)",
    )

    args = parser.parse_args()

    # Validate inputs
    if not os.path.isdir(args.input_dir):
        print(f"Error: Input directory '{args.input_dir}' does not exist")
        return 1

    process_directory(args.input_dir, args.output_dir, args.width, args.height)
    return 0


if __name__ == "__main__":
    exit(main())
