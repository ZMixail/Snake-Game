import pygame as pg
import random

class Snake():
    def __init__(self, color, trail, pos, dir):
        self.color = color
        self.trail = trail
        self.pos = pos
        self.dir = dir
        self.health = 100

    def draw(self):
        pg.draw.rect(field_surf, self.trail,
                     (self.pos[-1]['x'], self.pos[-1]['y'], cell, cell))
        pg.draw.rect(field_surf, self.color,
                     (self.pos[0]['x'], self.pos[0]['y'], cell, cell))
        del self.pos[-1]

    def grow(self):
        self.pos.append(self.pos[-1])
        if snake.health < 100:
            snake.health += 10

    def rainbow(self):
        cur_color = rainbow_colors.index(self.color)
        next_color = cur_color + 1
        if next_color == len(rainbow_colors):
            next_color = 0
        self.color = rainbow_colors[next_color]

    def move(self):
        if self.dir == left:
            new_head = {'x': self.pos[0]['x'] - (cell + l_size),
                        'y': self.pos[0]['y']}
        elif self.dir == right:
            new_head = {'x': self.pos[0]['x'] + (cell + l_size),
                        'y': self.pos[0]['y']}
        elif self.dir == up:
            new_head = {'x': self.pos[0]['x'],
                        'y': self.pos[0]['y'] - (cell + l_size)}
        elif self.dir == down:
            new_head = {'x': self.pos[0]['x'],
                        'y': self.pos[0]['y'] + (cell + l_size)}
        self.pos.insert(0, new_head)

    def mirror(self):
        head = self.pos[0]
        if head['x'] < 0:
            head['x'] = field - cell
        elif head['x'] > field:
            head['x'] = 0
        if head['y'] < 0:
            head['y'] = field - cell
        elif head['y'] > field:
            head['y'] = 0

    def went_beyond(self):
        head = self.pos[0]
        x = head['x']
        y = head['y']
        return x < 0 or x > field or y < 0 or y > field

    def ate_itself(self):
        head = self.pos[0]
        return head in self.pos[2:]

    def get_poisoned(self):
        self.health -= 20

class Apple():
    def __init__(self, color):
        self.color = color
        self.new_pos()

    def draw(self):
        x = self.pos['x']
        y = self.pos['y']
        pg.draw.rect(field_surf, self.color, (x, y, cell, cell))

    def new_pos(self):
        self.pos = {'x': random.randrange(0, field, cell+l_size),
                    'y': random.randrange(0, field, cell+l_size)}
        while self.pos in snake.pos:
            self.pos = {'x': random.randrange(0, field, cell+l_size),
                        'y': random.randrange(0, field, cell+l_size)}


def draw_button(button):
    pos = buttons[button]['text pos']
    pg.draw.rect(screen, bd_color, buttons[button]['edging'])
    buttons[button]['surface'].fill(button_color)
    buttons[button]['surface'].blit(buttons[button]['text'], pos)

def draw_main_menu():
    screen.fill(bg_color)
    draw_button('play')
    draw_button('settings')

def draw_settings():
    screen.fill(bg_color)
    pg.draw.rect(screen, bd_color, s_menu_edge)
    s_menu.fill(menu_color)
    line_num = 0
    for line in s_lines:
        text_pos_y = s_line_height*line_num + text_size*2//3
        s_menu.blit(s_lines[line]['text'], (text_pos_x_1,  text_pos_y))
        if line == 'delay':
            s_menu.blit(numbers[delay], (text_pos_x_2, text_pos_y))
        elif line == 'apples':
            s_menu.blit(numbers[apples_num], (text_pos_x_2, text_pos_y))
        elif s_lines[line]['switch']:
            s_menu.blit(on_text, (text_pos_x_2, text_pos_y))
        else:
            s_menu.blit(off_text, (text_pos_x_2, text_pos_y))
        line_num += 1

def draw_field():
    pg.draw.rect(screen, bd_color, (bd, bd, field + bd*2, field + bd*2))
    field_surf.fill(field_color)
    pg.draw.rect(field_surf, field_color, (cell, cell, field, field))
    for i in range(cell, field, cell + l_size):
        pg.draw.line(field_surf, bd_color, (i, 0), (i, field), l_size)
        pg.draw.line(field_surf, bd_color, (0, i), (field, i), l_size)

def draw_menu():
    pg.draw.rect(screen, bd_color,
                 (field + bd*4, bd, menu + bd*2, field + bd*2))
    menu_surf.fill(menu_color)
    # Score
    score_text = font.render('Score: {}'.format(score), 1, text_color)
    menu_surf.blit(score_text, menu_line[0])
    # Health bar
    if s_lines['poison']['switch']:
        health_bar[2] = int(health_bar_max * snake.health/100)
        pg.draw.rect(menu_surf, bd_color, health_bar_edging)
        if snake.health > 0:
            pg.draw.rect(menu_surf, health_color, health_bar)


