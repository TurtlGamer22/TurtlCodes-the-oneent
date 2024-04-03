import pygame
import random

pygame.init()

screen_width = 720
screen_height = 480
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
paddle_speed = 10
left_score = 0
right_score = 0

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
left_paddle = pygame.Rect(10, screen_height / 2 - 70, 10, 140)
right_paddle = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)

clock = pygame.time.Clock()

def ball_animation():
    global ball_speed_x, ball_speed_y, left_score, right_score
    
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    
    if ball.left <= 0:
        right_score += 1
        ball_restart()
    
    if ball.right >= screen_width:
        left_score += 1
        ball_restart()

    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x *= -1

def ball_restart():
    global ball_speed_x, ball_speed_y
    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))

def paddle_animation():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= paddle_speed
    if keys[pygame.K_s] and left_paddle.bottom < screen_height:
        left_paddle.y += paddle_speed
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= paddle_speed
    if keys[pygame.K_DOWN] and right_paddle.bottom < screen_height:
        right_paddle.y += paddle_speed

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    ball_animation()
    paddle_animation()

    screen.fill(black)
    pygame.draw.rect(screen, white, left_paddle)
    pygame.draw.rect(screen, white, right_paddle)
    pygame.draw.ellipse(screen, white, ball)
    pygame.draw.aaline(screen, white, (screen_width / 2, 0), (screen_width / 2, screen_height))

    left_score_text = pygame.font.Font(None, 74).render(str(left_score), True, white)
    screen.blit(left_score_text, (screen_width / 4, 10))

    right_score_text = pygame.font.Font(None, 74).render(str(right_score), True, white)
    screen.blit(right_score_text, (screen_width * 3 / 4, 10))

    pygame.display.flip()
    clock.tick(60)
