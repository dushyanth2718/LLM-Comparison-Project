import pygame
import random

# Initialize fonts
pygame.font.init()

# GLOBAL VARIABLES
s_width = 800               # screen width
s_height = 700              # screen height
play_width = 300            # play area width (10 blocks * 30 px)
play_height = 600           # play area height (20 blocks * 30 px)
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height - 50

# SHAPE FORMATS (5x5 grid strings)
S = [['.....',
      '.....',
      '..00.',
      '.00..',
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
# Colors for each shape in RGB format
shape_colors = [
    (0, 255, 0),      # S: green
    (255, 0, 0),      # Z: red
    (0, 255, 255),    # I: cyan
    (255, 255, 0),    # O: yellow
    (255, 165, 0),    # J: orange
    (0, 0, 255),      # L: blue
    (128, 0, 128)     # T: purple
]

class Piece:
    def __init__(self, x, y, shape):
        self.x = x  # grid position (column)
        self.y = y  # grid position (row)
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

def create_grid(locked_positions={}):
    """Create a 20x10 grid with locked positions filled in."""
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                grid[i][j] = locked_positions[(j, i)]
    return grid

def convert_shape_format(piece):
    """
    Convert the 5x5 string representation of the piece into grid positions.
    The offset (-2, -4) is used so that the shape appears centered.
    """
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j - 2, piece.y + i - 4))
    return positions

def valid_space(piece, grid):
    """Return True if the piece is in a valid (empty) space on the grid."""
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_positions = [pos for sub in accepted_positions for pos in sub]

    formatted = convert_shape_format(piece)

    for pos in formatted:
        x, y = pos
        if pos not in accepted_positions:
            if y > -1:
                return False
    return True

def check_lost(locked_positions):
    """Check if any of the locked positions are above the top of the play area."""
    for pos in locked_positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    """Return a random new piece."""
    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(surface, text, size, color):
    """Draw text in the center of the play area."""
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width / 2 - label.get_width() / 2,
                         top_left_y + play_height / 2 - label.get_height() / 2))

def draw_grid(surface, grid):
    """Draw the grid lines on the play area."""
    sx = top_left_x
    sy = top_left_y

    # Horizontal lines
    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size),
                         (sx + play_width, sy + i * block_size))
    # Vertical lines
    for j in range(len(grid[0])):
        pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy),
                         (sx + j * block_size, sy + play_height))

def clear_rows(grid, locked):
    """Clear full rows and move the above rows down.
    
    Returns the number of cleared rows (used for score).
    """
    cleared = 0
    # Start checking from the bottom of the grid
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            cleared += 1
            # Remove all locked positions in this row
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
            # Move every locked position above this row one row down
            for key in sorted(list(locked), key=lambda x: x[1], reverse=True):
                x, y = key
                if y < i:
                    newKey = (x, y + 1)
                    locked[newKey] = locked.pop(key)
    return cleared

def draw_next_shape(piece, surface):
    """Display the next shape preview."""
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render("Next Shape", 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100

    format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, piece.color,
                                 (sx + j * block_size, sy + i * block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))

def draw_window(surface, grid, score=0):
    """Draw the main game window (background, grid, score, etc.)."""
    surface.fill((0, 0, 0))

    # Draw title
    font = pygame.font.SysFont("comicsans", 60)
    label = font.render("Tetris", 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - label.get_width() / 2, 30))

    # Draw current score
    font = pygame.font.SysFont("comicsans", 30)
    score_label = font.render("Score: " + str(score), 1, (255, 255, 255))
    sx = top_left_x - 200
    sy = top_left_y + play_height / 2 - 100
    surface.blit(score_label, (sx + 20, sy + 160))

    # Draw each block in the grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

    draw_grid(surface, grid)
    # Draw a red border around the play area
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

def main(win):
    locked_positions = {}  # (x,y):(R,G,B)
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27  # seconds per fall
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        # Increase difficulty over time
        if level_time / 1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        # Handle piece falling
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        # Process events (keyboard, window closing, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    # Rotate the piece
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)

        shape_pos = convert_shape_format(current_piece)

        # Add current piece to the grid for drawing
        for pos in shape_pos:
            x, y = pos
            if y > -1:
                grid[y][x] = current_piece.color

        # If the piece hit the ground, lock it and get a new one
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(win, grid, score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        # Check if the player lost
        if check_lost(locked_positions):
            draw_text_middle(win, "YOU LOST", 80, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False

def main_menu(win):
    """Display the start screen until the user presses a key."""
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle(win, "Press any key to play", 60, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                main(win)
    pygame.quit()

if __name__ == '__main__':
    win = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption("Tetris")
    main_menu(win)
