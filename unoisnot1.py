import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BROWN = (165, 42, 42)

gravity = 0.5
player_speed = 5
jump_strength = 10

block_size = 20

world = []  # Initialize an empty world grid

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Infinitely Generating Platformer")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = 100
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False

    def update(self, world):
        self.vel_y += gravity
        self.on_ground = False
        self.rect.y += self.vel_y
        self.collide_with_blocks(0, self.vel_y, world)
        self.rect.x += self.vel_x
        self.collide_with_blocks(self.vel_x, 0, world)

    def collide_with_blocks(self, dx, dy, world):
        for row in range(len(world)):
            for col in range(len(world[row])):
                if world[row][col] == 1:
                    block_rect = pygame.Rect(col * block_size, row * block_size, block_size, block_size)
                    if self.rect.colliderect(block_rect):
                        if dx > 0:
                            self.rect.right = block_rect.left
                            self.vel_x = 0
                        elif dx < 0:
                            self.rect.left = block_rect.right
                            self.vel_x = 0
                        elif dy > 0:
                            self.rect.bottom = block_rect.top
                            self.vel_y = 0
                            self.on_ground = True
                        elif dy < 0:
                            self.rect.top = block_rect.bottom
                            self.vel_y = 0

player = Player()

# Function to generate a random platform
def generate_platform(width):
    platform = []
    hole_position = random.randint(1, width - 2)
    for i in range(width):
        if i == hole_position:
            platform.append(0)  # No block
        else:
            platform.append(1)  # Block
    return platform

def generate_new_chunk():
    chunk_width = SCREEN_WIDTH // block_size
    return [generate_platform(chunk_width) for _ in range(5)]  # Generate 5 rows of platforms

def shift_world_up():
    world.pop(0)
    world.append(generate_new_chunk())
    player.rect.y -= block_size

# Generate initial chunk
world.append(generate_new_chunk())

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.on_ground:
                player.vel_y = -jump_strength

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.vel_x = -player_speed
    elif keys[pygame.K_RIGHT]:
        player.vel_x = player_speed
    else:
        player.vel_x = 0

    # Move the player
    player.rect.x += player.vel_x

    # Generate new chunk if player reaches the bottom
    if player.rect.bottom >= SCREEN_HEIGHT:
        shift_world_up()

    # Follow player with the camera
    if player.rect.right >= SCREEN_WIDTH:
        player.rect.right = SCREEN_WIDTH
    elif player.rect.left <= 0:
        player.rect.left = 0

    screen.fill(BLACK)
    # Draw world
    for row_idx, row in enumerate(world):
        for col_idx, block in enumerate(row):
            if block == 1:
                pygame.draw.rect(screen, BROWN, (col_idx * block_size, row_idx * block_size, block_size, block_size))

    player.update(world)
    pygame.draw.rect(screen, GREEN, player.rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
