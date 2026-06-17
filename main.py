import pygame
import random
import sys

# Ініціалізація
pygame.init()

# Налаштування екрану
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Збирач - Сенсорна гра")

# Кольори
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Клас гравця
class Player:
    def __init__(self):
        self.size = 40
        self.x = WIDTH // 2 - self.size // 2
        self.y = HEIGHT - 100
        self.speed = 8
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.target_x = self.x
        self.target_y = self.y
        
    def move_to(self, target_x, target_y):
        self.target_x = target_x - self.size // 2
        self.target_y = target_y - self.size // 2
        
    def update(self):
        # Плавне переміщення до цілі
        dx = self.target_x - self.rect.x
        dy = self.target_y - self.rect.y
        distance = (dx**2 + dy**2)**0.5
        
        if distance > 1:
            if distance < self.speed:
                self.rect.x = self.target_x
                self.rect.y = self.target_y
            else:
                self.rect.x += (dx / distance) * self.speed
                self.rect.y += (dy / distance) * self.speed
        
        # Обмеження в межах екрану
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.size))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.size))
        
    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 3)

# Клас предмета
class Item:
    def __init__(self):
        self.size = 30
        self.x = random.randint(0, WIDTH - self.size)
        self.y = random.randint(0, HEIGHT - 150)
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.color = random.choice([RED, GREEN, YELLOW, ORANGE, PURPLE])
        self.speed = 2
        
    def update(self):
        self.rect.y += self.speed
        # Якщо предмет вийшов за екран - переміщуємо вгору
        if self.rect.y > HEIGHT:
            self.rect.y = -self.size
            self.rect.x = random.randint(0, WIDTH - self.size)
            self.color = random.choice([RED, GREEN, YELLOW, ORANGE, PURPLE])
            
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.size // 2)
        pygame.draw.circle(screen, WHITE, self.rect.center, self.size // 2, 2)

# Клас бонуса
class Bonus:
    def __init__(self):
        self.size = 20
        self.x = random.randint(0, WIDTH - self.size)
        self.y = random.randint(0, HEIGHT - 150)
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.speed = 1
        self.active = False
        self.timer = 0
        
    def spawn(self):
        if not self.active and random.random() < 0.005:  # 0.5% шанс появи
            self.active = True
            self.x = random.randint(0, WIDTH - self.size)
            self.y = -self.size
            self.rect.x = self.x
            self.rect.y = self.y
            self.timer = 300  # 5 секунд при 60 FPS
            
    def update(self):
        if self.active:
            self.rect.y += self.speed
            self.timer -= 1
            if self.timer <= 0 or self.rect.y > HEIGHT:
                self.active = False
                
    def draw(self, screen):
        if self.active:
            pygame.draw.circle(screen, WHITE, self.rect.center, self.size // 2)
            pygame.draw.circle(screen, BLACK, self.rect.center, self.size // 2, 2)
            # Малюємо зірочку
            font = pygame.font.Font(None, 24)
            text = font.render("★", True, YELLOW)
            screen.blit(text, (self.rect.x + 2, self.rect.y - 2))

# Клас гри
class Game:
    def __init__(self):
        self.player = Player()
        self.items = [Item() for _ in range(8)]
        self.bonus = Bonus()
        self.score = 0
        self.high_score = 0
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.running = True
        self.clock = pygame.time.Clock()
        self.touch_active = False
        
        # Завантажуємо рекорд
        try:
            with open("highscore.txt", "r") as f:
                self.high_score = int(f.read())
        except:
            self.high_score = 0
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.VIDEORESIZE:
                global WIDTH, HEIGHT
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                
            # Сенсорне керування (для мобільних пристроїв)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Ліва кнопка миші або дотик
                    self.touch_active = True
                    self.player.move_to(event.pos[0], event.pos[1])
                    
            elif event.type == pygame.MOUSEMOTION:
                if self.touch_active and pygame.mouse.get_pressed()[0]:
                    self.player.move_to(event.pos[0], event.pos[1])
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.touch_active = False
                    
            # Клавіатура (для десктопа)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.rect.x -= self.player.speed * 3
                elif event.key == pygame.K_RIGHT:
                    self.player.rect.x += self.player.speed * 3
                elif event.key == pygame.K_UP:
                    self.player.rect.y -= self.player.speed * 3
                elif event.key == pygame.K_DOWN:
                    self.player.rect.y += self.player.speed * 3
                    
    def update(self):
        self.player.update()
        
        # Оновлення предметів
        for item in self.items[:]:
            item.update()
            
            # Перевірка колізії з гравцем
            if self.player.rect.colliderect(item.rect):
                self.items.remove(item)
                self.items.append(Item())
                self.score += 1
                
        # Оновлення бонусу
        self.bonus.spawn()
        self.bonus.update()
        
        # Перевірка колізії з бонусом
        if self.bonus.active and self.player.rect.colliderect(self.bonus.rect):
            self.bonus.active = False
            self.score += 5
            
        # Оновлення рекорду
        if self.score > self.high_score:
            self.high_score = self.score
            with open("highscore.txt", "w") as f:
                f.write(str(self.high_score))
                
    def draw(self):
        screen.fill(BLACK)
        
        # Малюємо сітку для краси
        for x in range(0, WIDTH, 50):
            pygame.draw.line(screen, (20, 20, 20), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, 50):
            pygame.draw.line(screen, (20, 20, 20), (0, y), (WIDTH, y))
        
        # Малюємо об'єкти
        for item in self.items:
            item.draw(screen)
            
        self.bonus.draw(screen)
        self.player.draw(screen)
        
        # Малюємо текст
        score_text = self.font.render(f"Рахунок: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        high_text = self.small_font.render(f"Рекорд: {self.high_score}", True, WHITE)
        screen.blit(high_text, (10, 50))
        
        # Інструкція
        if self.score < 5:
            help_text = self.small_font.render("Торкніться екрану або переміщуйте палець", True, (100, 100, 100))
            screen.blit(help_text, (WIDTH // 2 - 150, HEIGHT - 30))
        
        pygame.display.flip()
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
            
        pygame.quit()
        sys.exit()

# Запуск гри
if __name__ == "__main__":
    game = Game()
    game.run()