def start_new_game():
    global snake, apples, score, score_text

    pg.mouse.set_visible(False)

    pos = [{'x': random.randrange(0, field*2//3, cell + l_size),
            'y': random.randrange(0, field, cell + l_size)}]
    if s_lines['trail']['switch']:
        snake = Snake(snake_color, trail_color, pos, dir)
    else:
        snake = Snake(snake_color, field_color, pos, dir)

    apples = []
    if s_lines['phantom']['switch']:
        color = phantom_color
    elif s_lines['poison']['switch']:
        color = poison_color
    else:
        color = red
    for i in range(apples_num):
        apples.append(Apple(color))

    score = 0
    score_text = font.render('Score: {}'.format(score), True, text_color)

    screen.fill(bg_color)
    draw_field()
    draw_menu()
    if not s_lines['phantom']['switch']:
        for apple in apples:
            apple.draw()

def end_game(cause_text):
    global game
    pg.mouse.set_visible(True)
    game = False
    if s_lines['phantom']['switch']:
        for apple in apples:
            apple.draw()
    if s_lines['poison']['switch']:
        pg.draw.rect(menu_surf, bd_color, health_bar_edging)
    menu_surf.blit(gameover_text, menu_line[1])
    menu_surf.blit(cause_text, menu_line[2])
    menu_surf.blit(new_game_text, menu_line[3])

def in_rect(dot, rect):
    rect = (rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3])
    cond_1 = dot[0] > rect[0] and dot[0] < rect[2]
    cond_2 = dot[1] >= rect[1] and dot[1] <= rect[3]
    return cond_1 and cond_2


jacarta  = (68, 53, 91)
toledo   = (49, 38, 62)
black    = (34, 30, 34) # Black Russian
yellow   = (236, 167, 44)
orange   = (238, 86, 34) # Outrageous Orange
red      = (254, 26, 26) # Torch Red or Scarlet
green    = (118, 220, 20)
aqua     = (0, 255, 255)
sapphire = (15, 82, 186)
purple   = (214, 54, 201)

rainbow_colors = (red, orange, yellow, green, aqua, sapphire, purple)
bg_color = jacarta
bd_color = black
field_color = toledo
menu_color = yellow
button_color = orange
text_color = black
snake_color = yellow
trail_color = jacarta
phantom_color = purple
poison_color = aqua
health_color = red

left = 'left'
right = 'right'
up = 'up'
down = 'down'

dir = right

main_menu = True
settings = False
game = False # Game menu
phantom = False
poison = False
mirror = False
rainbow = False
trail = False

score = 0
delay = 100
apples_num = 5
poison_chance = 50
max_number = 501
s_lines_num = 7

cells_in_line = 30
cell = 30
l_size = 2

field = cell*cells_in_line + l_size*(cells_in_line - 1)
menu = field//2
bd = cell//2
width = field + menu + bd*7
height = field + bd*4
text_size = cell
text_pos_x_1 = cell
text_pos_x_2 = cell + menu//2
s_line_height = text_size*3
s_pos_x = (width - menu)//2
s_pos_y = height//2 - s_line_height*s_lines_num//2
s_menu_edge = (s_pos_x - bd, s_pos_y - bd,
               menu + bd*2, s_line_height*s_lines_num + bd*2)
health_bar = [int(bd*1.5), int(field - bd*2.5),
              menu - bd*3, bd]
health_bar_max = menu - bd*3
health_bar_edging = (bd, field - bd*3, menu - bd*2, bd*2)

