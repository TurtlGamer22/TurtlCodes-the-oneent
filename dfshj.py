import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Player settings
player_size = 50
player_pos = [50, SCREEN_HEIGHT - player_size - 100]
player_velocity = 0
gravity = 0.3  # Adjusted gravity for more natural jumps
jump_height = -10  # Adjusted jump height to control jump elevation
on_ground = False
# Enemy settings
enemies = []
enemy_size = 30
enemy_shoot_timer = 90
projectiles = []
projectile_speed = 5
projectile_size = 5

# Game settings
game_speed = 3
score = 0
font = pygame.font.SysFont(None, 55)

# Platform settings
platforms = [[0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100]]
platform_width = 100
platform_height = 20

def jump():
    global player_velocity, on_ground
    if on_ground:  # The player can only jump if they are on the ground
        player_velocity = jump_height
        on_ground = False

def check_platform_collision():
    global player_pos, player_velocity, on_ground
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    for plat in platforms:
        plat_rect = pygame.Rect(plat[0], plat[1], plat[2], plat[3])
        if player_rect.colliderect(plat_rect) and player_velocity >= 0:
            player_pos[1] = plat[1] - player_size
            player_velocity = 0
            on_ground = True
            return

    # Check if player is falling below the screen or going above the window
    if player_pos[1] > SCREEN_HEIGHT:
        game_over()
    elif player_pos[1] < 0:  # Prevent going above the window
        player_pos[1] = 0
        player_velocity = 0

def game_over():
    global running
    game_over_text = font.render('Game Over! Score: ' + str(score), True, WHITE)
    screen.blit(game_over_text, (150, SCREEN_HEIGHT // 2 - 50))
    pygame.display.flip()
    pygame.time.wait(2000)
    running = False

def restart_game():
    global platforms, score, player_pos, on_ground, enemies, projectiles
    player_pos = [50, SCREEN_HEIGHT - player_size - 100]
    platforms = [[0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100]]
    enemies = []
    projectiles = []
    score = 0
    on_ground = False
    main()

def check_collisions():
    global enemies, projectiles, score
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    # Check for collisions with projectiles
    for proj in projectiles:
        if player_rect.colliderect(pygame.Rect(proj[0], proj[1], projectile_size, projectile_size)):
            game_over()
            return
    # Check for defeating enemies
    for enemy in enemies[:]:
        if player_rect.colliderect(pygame.Rect(enemy[0], enemy[1], enemy_size, enemy_size)):
            enemies.remove(enemy)
            score += 50  # Bonus score for defeating enemies

def apply_gravity():
    global player_pos, player_velocity, on_ground
    player_velocity += gravity
    player_pos[1] += player_velocity
    check_platform_collision()

def generate_platforms_and_enemies():
    while platforms[-1][0] < SCREEN_WIDTH + 200:  # Generate ahead
        last_platform = platforms[-1]
        new_platform_x = last_platform[0] + random.randint(150, 250)
        new_platform_y = random.randint(SCREEN_HEIGHT - 300, SCREEN_HEIGHT - 50)
        platforms.append([new_platform_x, new_platform_y, platform_width, platform_height])
        
        # Randomly place enemies on platforms
        if random.randint(0, 4) == 0:  # 1 in 5 chance
            enemies.append([new_platform_x + platform_width // 2 - enemy_size // 2, new_platform_y - enemy_size, enemy_shoot_timer])

def move_world():
    global score, platforms, enemies, projectiles
    # Adjust platform and enemy movement to ensure continuous challenge
    platforms = [plat for plat in platforms if plat[0] + platform_width > -game_speed]
    enemies = [enemy for enemy in enemies if enemy[0] > -enemy_size]
    projectiles[:] = [proj for proj in projectiles if 0 < proj[0] < SCREEN_WIDTH]

    for plat in platforms:
        plat[0] -= game_speed
    for enemy in enemies:
        enemy[0] -= game_speed
        enemy[2] -= 1
        if enemy[2] <= 0:  # Enemy shooting logic
            projectiles.append([enemy[0] + enemy_size / 2, enemy[1] + enemy_size / 2, projectile_speed])
            enemy[2] = enemy_shoot_timer
    for proj in projectiles:
        proj[0] += proj[2]

    score += 1
    if player_pos[0] < 0:  # Check if player gets left behind
        game_over()

def main():
    global running
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                jump()

        apply_gravity()
        move_world()
        generate_platforms_and_enemies()
        check_collisions()

        screen.fill(BLACK)
        for plat in platforms:
            pygame.draw.rect(screen, GREEN, pygame.Rect(plat[0], plat[1], plat[2], plat[3]))
        for enemy in enemies:
            pygame.draw.rect(screen, RED, pygame.Rect(enemy[0], enemy[1], enemy_size, enemy_size))
        for proj in projectiles:
            pygame.draw.circle(screen, BLUE, (int(proj[0]), int(proj[1])), projectile_size)
        pygame.draw.rect(screen, WHITE, pygame.Rect(player_pos[0], player_pos[1], player_size, player_size))

        score_text = font.render('Score: ' + str(score), True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    restart_game()  # Restart game after running becomes False

if __name__ == "__main__":
    main()
