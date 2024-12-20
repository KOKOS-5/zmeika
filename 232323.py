import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы экрана
WIDTH = 600
HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()


# Класс змейки
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.grow = False

    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.insert(0, new_head)

        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def set_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def draw(self, surf):
        for x, y in self.body:
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surf, GREEN, rect)

    def check_collision(self):
        head_x, head_y = self.body[0]
        if (head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT or self.body[0] in self.body[1:]):
            return True
        else:
            return False


# Класс еды
class Food:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, GRID_SIZE, GRID_SIZE)
        self.update()

    def get_random_pos(self):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in snake.body:
                return (x * GRID_SIZE, y * GRID_SIZE)

    def update(self):
        x, y = self.get_random_pos()
        self.rect.x = x
        self.rect.y = y


# Создание объектов
snake = Snake()
food = Food()

score = 0
font = pygame.font.Font(None, 36)
game_over = False


def draw_score(surf, score):
    text_surf = font.render(f"Счет: {score}", True, BLACK)
    surf.blit(text_surf, (10, 10))


def game_over_screen(surf):
    text_surf = font.render(f"ИГРА ОКОНЧЕНА", True, BLACK)
    surf.blit(text_surf, (WIDTH // 2 - 100, HEIGHT // 2 - 20))


# Основной игровой цикл
running = True
while running:
    clock.tick(FPS)

    if not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake.set_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.set_direction((1, 0))
                elif event.key == pygame.K_UP:
                    snake.set_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.set_direction((0, 1))

        # Движение змейки
        snake.move()

        # Проверка столкновения со едой
        if snake.body[0][0] * GRID_SIZE == food.rect.x and snake.body[0][1] * GRID_SIZE == food.rect.y:
            snake.grow = True
            food.update()
            score += 1

        # Проверка столкновения
        if snake.check_collision():
            game_over = True

        # Отрисовка
        screen.fill(WHITE)
        snake.draw(screen)
        pygame.draw.rect(screen, RED, food.rect)
        draw_score(screen, score)
        pygame.display.flip()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                game_over = False
                snake = Snake()
                food = Food()
                score = 0

        screen.fill(RED)
        game_over_screen(screen)
        pygame.display.flip()

pygame.quit()