buttons = {'play': {'rect': (width//3, height//3,
                             width//3, height//9),
                    'text pos': (width//8, bd)},
           'settings': {'rect': (width//3, height*5//9,
                                 width//3, height//9),
                        'text pos': (width//12, bd)}}

for button in buttons:
    buttons[button]['edging'] = (buttons[button]['rect'][0] - bd,
                                 buttons[button]['rect'][1] - bd,
                                 buttons[button]['rect'][2] + bd*2,
                                 buttons[button]['rect'][3] + bd*2)

s_lines = {'phantom': {'switch': phantom},
           'poison': {'switch': poison},
           'mirror': {'switch': mirror},
           'rainbow': {'switch': rainbow},
           'trail': {'switch': trail},
           'delay': {},
           'apples': {}}

line_num = 0
for line in s_lines:
    s_lines[line]['pos'] = (s_pos_x,
                            s_pos_y + (s_line_height + 0.5)*line_num,
                            menu, s_line_height)
    s_lines[line]['color'] = button_color
    line_num += 1

menu_lines_num = 4
menu_line = []
for i in range(menu_lines_num):
    menu_line.append((bd, text_size*i + bd*(i + 1)))

# Path to file
alata_path = 'Alata-Regular.ttf'

# Initialization of surfaces and texts
pg.init()
screen = pg.display.set_mode((width, height))
pg.display.set_caption('Snake')
buttons['play']['surface'] = pg.Surface.subsurface(screen, buttons['play']['rect'])
buttons['settings']['surface'] = pg.Surface.subsurface(screen, buttons['settings']['rect'])
s_menu = pg.Surface.subsurface(screen, (s_pos_x, s_pos_y, menu,
                                               s_line_height*s_lines_num))
field_surf = pg.Surface.subsurface(screen, (bd*2, bd*2, field, field))
menu_surf = pg.Surface.subsurface(screen, (field + bd*5, bd*2, menu, field))

font = pg.font.Font(alata_path, text_size)
main_menu_font = pg.font.Font(alata_path, text_size*2)
gameover_text = font.render('Game over!', True, text_color)
ate_itself_text = font.render('You have ate yourself...', True, text_color)
went_beyond_text = font.render('You have went beyond...', True, text_color)
poison_text = font.render('You have died from poison...', True, text_color)
new_game_text = font.render('Press F to start the new game', True, text_color)
on_text = font.render('ON', True, text_color)
off_text = font.render('OFF', True, text_color)
buttons['play']['text'] = main_menu_font.render('PLAY', True, text_color)
buttons['settings']['text'] = main_menu_font.render('SETTINGS', True, text_color)
s_lines['phantom']['text'] = font.render('Phantom: ', True, text_color)
s_lines['poison']['text'] = font.render('Poison: ', True, text_color)
s_lines['mirror']['text'] = font.render('Mirror: ', True, text_color)
s_lines['rainbow']['text'] = font.render('Rainbow: ', True, text_color)
s_lines['trail']['text'] = font.render('Trail: ', True, text_color)
s_lines['delay']['text'] = font.render('Delay: ', True, text_color)
s_lines['apples']['text'] = font.render('Apples num: ', True, text_color)
numbers = []
for i in range(max_number):
    numbers.append(font.render(str(i), True, text_color))

run = True
while run:
    pg.time.delay(delay)
    mouse = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.KEYDOWN:
            if game:
                if event.key == pg.K_a and snake.dir != right:
                    snake.dir = left
                    break
                elif event.key == pg.K_d and snake.dir != left:
                    snake.dir = right
                    break
                elif event.key == pg.K_w and snake.dir != down:
                    snake.dir = up
                    break
                elif event.key == pg.K_s and snake.dir != up:
                    snake.dir = down
                    break
            if event.key == pg.K_q:
                run = False
            elif event.key == pg.K_ESCAPE:
                pg.mouse.set_visible(True)
                game = False
                main_menu = True
                settings = False
            elif event.key == pg.K_f:
                game = True
                main_menu = False
                settings = False
                start_new_game()
        elif event.type == pg.MOUSEBUTTONDOWN:
            if main_menu:
                for button in buttons:
                    if in_rect(mouse, buttons[button]['rect']):
                        if button == 'play':
                            main_menu = False
                            game = True
                            start_new_game()
                        elif button == 'settings':
                            main_menu = False
                            settings = True
            elif settings:
                line_num = 0
                for line in s_lines:
                    if in_rect(mouse, s_lines[line]['pos']):
                        if line == 'delay':
                            # Mouse wheel up
                            if event.button == 4:
                                if delay + 5 < max_number:
                                    delay += 5
                            # Mouse wheel down
                            elif event.button == 5:
                                if delay > 0:
                                    delay -= 5
                        elif line == 'apples':
                            # Mouse wheel up
                            if event.button == 4:
                                if apples_num + 1 < max_number:
                                    apples_num += 1
                            # Mouse wheel down
                            elif event.button == 5:
                                if apples_num > 0:
                                    apples_num -= 1
                        elif s_lines[line]['switch']:
                            s_lines[line]['switch'] = False
                        else:
                            s_lines[line]['switch'] = True
                    line_num += 1
    if game:
        snake.move()
        if snake.went_beyond() and s_lines['mirror']['switch']:
            snake.mirror()
        if snake.went_beyond():
            end_game(cause_text = went_beyond_text)
        elif snake.ate_itself():
            end_game(cause_text = ate_itself_text)
        else:
            if s_lines['rainbow']['switch']:
                snake.rainbow()
            snake.draw()
            for apple in apples:
                if snake.pos[0] == apple.pos:
                    score += 1
                    apple.new_pos()
                    apple.draw()
                    draw_menu()
                    poison_rand = random.randrange(100)
                    if s_lines['poison']['switch']:
                        if poison_rand < poison_chance:
                            snake.get_poisoned()
                            score -= 1
                            draw_menu()
                            if snake.health <= 0:
                                end_game(cause_text = poison_text)
                        else:
                            snake.grow()
                    else:
                        snake.grow()
    elif main_menu:
        draw_main_menu()
    elif settings:
        draw_settings()
    pg.display.update()

pg.quit()
print('Final score: {}'.format(score))
