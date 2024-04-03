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

world = [[0] * (SCREEN_HEIGHT // 20) for _ in range(SCREEN_WIDTH // 20)]  # Initialize a basic world grid

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Terraria Basic")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 100
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
                    block_rect = pygame.Rect(col * 20, row * 20, 20, 20)
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

    screen.fill(BROWN)
    player.update(world)
    pygame.draw.rect(screen, BLACK, player.rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
