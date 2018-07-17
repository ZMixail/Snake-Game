import pygame, random, sys
# Функции
def drawSnake():
    for s in snake:
        pygame.draw.rect(win, GREEN, (s['x'], s['y'], cellSize, cellSize))

def moveSnake():
    if dir == LEFT:
        snake.reverse()
        for n in range(len(snake) - 1):
            snake[n]['x'] = snake[n+1]['x']
            snake[n]['y'] = snake[n+1]['y']
        snake.reverse()
        snake[0]['x'] -= cellSize
    elif dir == RIGHT:
        snake.reverse()
        for n in range(len(snake) - 1):
            snake[n]['x'] = snake[n+1]['x']
            snake[n]['y'] = snake[n+1]['y']
        snake.reverse()
        snake[0]['x'] += cellSize
    elif dir == UP:
        snake.reverse()
        for n in range(len(snake) - 1):
            snake[n]['x'] = snake[n+1]['x']
            snake[n]['y'] = snake[n+1]['y']
        snake.reverse()
        snake[0]['y'] -= cellSize
    elif dir == DOWN:
        snake.reverse()
        for n in range(len(snake) - 1):
            snake[n]['x'] = snake[n+1]['x']
            snake[n]['y'] = snake[n+1]['y']
        snake.reverse()
        snake[0]['y'] += cellSize

def growSnake():
    newSeg = {'x': snake[len(snake) - 1]['x'], 'y': snake[len(snake) - 1]['y']}
    snake.append(newSeg)

def drawApple():
    appleCoords = (apple['x'], apple['y'], cellSize, cellSize)
    pygame.draw.rect(win, RED, appleCoords)

def newApple(snake):
    for seg in snake:
        while apple == seg:
            apple['x'] = getRandom('width')
            apple['y'] = getRandom('height')

def getRandom(axes):
    if axes == 'width':
        return random.randrange(0, WIDTH, cellSize)
    elif axes == 'height':
        return random.randrange(0, HEIGHT, cellSize)

def wallMirror():
    if snake[0]['x'] > WIDTH - cellSize:
        snake[0]['x'] = 0
    elif snake[0]['x'] < 0:
        snake[0]['x'] = WIDTH
    elif snake[0]['y'] > HEIGHT - cellSize:
        snake[0]['y'] = 0
    elif snake[0]['y'] < 0:
        snake[0]['y'] = HEIGHT

def snakeAteItself():
    for s in snake[1:]:
        if s == snake[0]:
            return True
            break

# Цвета
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
BG_COLOR = BLUE
# Вспомогательные переменные
LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'
# Размер одной клетки
cellSize = 20
# Размер окна
WIDTH = cellSize * 45
HEIGHT =  cellSize * 25
# Переменные для змейки
dir = RIGHT
randomCoord = {'x': getRandom('width'), 'y': getRandom('height')}
snake = [{'x': randomCoord['x'], 'y': randomCoord['y']}]
# Переменные для яблочка
apple = {'x': getRandom('width'), 'y': getRandom('height')}
newApple(snake)
# Создание окна
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SNAKE")
# Главный цикл
run = True
while run:
    # Задержка на 0,1 секунды
    pygame.time.delay(100)
    # Управление змейкой (смена направления и т.д.)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_a and dir != RIGHT:
                dir = LEFT
            elif e.key == pygame.K_d and dir != LEFT:
                dir = RIGHT
            elif e.key == pygame.K_w and dir != DOWN:
                dir = UP
            elif e.key == pygame.K_s and dir != UP:
                dir = DOWN
    # Проверка, не съела ли змейка себя
    if snakeAteItself():
        run = False
    # Проверка на съедение яблочка
    if snake[0]['x'] == apple['x'] and snake[0]['y'] == apple['y']:
        growSnake()
        newApple(snake)
    # Если змейка врезается в стену, то она появляется c противоположной стороны
    wallMirror()
    # Движение змейки
    moveSnake()
    # Отрисовка
    win.fill(BG_COLOR)
    drawSnake()
    drawApple()
    # Обновление дисплея
    pygame.display.update()
# Выход из игры
pygame.quit()
sys.exit()
