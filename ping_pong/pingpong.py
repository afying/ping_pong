import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-Понг")

BG = (50, 205, 50)
BLACK = (0,0,0)
BLUE = (0, 0, 145)
RED = (145, 0 ,0)

PADDLE_WIDTH, PADDLE_HEIGHT = 15, 90
BALL_SIZE = 30
PADDLE_SPEED = 7
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
s = -1
ball_image = pygame.image.load('ball.png').convert_alpha()
ball_image = pygame.transform.scale(ball_image, (BALL_SIZE, BALL_SIZE))

def restart_game():
    global player_score, opponent_score, BALL_SPEED_X, BALL_SPEED_Y
    player_score = 0
    opponent_score = 0
    BALL_SPEED_X = 5
    BALL_SPEED_Y = 5
    ball.center = (WIDTH // 2, HEIGHT // 2)
    player_paddle.centery = HEIGHT // 2
    opponent_paddle.centery = HEIGHT // 2

player_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 74)
win_font = pygame.font.Font(None, 100)

but_font = pygame.font.Font(None, 20)
button_rect = pygame.Rect(300, 450, 200, 50)
button_color = (0, 0, 0)
text_color = (255, 255, 255)
text = but_font.render("Нажми для игры снова", True, text_color)

clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()

def reset_ball():
    global BALL_SPEED_X, BALL_SPEED_Y
    ball.center = (WIDTH // 2, HEIGHT // 2)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (player_score >= 5 or opponent_score >= 5) and button_rect.collidepoint(event.pos):
                restart_game()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_paddle.top > 0: player_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and player_paddle.bottom < HEIGHT: player_paddle.y += PADDLE_SPEED
    if keys[pygame.K_UP] and opponent_paddle.top > 0: opponent_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and opponent_paddle.bottom < HEIGHT: opponent_paddle.y += PADDLE_SPEED

    ball.x += BALL_SPEED_X
    ball.y += BALL_SPEED_Y

    seconds = (pygame.time.get_ticks() - start_ticks) / 1000

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        BALL_SPEED_Y *= -1
    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        s -= 0.01
        BALL_SPEED_X *= s

    if ball.left <= 0:
        opponent_score += 1
        reset_ball()
        seconds = 0
        start_ticks = pygame.time.get_ticks()
        BALL_SPEED_X = 5
        BALL_SPEED_Y = 5
        s = -1
    if ball.right >= WIDTH:
        player_score += 1
        reset_ball()
        seconds = 0
        start_ticks = pygame.time.get_ticks()
        BALL_SPEED_X = 5
        BALL_SPEED_Y = 5
        s = -1
    
    screen.fill(BG)
    pygame.draw.rect(screen, BLUE, player_paddle)
    pygame.draw.rect(screen, RED, opponent_paddle)
    pygame.draw.aaline(screen, BLACK, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    screen.blit(ball_image, ball)

    player_text = font.render(str(player_score), True, BLUE)
    screen.blit(player_text, (WIDTH // 4, 20))
    opponent_text = font.render(str(opponent_score), True, RED)
    screen.blit(opponent_text, (3 * WIDTH // 4, 20))
    timer = font.render(str(seconds), True, BLACK)
    screen.blit(timer, (1.75 * WIDTH // 4, 20))

    if player_score >= 5 or opponent_score >= 5:
        BALL_SPEED_X = 0
        BALL_SPEED_Y = 0
        
        if player_score >= 5:
            win_text = win_font.render("ПОБЕДА СИНИХ", True, BLUE)
        else:
            win_text = win_font.render("ПОБЕДА КРАСНЫХ", True, RED)
            
        text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(win_text, text_rect)
        pygame.draw.rect(screen, button_color, button_rect)
        screen.blit(text, (button_rect.x + 25, button_rect.y + 15))

    pygame.display.flip()
    clock.tick(60)