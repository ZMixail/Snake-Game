import pygame as pg
import random

class Interface():
    def __init__(self, bg_color, border_color, field_color, menu_color, button_color):
        self.bg_color = bg_color
        self.border_color = border_color
        self.field_color = field_color
        self.menu_color = menu_color
        self.button_color = button_color

    def draw_button(self, button):
        pos = buttons[button]['text pos']
        pg.draw.rect(screen, self.border_color, buttons[button]['edging'])
        buttons[button]['surface'].fill(button_color)
        buttons[button]['surface'].blit(buttons[button]['text'], pos)

    def main_menu(self):
        screen.fill(self.bg_color)
        interface.draw_button('play')
        interface.draw_button('settings')

    def settings(self):
        screen.fill(self.bg_color)
        pg.draw.rect(screen, self.border_color, settings_menu_edging)
        settings_menu.fill(self.menu_color)
        line_num = 0
        for line in settings_lines:
            text_pos_y = s_line_height*line_num + (text_size*2)//3
            settings_menu.blit(settings_lines[line]['text'], (text_pos_x_1,  text_pos_y))
            if line == 'delay':
                settings_menu.blit(numbers[delay], (text_pos_x_2, text_pos_y))
            elif line == 'apples':
                settings_menu.blit(numbers[apples_num], (text_pos_x_2, text_pos_y))
            elif settings_lines[line]['switch']:
                settings_menu.blit(on_text, (text_pos_x_2, text_pos_y))
            else:
                settings_menu.blit(off_text, (text_pos_x_2, text_pos_y))
            line_num += 1

    def draw_field(self):
        pg.draw.rect(screen, self.border_color, (border, border, field + border*2, field + border*2))
        field_surface.fill(self.field_color)
        pg.draw.rect(field_surface, self.field_color, (cell, cell, field, field))
        for i in range(cell, field, cell + line_size):
            pg.draw.line(field_surface, self.border_color, (i, 0), (i, field), line_size)
            pg.draw.line(field_surface, self.border_color, (0, i), (field, i), line_size)

    def draw_menu(self):
        pg.draw.rect(screen, self.border_color, (field + border*4, border, menu + border*2, field + border*2))
        menu_surface.fill(self.menu_color)
        menu_surface.blit(score_text, menu_line[0])

    def gameover(self):
        menu_surface.blit(gameover_text, menu_line[1])
        menu_surface.blit(cause_text, menu_line[2])
        menu_surface.blit(new_game_text, menu_line[3])

class Snake():
    def __init__(self, color, trail, pos, dir):
        self.color = color
        self.trail = trail
        self.pos = pos
        self.dir = dir

    def draw(self):
        pg.draw.rect(field_surface, self.trail, (self.pos[-1]['x'], self.pos[-1]['y'], cell, cell))
        pg.draw.rect(field_surface, self.color, (self.pos[0]['x'], self.pos[0]['y'], cell, cell))
        del self.pos[-1]

    def grow(self):
        self.pos.append(self.pos[-1])

    def rainbow(self):
        cur_color = rainbow_colors.index(self.color)
        next_color = cur_color + 1
        if next_color == len(rainbow_colors):
            next_color = 0
        self.color = rainbow_colors[next_color]

    def move(self):
        if self.dir == left:
            new_head = {'x': self.pos[0]['x'] - (cell + line_size),
                        'y': self.pos[0]['y']}
        elif self.dir == right:
            new_head = {'x': self.pos[0]['x'] + (cell + line_size),
                        'y': self.pos[0]['y']}
        elif self.dir == up:
            new_head = {'x': self.pos[0]['x'],
                        'y': self.pos[0]['y'] - (cell + line_size)}
        elif self.dir == down:
            new_head = {'x': self.pos[0]['x'],
                        'y': self.pos[0]['y'] + (cell + line_size)}
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
        return head['x'] < 0 or head['x'] > field or head['y'] < 0 or head['y'] > field

    def ate_itself(self):
        head = self.pos[0]
        return head in self.pos[2:]

