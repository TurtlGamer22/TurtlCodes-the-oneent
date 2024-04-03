import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

gravity = 0.5
game_speed = 10
score = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Runner")
clock = pygame.time.Clock()

class Dinosaur():
    def __init__(self):
        self.rect = pygame.Rect(100, 310, 20, 20) 
        self.jump_vel = -10
        self.jump = False

    def update(self):
        if self.jump:
            self.rect.y += self.jump_vel
            self.jump_vel += gravity
            if self.rect.y > 310:
                self.rect.y = 310
                self.jump = False
                self.jump_vel = -10

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)

    def start_jump(self):
        if not self.jump:
            self.jump = True

class Obstacle():
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH, 310, 20, 20)

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -20: 
            self.rect.x = SCREEN_WIDTH
            global score
            score += 1

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)

dinosaur = Dinosaur()
obstacles = [Obstacle()]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dinosaur.start_jump()

    screen.fill(WHITE)

    dinosaur.update()
    dinosaur.draw(screen)

    for obstacle in obstacles:
        obstacle.update()
        obstacle.draw(screen)
        if dinosaur.rect.colliderect(obstacle.rect): 
            pygame.quit()
            exit()

    score_text = pygame.font.SysFont(None, 30).render(f'Score: {score}', True, BLACK)
    screen.blit(score_text, (650, 10))

    pygame.display.update()
    clock.tick(30) 

pygame.quit()
