import pygame
import sys
import random
import time
import os
import glob
import yaml
import datetime
from gpiozero import Button, PWMOutputDevice
from generate_qr import generate_qr_code
import subprocess
from image_utils import load_and_scale_image, adjust_image_temp
from network import enable_wifi_hotspot, disable_wifi_hotspot


class PhotoFrame:
    def __init__(self):
        self.wifi_name = "pi-frame"
        self.wifi_password = "purp0droid%BAHA"

        # Display state
        self.screen = None
        self.screen_width = 0
        self.screen_height = 0

        # Config display state
        self.config_scaled_qr_img = None
        self.hotspot_scaled_qr_img = None
        self.backend_process = None
        self.frontend_process = None

        # The pi's NetworkManager shoooouuld always set the pi's IP to 10.42.0.1 when in hotspot mode
        self.ip_address = "10.42.0.1"

        # Paths
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(
            self.script_dir, "../", "frame-config-backend", "static", "config.yml"
        )
        self.images_path = os.path.join(
            self.script_dir, "../", "frame-config-backend", "static", "images"
        )
        self.frontend_dir_path = os.path.join(
            self.script_dir, "../", "frame-config-frontend"
        )
        self.backend_dir_path = os.path.join(
            self.script_dir, "../", "frame-config-backend"
        )

        # Mode state
        self.config_button_pressed = False
        self.is_config_mode = False
        self.running = True

        # Photo display state
        self.image_index = 0
        self.last_change = None
        self.current_surface = None
        self.image_files = []
        self.refresh_interval = self.get_interval_seconds()
        self.color_adjustment = self.get_color_adjustment()

        # Button GPIO
        self.config_button = None

    def config_button_pressed_callback(self):
        self.config_button_pressed = True

    def set_screen_brightness(self, value=1.0):
        # value must be between 0 and 1
        brightness = max(0, min(1.0, value))
        self.screen_pwm.value = value

    def run(self):
        # Config button setup
        self.config_button = Button(16)
        self.config_button.when_pressed = self.config_button_pressed_callback

        # Screen brightness wpm setup
        self.screen_pwm = PWMOutputDevice(
            12, active_high=False, initial_value=0.5, frequency=100
        )

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

            self.update_display_brightness()

            if self.is_config_mode:
                self.render_config_screen()
            else:
                self.render_display_screen(clock)

            pygame.display.flip()
            clock.tick(1)  # 1 FPS

        self.stop()

    def stop(self):
        self.stopServers()
        pygame.quit()
        sys.exit(0)

    def stopServers(self):
        if self.backend_process is not None:
            self.backend_process.kill()
        if self.frontend_process is not None:
            self.frontend_process.kill()

    def update_display_brightness(self):
        night_start = self.get_night_mode_start()
        night_end = self.get_night_mode_end()
        if night_start == None or night_end == None:
            # nightmode not setup, default to full brightness
            self.screen_pwm.value = 1.0
            return

        # only bothering with the typical case of start in the
        # evening and end in the morning
        current_hour = datetime.datetime.now().hour
        if current_hour not in range(night_end, night_start):
            self.screen_pwm.value = 0.0
        else:
            self.screen_pwm.value = 1.0

    def setup_photo_display(self):
        print(f"Script directory: {self.script_dir}")

        # Stop local wifi hotspot
        disable_wifi_hotspot()
        self.stopServers()

        # Get image files
        print(f"Looking for images in: {self.images_path}")
        image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.bmp"]
        self.image_files = []

        self.refresh_interval = self.get_interval_seconds()

        # collect image-typed files in the images directory
        for ext in image_extensions:
            self.image_files.extend(glob.glob(os.path.join(self.images_path, ext)))

        # If no images found, swap trigger config mode and return early
        if not self.image_files:
            print(f"No images found in {self.images_path}")
            self.config_button_pressed = True
            return

        print(f"Found {len(self.image_files)} images")

        # Shuffle images initially
        random.shuffle(self.image_files)
        print("Images shuffled")

        # Reset display state
        self.image_index = 0
        self.last_change = time.time()
        self.current_surface = self.load_image(self.image_files[self.image_index])

    def setup_config_screen(self):
        # Start local wifi hotspot
        enable_wifi_hotspot(self.wifi_name, self.wifi_password)

        # Start backend server
        self.backend_process = subprocess.Popen(
            ["gunicorn", "-w", "2", "-b", "0.0.0.0:50001", "server:app"],
            cwd=self.backend_dir_path,
        )

        # Start frontend server using Python's built-in HTTP server
        self.frontend_process = subprocess.Popen(
            ["python3", "-m", "http.server", "50002"],
            cwd=self.frontend_dir_path,
        )

        qr_size = self.screen_height / 4

        # Generate QR code with config frontend URL
        config_qr_data = f"http://{self.ip_address}:50002"
        config_qr_output_path = os.path.join(self.script_dir, "config_qr_code.png")
        generate_qr_code(data=config_qr_data, output_file=config_qr_output_path)
        qr_img = pygame.image.load(config_qr_output_path)
        self.config_scaled_qr_img = pygame.transform.scale(qr_img, (qr_size, qr_size))

        # Generate QR code with hotspot info
        hotspot_qr_data = f"WIFI:T:WPA;S:{self.wifi_name};P:{self.wifi_password};;"
        hotspot_qr_output_path = os.path.join(self.script_dir, "hotspot_qr_code.png")
        generate_qr_code(data=hotspot_qr_data, output_file=hotspot_qr_output_path)
        hotspot_qr_img = pygame.image.load(hotspot_qr_output_path)
        self.hotspot_scaled_qr_img = pygame.transform.scale(
            hotspot_qr_img, (qr_size, qr_size)
        )

    def render_config_screen(self):
        # Clear screen with black
        self.screen.fill((0, 0, 0))

        center_x = self.screen_width // 2

        font = pygame.font.SysFont("Arial", 24)
        subtitle_font = pygame.font.SysFont("Arial", 18)

        ## HostSpot Instructions (left side of screen)
        # Draw hotspot QR code
        hotspot_img_rect = self.hotspot_scaled_qr_img.get_rect(
            center=(center_x // 2, self.screen_height // 3)
        )
        self.screen.blit(self.hotspot_scaled_qr_img, hotspot_img_rect)

        # Draw instructions for connecting to hotspot
        self.render_text_list(
            [
                "First, connect your phone or",
                "computer to the frame's wifi network",
                f"ssid: {self.wifi_name}",
                f"pw: {self.wifi_password}",
            ],
            center_x // 2,
            hotspot_img_rect.bottom + 60,
            font,
            self.screen,
        )

        ## Config Interface Instructions (right side of screen)
        # Draw config interface QR code
        config_img_rect = self.config_scaled_qr_img.get_rect(
            center=(center_x + center_x // 2, self.screen_height // 3)
        )
        self.screen.blit(self.config_scaled_qr_img, config_img_rect)

        self.render_text_list(
            [
                "Then, scan the QR code above to",
                "access the configuration page",
            ],
            center_x + center_x // 2,
            config_img_rect.bottom + 60,
            font,
            self.screen,
        )

        step3_surface = subtitle_font.render(
            "Pressing the config button again will return the frame to display mode",
            True,
            (200, 200, 200),
        )
        step3_rect = step3_surface.get_rect(
            center=(center_x, self.screen_height - (20 + step3_surface.get_height()))
        )
        self.screen.blit(step3_surface, step3_rect)

        # Draw line down middle of screen
        pygame.draw.line(
            self.screen,
            (100, 100, 100),
            (center_x, 100),
            (center_x, step3_rect.top - 60),
            4,
        )

    def render_text_list(self, textList, locationX, locationY, font, screen):
        offsetY = 0
        for text in textList:
            surface = font.render(
                text,
                True,
                (255, 255, 255),
            )
            rect = surface.get_rect(center=(locationX, locationY + offsetY))
            screen.blit(surface, rect)
            offsetY += surface.get_height() + 10

    def render_display_screen(self, clock):
        # Check if it's time to change image
        if time.time() - self.last_change >= self.refresh_interval:

            self.image_index += 1

            # When we reach the end, shuffle and restart
            if self.image_index >= len(self.image_files):
                self.image_index = 0
                random.shuffle(self.image_files)

            self.current_surface = self.load_image(self.image_files[self.image_index])

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
        if self.color_adjustment is not None and self.color_adjustment != "":
            image = adjust_image_temp(image, int(self.color_adjustment))
        return image

    def get_interval_seconds(self):
        configs = self.get_configs()
        if configs == None:
            print("pi_frame_main.getIntervalSeconds: Failed to parse configs")
            return 2 * 60 * 60  # Default to 2 hours in seconds

        interval = configs.get("image_interval", 2)
        if interval == None:
            interval = 2

        interval_unit = configs.get("image_interval_unit", "hours")
        if interval_unit == "minutes":
            return interval * 60
        else:  # assume hours
            return interval * 60 * 60

    def get_night_mode_start(self):
        configs = self.get_configs()
        start = configs.get("night_start", None)
        if start == "":
            return None

        try:
            start_int = int(start)
            return max(0, min(start_int, 23))
        except:
            print("pi_frame_main.get_night_mode_start failed to parse")
            return None

    def get_night_mode_end(self):
        configs = self.get_configs()
        end = configs.get("night_end", None)
        if end == "":
            return None

        try:
            end_int = int(end)
            return max(0, min(end_int, 23))
        except:
            print("pi_frame_main.get_night_mode_start failed to parse")

    def get_configs(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    return yaml.safe_load(f)
            except:
                print("pi_frame_main: Failed to parse config")
                return None

    def get_color_adjustment(self):
        adjustment = None
        configs = self.get_configs()
        if configs != None:
            adjustment = configs.get("color_temperature", None)

        try:
            adjustment = int(adjustment)
        except (TypeError, ValueError):
            return None

        return adjustment


def main():
    frame = PhotoFrame()
    try:
        frame.run()
    except KeyboardInterrupt:
        frame.stop()


if __name__ == "__main__":
    main()
