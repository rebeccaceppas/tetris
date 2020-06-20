import random, pygame

screen_width = 400
screen_height = 400
background_colour = (0, 0, 0)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tetris')
screen.fill(background_colour)

shapes = []
shape_colours = []

class Piece:

    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.colour = shape_colours[shapes.index(shape)]
        self.rotation = 0
    

def create_grid():
    pass

def get_shape(shapes):
    return Piece(5, 0, random.choice(shapes))

def valid_space():
    pass

def check_lost():
    pass

def draw_text():
    pass

def draw_grid():
    pass

def clear_rows():
    pass

def draw_next():
    pass

def draw_window(surface, grid):
    pass

def convert_shape():
    pass

def main():
    pass

def main_menu():
    pass


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

