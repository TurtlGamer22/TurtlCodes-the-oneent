import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Platformer")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Define player properties
player_width, player_height = 50, 50
player_speed = 5
jump_height = -10
gravity = 0.5
is_jumping = False

# Define platform properties
platform_width, platform_height = 100, 20
platform_speed = 5
platforms = []

# Define power-up properties
powerup_width, powerup_height = 30, 30
powerup_spawn_chance = 0.02  # Chance of a power-up spawning on each platform
powerup_speed = platform_speed  # Power-up moves at the same speed as platforms
powerups = []

# Define scoring
score = 0
font = pygame.font.SysFont(None, 36)

# Create base platform
base_platform = pygame.Rect(0, HEIGHT - platform_height, WIDTH, platform_height)
platforms.append(base_platform)

# Create initial platforms above the base platform
for i in range(5):
    x = random.randint(0, WIDTH - platform_width)
    y = random.randint(HEIGHT // 2, HEIGHT - platform_height - 50)
    platforms.append(pygame.Rect(x, y, platform_width, platform_height))

# Ensure player spawns on the base platform
player_x = random.randint(0, WIDTH - player_width)
player_y = base_platform.top - player_height

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    # Jumping mechanism
    if keys[pygame.K_SPACE] and not is_jumping:
        is_jumping = True
        jump_height = -10

    if is_jumping:
        player_y += jump_height
        jump_height += gravity
        if jump_height >= 10:
            is_jumping = False

    # Update platforms
    for platform in platforms:
        if not is_jumping and platform.collidepoint(player_x + player_width // 2, player_y + player_height):
            break  # Stop updating platforms if the player is on a platform
        platform.y += platform_speed
        if platform.y > HEIGHT:
            platforms.remove(platform)
            # Generate new platform
            x = random.randint(0, WIDTH - platform_width)
            y = random.randint(-100, -20)
            platforms.append(pygame.Rect(x, y, platform_width, platform_height))
            # Spawn power-up on platform
            if random.random() < powerup_spawn_chance:
                powerups.append(pygame.Rect(x + (platform_width - powerup_width) // 2,
                                            y - powerup_height,
                                            powerup_width,
                                            powerup_height))

    # Update power-ups
    for powerup in powerups:
        powerup.y += powerup_speed
        if powerup.colliderect(pygame.Rect(player_x, player_y, player_width, player_height)):
            powerups.remove(powerup)
            score += 10  # Increase score when collecting a power-up

    # Collision detection
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    on_platform = False
    for platform in platforms:
        if player_rect.colliderect(platform):
            if player_y < platform.y:
                player_y = platform.top - player_height
                is_jumping = False
                on_platform = True

    # Apply gravity only if not on a platform
    if not on_platform:
        player_y += gravity

    # Drawing
    win.fill(WHITE)
    pygame.draw.rect(win, BLACK, (player_x, player_y, player_width, player_height))
    for platform in platforms:
        pygame.draw.rect(win, BLACK, platform)
    for powerup in powerups:
        pygame.draw.rect(win, RED, powerup)
    # Display score
    score_text = font.render(f"Score: {score}", True, BLACK)
    win.blit(score_text, (10, 10))
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
