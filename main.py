import pygame
import sys
import random

# Ініціалізація
pygame.init()

# Налаштування екрану
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Збиралка з сенсорним керуванням")

# Кольори
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Граввець
player_size = 40
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT // 2 - player_size // 2
player_speed = 5

# М'ячі (цілі)
ball_radius = 15
balls = []
score = 0
font = pygame.font.Font(None, 36)

# Змінні для сенсорного керування
touch_pos = None
move_x = 0
move_y = 0

def create_ball():
    x = random.randint(ball_radius, WIDTH - ball_radius)
    y = random.randint(ball_radius, HEIGHT - ball_radius)
    color = random.choice([RED, GREEN, BLUE, YELLOW, PURPLE])
    return {'x': x, 'y': y, 'radius': ball_radius, 'color': color}

# Створюємо початкові м'ячі
for _ in range(10):
    balls.append(create_ball())

# Головний цикл
clock = pygame.time.Clock()
running = True

while running:
    # Обробка подій
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Сенсорне/мишине керування
        if event.type == pygame.MOUSEBUTTONDOWN:
            touch_pos = pygame.mouse.get_pos()
            # Розраховуємо напрямок руху до точки дотику
            dx = touch_pos[0] - (player_x + player_size // 2)
            dy = touch_pos[1] - (player_y + player_size // 2)
            distance = (dx**2 + dy**2)**0.5
            if distance > 0:
                move_x = (dx / distance) * player_speed
                move_y = (dy / distance) * player_speed
            else:
                move_x = 0
                move_y = 0
        
        if event.type == pygame.MOUSEBUTTONUP:
            touch_pos = None
            move_x = 0
            move_y = 0
        
        # Клавіатурне керування (для тестування на ПК)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_x = -player_speed
            elif event.key == pygame.K_RIGHT:
                move_x = player_speed
            elif event.key == pygame.K_UP:
                move_y = -player_speed
            elif event.key == pygame.K_DOWN:
                move_y = player_speed
        
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                move_x = 0
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                move_y = 0
    
    # Рух гравця
    player_x += move_x
    player_y += move_y
    
    # Обмеження руху гравця межами екрану
    player_x = max(0, min(player_x, WIDTH - player_size))
    player_y = max(0, min(player_y, HEIGHT - player_size))
    
    # Перевірка зіткнень з м'ячами
    player_center_x = player_x + player_size // 2
    player_center_y = player_y + player_size // 2
    
    for ball in balls[:]:
        dx = player_center_x - ball['x']
        dy = player_center_y - ball['y']
        distance = (dx**2 + dy**2)**0.5
        
        if distance < player_size // 2 + ball['radius']:
            balls.remove(ball)
            score += 1
            # Створюємо новий м'яч
            balls.append(create_ball())
    
    # Малювання
    screen.fill(WHITE)
    
    # Малюємо м'ячі
    for ball in balls:
        pygame.draw.circle(screen, ball['color'], (ball['x'], ball['y']), ball['radius'])
    
    # Малюємо гравця
    pygame.draw.rect(screen, BLACK, (player_x, player_y, player_size, player_size))
    pygame.draw.rect(screen, RED, (player_x + 5, player_y + 5, player_size - 10, player_size - 10))
    
    # Відображення рахунку
    score_text = font.render(f"Рахунок: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    # Відображення підказки
    if touch_pos:
        hint_text = font.render("Торкніться екрану для руху", True, BLACK)
        screen.blit(hint_text, (WIDTH // 2 - 150, HEIGHT - 40))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()