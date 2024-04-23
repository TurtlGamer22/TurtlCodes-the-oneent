import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 480
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PLATFORM_WIDTH = 80
PLATFORM_HEIGHT = 20
PLATFORM_COLOR = (255, 255, 255)
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
GRAVITY = 0.5
PLATFORM_GAP = 150

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Jump")
clock = pygame.time.Clock()

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.vel_y = 0

    def update(self):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0

    def jump(self):
        self.vel_y = -10

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Function to generate platforms
def create_platforms():
    platforms = pygame.sprite.Group()
    for i in range(7):
        platform = Platform(random.randint(0, WIDTH - PLATFORM_WIDTH),
                            random.randint(i * PLATFORM_GAP, (i + 1) * PLATFORM_GAP))
        platforms.add(platform)
    return platforms

# Sprite groups
all_sprites = pygame.sprite.Group()
platforms = create_platforms()
player = Player()
all_sprites.add(player)
all_sprites.add(platforms)

# Game loop
running = True
while running:
    # Keep loop running at the right speed
    clock.tick(FPS)

    # Process input/events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    # Update
    all_sprites.update()

    # Check if player hits platform
    hits = pygame.sprite.spritecollide(player, platforms, False)
    if hits:
        player.rect.bottom = hits[0].rect.top
        player.vel_y = 0

    # Scroll platforms upward
    for platform in platforms:
        platform.rect.y += player.vel_y
        if platform.rect.top > HEIGHT:
            platform.rect.bottom = 0
            platform.rect.x = random.randint(0, WIDTH - PLATFORM_WIDTH)

    # Draw/render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
