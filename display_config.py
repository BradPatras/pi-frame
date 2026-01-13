import pygame
import os
from generate_qr import generate_qr_code

# Initialize pygame
pygame.init()

# Get the script's directory for relative paths
script_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Script directory: {script_dir}")

# Set up fullscreen display
print("Setting up display...")
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
print(f"Screen size: {screen_width}x{screen_height}")
pygame.display.set_caption("Photo Display")

# Hide mouse cursor
pygame.mouse.set_visible(False)
print("Display setup complete")

clock = pygame.time.Clock()

# Generate QR code with current config webpage info
qr_data = "test-config-page-url"
qr_output_path = os.path.join(script_dir, "qr_code.png")
generate_qr_code(data=qr_data, output_file=qr_output_path)
qr_img = pygame.image.load(qr_output_path)
qr_width, qr_height = qr_img.get_size()
scale = min(200 / qr_width, 200 / qr_height)
new_width = int(qr_width * scale)
new_height = int(qr_height * scale)
scaled_img = pygame.transform.scale(qr_img, (new_width, new_height))


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

    # Clear screen with black
    screen.fill((0, 0, 0))
    
    # Draw current image centered
    img_rect = scaled_img.get_rect(
        center=(screen_width // 2, screen_height // 2)
    )
    screen.blit(scaled_img, img_rect)

    # Draw wifi name and password
    font = pygame.font.SysFont("Arial", 30)
    subtitle_font = pygame.font.SysFont("Arial", 26)

    wifi_name = "MyWiFiNetwork"
    wifi_password = "SuperSecretPassword"
    wifi_text = f"WiFi: {wifi_name}  Password: {wifi_password}"
    
    step2_surface = font.render("Then, scan the QR code below to access the configuration page", True, (255, 255, 255))
    step2_rect = step2_surface.get_rect(center=(screen_width // 2, img_rect.top - 60))
    screen.blit(step2_surface, step2_rect)

    creds_surface = font.render(wifi_text, True, (255, 255, 255))
    creds_rect = creds_surface.get_rect(center=(screen_width // 2, step2_rect.top - 40))
    screen.blit(creds_surface, creds_rect)

    step1_surface = font.render("First, connect your phone or computer to the frame's wifi network", True, (255, 255, 255))
    step1_rect = step1_surface.get_rect(center=(screen_width // 2, creds_rect.top - 40))
    screen.blit(step1_surface, step1_rect)

    step3_surface = subtitle_font.render("Pressing the config button again will return the frame to display mode", True, (200, 200, 200))
    step3_rect = step3_surface.get_rect(center=(screen_width // 2, img_rect.bottom + 60))
    screen.blit(step3_surface, step3_rect)

    pygame.display.flip()
    clock.tick(1)  # 1 FPS

pygame.quit()
