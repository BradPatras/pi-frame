import pygame
import sys
import random
import time
import os
import glob
import yaml
from gpiozero import Button
from generate_qr import generate_qr_code
import subprocess
import socket
from image_utils import load_and_scale_image, adjust_image_temp


class PhotoFrame:
    def __init__(self):
        # Display state
        self.screen = None
        self.screen_width = 0
        self.screen_height = 0

        # Mode state
        self.config_button_pressed = False
        self.is_config_mode = False
        self.running = True

        # Photo display state
        self.image_index = 0
        self.last_change = None
        self.current_surface = None
        self.next_surface = None
        self.image_files = []
        self.refresh_interval = self.get_interval_seconds()
        self.color_adjustment = self.get_color_adjustment()

        # Config display state
        self.scaled_qr_img = None
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.ip_address = None

        # Config button setup
        self.config_button = Button(16)
        self.config_button.when_pressed = self.config_button_pressed_callback

    def config_button_pressed_callback(self):
        self.config_button_pressed = True

    def run(self):
        # setup pygame
        pygame.init()
        clock = pygame.time.Clock()

        # Set up fullscreen display
        print("Setting up display...")
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width, self.screen_height = self.screen.get_size()
        print(f"Screen size: {self.screen_width}x{self.screen_height}")
        pygame.display.set_caption("Photo Display")

        # Hide mouse cursor
        pygame.mouse.set_visible(False)
        print("Display setup complete")

        # Initialize photo display
        self.setup_photo_display()

        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                    break

            # Toggle operating mode if needed
            if self.config_button_pressed:
                if self.is_config_mode:
                    self.setup_photo_display()
                    self.is_config_mode = False
                else:
                    self.setup_config_screen()
                    self.is_config_mode = True
                self.config_button_pressed = False

            if self.is_config_mode:
                self.render_config_screen()
            else:
                self.render_display_screen(clock)

            pygame.display.flip()
            clock.tick(1)  # 1 FPS

        self.stop()

    def stop(self):
        pygame.quit()
        sys.exit(0)

    def setup_photo_display(self):
        print(f"Script directory: {self.script_dir}")

        # Stop local wifi hotspot
        subprocess.run(["../stop_hotspot.sh"], cwd=self.script_dir)

        # Get image files
        images_folder = os.path.join(self.script_dir, "static", "images")
        print(f"Looking for images in: {images_folder}")
        image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.bmp"]
        self.image_files = []

        self.refresh_interval = self.get_interval_seconds()

        for ext in image_extensions:
            self.image_files.extend(glob.glob(os.path.join(images_folder, ext)))

        if not self.image_files:
            print(f"No images found in {images_folder}")
            print(f"Directory exists: {os.path.exists(images_folder)}")
            if os.path.exists(images_folder):
                print(f"Directory contents: {os.listdir(images_folder)}")
            sys.exit(1)

        print(f"Found {len(self.image_files)} images")

        # Shuffle images initially
        random.shuffle(self.image_files)
        print("Images shuffled")

        # Reset display state
        self.image_index = 0
        self.last_change = time.time()
        self.current_surface = None
        self.next_surface = None

    def setup_config_screen(self):
        print(f"Script directory: {self.script_dir}")

        # Start local wifi hotspot
        subprocess.run(["../start_hotspot.sh"], cwd=self.script_dir)
        # TODO: this may not work for the pi, need to do some testing with the pi hardware/os
        self.ip_address = socket.gethostbyname(socket.gethostname())

        # Frontend should be pre-built before deployment (npm run build)
        frontend_dir = os.path.join(self.script_dir, "..", "config_interface-frontend")

        # Start backend server
        self.backend_process = subprocess.Popen(
            ["gunicorn", "-w", "2", "-b", "0.0.0.0:5555", "server:app"],
            cwd=os.path.join(self.script_dir, "..", "config_interface-backend"),
        )

        # Start frontend server using Python's built-in HTTP server
        dist_dir = os.path.join(frontend_dir, "dist")
        self.frontend_process = subprocess.Popen(
            ["python3", "-m", "http.server", "6666", "--directory", dist_dir],
            cwd=frontend_dir,
        )

        # Generate QR code with config frontend URL
        qr_data = f"http://{self.ip_address}:6666"

        qr_output_path = os.path.join(self.script_dir, "qr_code.png")
        generate_qr_code(data=qr_data, output_file=qr_output_path)
        qr_img = pygame.image.load(qr_output_path)
        qr_width, qr_height = qr_img.get_size()
        scale = min(200 / qr_width, 200 / qr_height)
        new_width = int(qr_width * scale)
        new_height = int(qr_height * scale)
        self.scaled_qr_img = pygame.transform.scale(qr_img, (new_width, new_height))

    def render_config_screen(self):
        # Clear screen with black
        self.screen.fill((0, 0, 0))

        # Draw current image centered
        img_rect = self.scaled_qr_img.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2)
        )
        self.screen.blit(self.scaled_qr_img, img_rect)

        # Draw wifi name and password
        font = pygame.font.SysFont("Arial", 30)
        subtitle_font = pygame.font.SysFont("Arial", 26)

        wifi_name = "MyWiFiNetwork"
        wifi_password = "SuperSecretPassword"
        wifi_text = f"WiFi: {wifi_name}  Password: {wifi_password}"

        step2_surface = font.render(
            "Then, scan the QR code below to access the configuration page",
            True,
            (255, 255, 255),
        )
        step2_rect = step2_surface.get_rect(
            center=(self.screen_width // 2, img_rect.top - 60)
        )
        self.screen.blit(step2_surface, step2_rect)

        creds_surface = font.render(wifi_text, True, (255, 255, 255))
        creds_rect = creds_surface.get_rect(
            center=(self.screen_width // 2, step2_rect.top - 40)
        )
        self.screen.blit(creds_surface, creds_rect)

        step1_surface = font.render(
            "First, connect your phone or computer to the frame's wifi network",
            True,
            (255, 255, 255),
        )
        step1_rect = step1_surface.get_rect(
            center=(self.screen_width // 2, creds_rect.top - 40)
        )
        self.screen.blit(step1_surface, step1_rect)

        step3_surface = subtitle_font.render(
            "Pressing the config button again will return the frame to display mode",
            True,
            (200, 200, 200),
        )
        step3_rect = step3_surface.get_rect(
            center=(self.screen_width // 2, img_rect.bottom + 60)
        )
        self.screen.blit(step3_surface, step3_rect)

    def render_display_screen(self, clock):
        # Check if it's time to change image
        if time.time() - self.last_change >= self.refresh_interval:

            self.image_index += 1

            # When we reach the end, shuffle and restart
            if self.image_index >= len(self.image_files):
                self.image_index = 0
                random.shuffle(self.image_files)

            # Use preloaded image if available
            if self.next_surface:
                self.current_surface = self.next_surface
            else:
                self.current_surface = self.load_image(
                    self.image_files[self.image_index]
                )

            # Preload next image
            next_index = (self.image_index + 1) % len(self.image_files)
            self.next_surface = self.load_image(self.image_files[next_index])

            self.last_change = time.time()

        # Clear screen with black
        self.screen.fill((0, 0, 0))

        # Draw current image centered
        if self.current_surface:
            img_rect = self.current_surface.get_rect(
                center=(self.screen_width // 2, self.screen_height // 2)
            )
            self.screen.blit(self.current_surface, img_rect)

    def load_image(self, image_path):
        image = load_and_scale_image(image_path, self.screen_width, self.screen_height)
        if self.color_adjustment is not None:
            image = adjust_image_temp(image, int(self.color_adjustment))
        return image

    def get_interval_seconds(self):
        config_path = os.path.join(self.script_dir, "static", "config.yml")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    config = yaml.safe_load(f)
                    interval = config.get("image_interval", 2)
                    interval_unit = config.get("image_interval_unit", "hours")
                    if interval_unit == "minutes":
                        return interval * 60
                    else:  # assume hours
                        return interval * 60 * 60
            except:
                pass
        return 2 * 60 * 60  # Default to 2 hours in seconds

    def get_color_adjustment(self):
        config_path = os.path.join(self.script_dir, "static", "config.yml")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    config = yaml.safe_load(f)
                    color_temp = config.get("color_temperature", None)
                    return color_temp
            except:
                pass
        return None


def main():
    frame = PhotoFrame()
    frame.run()