class Apple():
    def __init__(self, color):
        self.color = color
        self.new_pos()

    def draw(self):
        pg.draw.rect(field_surface, self.color, (self.pos['x'], self.pos['y'], cell, cell))

    def new_pos(self):
        self.pos = {'x': random.randrange(0, field, cell + line_size),
                    'y': random.randrange(0, field, cell + line_size)}
        while self.pos in snake.pos:
            self.pos = {'x': random.randrange(0, field, cell + line_size),
                        'y': random.randrange(0, field, cell + line_size)}


def start_new_game():
    global start, interface, snake, apples, score, score_text

    pg.mouse.set_visible(False)

    if settings_lines['trail']['switch']:
        trail_color = lightblue
    else:
        trail_color = interface.field_color
    pos = [{'x': random.randrange(0, field*2//3, cell + line_size),
            'y': random.randrange(0, field, cell + line_size)}]
    snake = Snake(snake_color, trail_color, pos, dir)

    apples = []
    if settings_lines['phantom']['switch']:
        color = phantom_color
    else:
        color = red
    for i in range(apples_num):
        apples.append(Apple(color))

    score = 0
    score_text = font.render('Score: {}'.format(score), True, white)

    screen.fill(interface.bg_color)
    interface.draw_field()
    interface.draw_menu()
    if not settings_lines['phantom']['switch']:
        for apple in apples:
            apple.draw()

def end_game():
    global game
    pg.mouse.set_visible(True)
    game = False
    if settings_lines['phantom']['switch']:
        for apple in apples:
            apple.draw()
    interface.gameover()

def in_rect(dot, rect):
    rect = (rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3])
    return (dot[0] > rect[0] and dot[0] < rect[2]) and (dot[1] >= rect[1] and dot[1] <= rect[3])


black     = (0, 0, 0)
red       = (254, 26, 26)
green     = (118, 220, 20)
blue      = (15, 82, 186)
lightblue = (14, 77, 148)
grey      = (42, 43, 46)
darkgrey  = (20, 21, 24)
brown     = (101, 53, 15)
orange    = (255, 165, 0)
cyan      = (0, 255, 255)
purple    = (214, 54, 201)
yellow    = (255, 255, 0)
white     = (255, 255, 255)

rainbow_colors = (red, orange, yellow, green, cyan, purple)
bg_color = brown
border_color = black
field_color = blue
menu_color = grey
button_color = grey
select_color = darkgrey
text_color = white
snake_color = green
trail_color = lightblue
phantom_color = purple

left = 'left'
right = 'right'
up = 'up'
down = 'down'

dir = right

main_menu = True
settings = False
game = False # Game menu
phantom = False
mirror = False
rainbow = False
trail = False

score = 0
delay = 100
apples_num = 5
max_number = 501

cells_in_line = 30
cell = 30
line_size = 2

field = cell*cells_in_line + line_size*(cells_in_line - 1)
menu = field//2
border = cell//2
width = field + menu + border*7
height = field + border*4
text_size = cell
text_pos_x_1 = cell
text_pos_x_2 = cell + menu//2
s_line_height = text_size*3
settings_pos = (width - menu)//2
settings_menu_edging = (settings_pos - border, border, menu + border*2, field + border*2)


