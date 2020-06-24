import random, pygame

pygame.init()
pygame.font.init()

screen_width = 800
screen_height = 700
play_width = 300
play_height = 600
block_size = 30  # each little square
background_colour = (0, 0, 0)

# coordinates of top left point
top_x = (screen_width - play_width)/2
top_y = (screen_height - play_height)


S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colours = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

class Piece:

    ''' Shape object with position coordinates, colour and rotation '''

    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.colour = shape_colours[shapes.index(shape)]
        self.rotation = 0
    
def create_grid(locked_positions={}):
    
    ''' Creates grid object, colors squares depending if taken or empty '''

    grid = [[(0, 0, 0) for x in range(10)] for y in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                grid[i][j] = locked_positions[(j, i)]

    return grid

def get_shape(shapes):

    ''' Returns random shape at center of grid '''

    return Piece(5, 0, random.choice(shapes))

def draw_text(surface, message, colour, size):

    ''' Draws given message at center of screen '''

    f = pygame.font.SysFont('arial', size, bold=True)
    label = f.render(message, 1, colour)
    surface.blit(label, (top_x + play_width/2 - label.get_width()/2, top_y + play_height/2 - label.get_height()/2 - 50))

def draw_grid(surface, grid):
    
    ''' Draws the grey gridlines '''

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (top_x, top_y + i * block_size), (top_x + play_width, top_y + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (top_x + j * block_size, top_y), (top_x + j * block_size, top_y + play_height))

def clear_rows(grid, locked_positions={}):

    ''' Clears complete rows and shits above rows downwards '''

    increment = 0
    ind = 0
    for i in range(len(grid) -1, -1, -1):
        if (0, 0, 0) not in grid[i]:
            ind = i
            increment += 1
            for j in range(len(grid[i])):
                try:
                    del locked_positions[(j, i)]
                except:
                    continue
    
    if increment > 0:
        for key in sorted(list(locked_positions, key = lambda x: x[1]))[::-1]:
            x, y = key
            if y < ind:
                new_key = (x, y + increment)
                locked_positions[new_key] = locked_positions.pop(key)

    return increment

def draw_next(surface, piece):

    ''' Shows user the next shape '''

    f = pygame.font.SysFont('arial', 50)
    label = f.render('Next shape', 1, (255, 255, 255))
    xx = top_x + play_width + 30
    yy = top_y + play_height/2 - 100

    form = piece.shape[piece.rotation % len(piece.shape)]  # gives you needed sublist

    for i, line in enumerate(form):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, piece.colour, (xx + j * block_size, yy + i * block_size, block_size, block_size), 0)

    surface.blit(label, (xx, yy - 30))


def draw_window(surface, grid, score=0):

    ''' Displays the window, grid, surrounding red rectangle, game title and score label '''

    surface.fill((0, 0, 0))
    
    f = pygame.font.SysFont('arial', 60)
    label = f.render('Tetris', 1, (255, 255, 255))
    surface.blit(label, (top_x + play_width/2 - label.get_width()/2, top_y - 50))

    f2 = pygame.font.SysFont('arial', 40)
    label_score = f.render('Your score is: %d' %(score), 1, (255, 255, 255))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_x + j * block_size, top_y + i * block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0), (top_x, top_y, play_width, play_height), 1)

    draw_grid(surface, grid)


def convert_shape_format(piece):
    
    ''' Converts shape list into positions '''

    positions = []
    form = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(form):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))

    for i, position in enumerate(positions):
        positions[i] = (position[0] - 2, position[1] - 4)

    return positions

def valid_space(piece, grid):
    
    ''' Checks if piece is going to a valid space in grid '''

    valid = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    valid = [j for sublist in valid for j in sublist]
    formatted = convert_shape_format(piece)

    for position in formatted:
        if position not in valid:
            if position[1] >= 0:
                return False

    return True

def check_lost(positions):
    
    ''' Checks if the piece is above the screen '''
    
    for position in positions:
        x, y = position
        if y <= 0:
            return True
    
    return False

def main():

    ''' Main game structure '''
    
    locked_positions = {}
    create_grid(locked_positions)
    current_piece = get_shape(shapes)
    next_piece = get_shape(shapes)
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    change_piece = False
    running = True
    while running:
        
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation += 1

        shape_position = convert_shape_format(current_piece)
        for i in range(len(shape_position)):
            x, y = shape_position[i]
            if y >= 0:
                grid[y][x] = current_piece.colour

        if change_piece:
            for position in shape_position:
                p = (position[0], position[1])
                locked_positions[p] = current_piece.colour
            current_piece = next_piece
            next_piece = get_shape(shapes)
            increment = clear_rows(grid, locked_positions)
            score += 10 * increment
            change_piece = False
        
        draw_window(screen, grid, score)
        draw_next(screen, next_piece)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text(screen, 'You Lost!', (255, 255, 255), 40)
            pygame.display.update()
            pygame.time.delay(2000)
            running = False


def main_menu():
    
    ''' Start of program '''

    running = True
    while running:
        screen.fill(background_colour)
        draw_text(screen, 'Press any key to play', (255, 255, 255), 60)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()
            if event.type == pygame.KEYDOWN:
                main()



screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tetris')

main_menu()

