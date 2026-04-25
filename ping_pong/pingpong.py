import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-Понг")

BG = (173, 216, 230)
BLACK = (0,0,0)
BLUE = (0, 0, 145)
RED = (145, 0 ,0)

PADDLE_WIDTH, PADDLE_HEIGHT = 15, 90
BALL_SIZE = 30
PADDLE_SPEED = 7
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# ЗАГРУЗКА КАРТИНКИ
try:
    ball_image = pygame.image.load('ball.png').convert_alpha()
    ball_image = pygame.transform.scale(ball_image, (BALL_SIZE, BALL_SIZE))
except:
    print("Файл ball.png не найден! Будет использован белый круг.")
    ball_image = None

player_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 74)
win_font = pygame.font.Font(None, 100)

clock = pygame.time.Clock()

def reset_ball():
    global BALL_SPEED_X, BALL_SPEED_Y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    BALL_SPEED_X *= -1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_paddle.top > 0: player_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and player_paddle.bottom < HEIGHT: player_paddle.y += PADDLE_SPEED
    if keys[pygame.K_UP] and opponent_paddle.top > 0: opponent_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and opponent_paddle.bottom < HEIGHT: opponent_paddle.y += PADDLE_SPEED

    ball.x += BALL_SPEED_X
    ball.y += BALL_SPEED_Y

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        BALL_SPEED_Y *= -1
    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        BALL_SPEED_X *= -1

    if ball.left <= 0:
        opponent_score += 1
        reset_ball()
    if ball.right >= WIDTH:
        player_score += 1
        reset_ball()

    screen.fill(BG)
    pygame.draw.rect(screen, BLUE, player_paddle)
    pygame.draw.rect(screen, RED, opponent_paddle)
    pygame.draw.aaline(screen, BLACK, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # ОТРИСОВКА КАРТИНКИ МЯЧА
    if ball_image:
        screen.blit(ball_image, ball)
    else:
        pygame.draw.ellipse(screen, WHITE, ball)

    player_text = font.render(str(player_score), True, BLUE)
    screen.blit(player_text, (WIDTH // 4, 20))
    opponent_text = font.render(str(opponent_score), True, RED)
    screen.blit(opponent_text, (3 * WIDTH // 4, 20))

    if player_score == 5:
        win_text = win_font.render("ПОБЕДА СИНИХ", True, BLUE)
        text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(win_text, text_rect)
        pygame.display.flip()
        BALL_SPEED_X = 0
        BALL_SPEED_Y = 0
    if opponent_score == 5:
        win_text = win_font.render("ПОБЕДА КРАСНЫХ", True, RED)
        text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(win_text, text_rect)
        pygame.display.flip()
        BALL_SPEED_X = 0
        BALL_SPEED_Y = 0

    pygame.display.flip()
    clock.tick(60)