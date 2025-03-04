import pygame
import random

# Initialize pygame fonts
pygame.font.init()

# -----------------------------
# Global Variables and Settings
# -----------------------------
s_width = 800
s_height = 700
play_width = 300   # 10 columns * 30 px per block
play_height = 600  # 20 rows * 30 px per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height - 50

# -----------------------------
# Define Tetris Shapes
# Each shape is a list of rotations; each rotation is represented as a 5x5 grid
# using a string, where '0' represents a filled block.
# -----------------------------
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
# Assign each shape a color
shape_colors = [
    (0, 255, 0),     # S
    (255, 0, 0),     # Z
    (0, 255, 255),   # I
    (255, 255, 0),   # O
    (255, 165, 0),   # J
    (0, 0, 255),     # L
    (128, 0, 128)    # T
]

# -----------------------------
# Class Definitions
# -----------------------------
class Piece:
    def __init__(self, x, y, shape):
        self.x = x  # Column position on grid
        self.y = y  # Row position on grid
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

# -----------------------------
# Helper Functions
# -----------------------------
def create_grid(locked_positions={}):
    """Create a 20x10 grid filled with black (empty) blocks. Locked positions
    are colored and kept in the grid."""
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                grid[i][j] = locked_positions[(j, i)]
    return grid

def convert_shape_format(piece):
    """Convert the piece's current rotation into grid positions."""
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]
    
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                # The offsets (-2, -4) adjust the shape to the grid
                positions.append((piece.x + j - 2, piece.y + i - 4))
    return positions

def valid_space(piece, grid):
    """Check if the piece's current position is valid (inside the grid and not
    colliding with locked positions)."""
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_positions = [pos for sub in accepted_positions for pos in sub]
    
    formatted = convert_shape_format(piece)
    
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    """Return True if any locked position is above the top of the screen."""
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    """Return a new random piece."""
    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(text, size, color, surface):
    """Draw centered text on the given surface."""
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    
    surface.blit(
        label,
        (
            top_left_x + play_width / 2 - label.get_width() / 2,
            top_left_y + play_height / 2 - label.get_height() / 2
        )
    )

def draw_grid(surface, grid):
    """Draw the grid lines for the play area."""
    sx = top_left_x
    sy = top_left_y
    
    for i in range(len(grid)):
        # Horizontal lines
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size), (sx + play_width, sy + i * block_size))
        for j in range(len(grid[i])):
            # Vertical lines
            pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy), (sx + j * block_size, sy + play_height))

def clear_rows(grid, locked):
    """Check and clear full rows in the grid. Move all rows above down."""
    inc = 0
    # Iterate backwards over the grid rows
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            # Remove every block in this row from locked_positions
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except KeyError:
                    continue
            # Shift rows above down by one
            for key in sorted(list(locked), key=lambda x: x[1], reverse=True):
                x, y = key
                if y < i:
                    newKey = (x, y + 1)
                    locked[newKey] = locked.pop(key)
    return inc

def draw_window(surface, grid, score=0):
    """Draw the current game window: title, score, grid, and border."""
    surface.fill((0, 0, 0))
    
    # Tetris Title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255, 255, 255))
    
    surface.blit(
        label,
        (top_left_x + play_width / 2 - label.get_width() / 2, 30)
    )
    
    # Current Score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))
    
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    surface.blit(label, (sx + 20, sy + 160))
    
    # Draw each block in the grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(
                surface,
                grid[i][j],
                (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size),
                0
            )
    
    draw_grid(surface, grid)
    # Draw a red border around the play area
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 4)

# -----------------------------
# Main Game Loop
# -----------------------------
def main(win):
    locked_positions = {}  # (x,y):(r, g, b)
    grid = create_grid(locked_positions)
    
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27  # Adjust for difficulty
    
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        # Make the current piece fall at regular intervals
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        # Process events (key presses, window close, etc.)
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
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    # Rotate the piece
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)

        # Draw the current piece on the grid
        shape_pos = convert_shape_format(current_piece)
        for pos in shape_pos:
            x, y = pos
            if y > -1:
                grid[y][x] = current_piece.color

        # If the piece has reached its final position, lock it and get a new piece
        if change_piece:
            for pos in shape_pos:
                locked_positions[pos] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            # Clear any full rows and update the score
            score += clear_rows(grid, locked_positions) * 10

        draw_window(win, grid, score)
        pygame.display.update()

        # Check if any blocks have reached the top (loss condition)
        if check_lost(locked_positions):
            draw_text_middle("YOU LOST", 80, (255, 255, 255), win)
            pygame.display.update()
            pygame.time.delay(2000)
            run = False

# -----------------------------
# Main Menu Loop
# -----------------------------
def main_menu(win):
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle("Press Any Key To Play", 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)
    pygame.quit()

# -----------------------------
# Start the Game
# -----------------------------
if __name__ == '__main__':
    win = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption('Tetris')
    main_menu(win)