buttons = {'play': {'rect': (width//3, height//3, width//3, height//9),
                    'text pos': (width//8, border)},
           'settings': {'rect': (width//3, height*5//9, width//3, height//9),
                        'text pos': (width//12, border)}}

for button in buttons:
    buttons[button]['edging'] = (buttons[button]['rect'][0] - border,
                                 buttons[button]['rect'][1] - border,
                                 buttons[button]['rect'][2] + border*2,
                                 buttons[button]['rect'][3] + border*2)

settings_lines = {'phantom': {'switch': phantom},
                  'mirror': {'switch': mirror},
                  'rainbow': {'switch': rainbow},
                  'trail': {'switch': trail},
                  'delay': {},
                  'apples': {}}
line_num = 0
for line in settings_lines:
    settings_lines[line]['pos'] = (settings_pos, border*2 + (s_line_height + 0.5)*line_num, menu, s_line_height)
    settings_lines[line]['color'] = button_color
    line_num += 1

menu_lines_num = 4
menu_line = []
for i in range(menu_lines_num):
    menu_line.append((border, text_size*i + border*(i + 1)))

pg.init()
screen = pg.display.set_mode((width, height))
pg.display.set_caption('Snake')
buttons['play']['surface'] = pg.Surface.subsurface(screen, buttons['play']['rect'])
buttons['settings']['surface'] = pg.Surface.subsurface(screen, buttons['settings']['rect'])
settings_menu = pg.Surface.subsurface(screen, (settings_pos, border*2, menu, field))
field_surface = pg.Surface.subsurface(screen, (border*2, border*2, field, field))
menu_surface = pg.Surface.subsurface(screen, (field + border*5, border*2, menu, field))

font = pg.font.Font('Alata-Regular.ttf', text_size)
main_menu_font = pg.font.Font('Alata-Regular.ttf', text_size*2)
gameover_text = font.render('Game over!', True, text_color)
ate_itself_text = font.render('You ate yourself...', True, text_color)
went_beyond_text = font.render('You went beyond...', True, text_color)
new_game_text = font.render('Press F to start the new game', True, text_color)
on_text = font.render('ON', True, text_color)
off_text = font.render('OFF', True, text_color)
buttons['play']['text'] = main_menu_font.render('PLAY', True, text_color)
buttons['settings']['text'] = main_menu_font.render('SETTINGS', True, text_color)
settings_lines['phantom']['text'] = font.render('Phantom: ', True, text_color)
settings_lines['mirror']['text'] = font.render('Mirror: ', True, text_color)
settings_lines['rainbow']['text'] = font.render('Rainbow: ', True, text_color)
settings_lines['trail']['text'] = font.render('Trail: ', True, text_color)
settings_lines['delay']['text'] = font.render('Delay: ', True, text_color)
settings_lines['apples']['text'] = font.render('Apples num: ', True, text_color)
numbers = []
for i in range(max_number):
    numbers.append(font.render(str(i), True, text_color))

interface = Interface(bg_color, border_color, field_color, menu_color, button_color)

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
                        if event.type == pg.MOUSEBUTTONDOWN:
                            if button == 'play':
                                main_menu = False
                                game = True
                                start_new_game()
                            elif button == 'settings':
                                main_menu = False
                                settings = True
            elif settings:
                line_num = 0
                for line in settings_lines:
                    if in_rect(mouse, settings_lines[line]['pos']):
                        if line == 'delay':
                            if event.button == 4 and delay + 5 < max_number: # Mouse wheel up
                                delay += 5
                            elif event.button == 5 and delay > 0: # Mouse wheel down
                                delay -= 5
                        elif line == 'apples':
                            if event.button == 4 and apples_num + 1 < max_number: # Mouse wheel up
                                apples_num += 1
                            elif event.button == 5 and apples_num > 0: # Mouse wheel down
                                apples_num -= 1
                        elif settings_lines[line]['switch']:
                            settings_lines[line]['switch'] = False
                        else:
                            settings_lines[line]['switch'] = True
                    line_num += 1
    if game:
        snake.move()
        if snake.went_beyond() and settings_lines['mirror']['switch']:
            snake.mirror()
        if snake.went_beyond():
            cause_text = went_beyond_text
            end_game()
        elif snake.ate_itself():
            cause_text = ate_itself_text
            end_game()
        else:
            if settings_lines['rainbow']['switch']:
                snake.rainbow()
            snake.draw()
            for apple in apples:
                if snake.pos[0] == apple.pos:
                    snake.grow()
                    apple.new_pos()
                    apple.draw()
                    score += 1
                    score_text = font.render('Score: {}'.format(score), 1, white)
                    interface.draw_menu()
    elif main_menu:
        interface.main_menu()
    elif settings:
        interface.settings()
    pg.display.update()

pg.quit()
print('Final score: {}'.format(score))
