import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
GRID_OFFSET_X = (SCREEN_WIDTH - BLOCK_SIZE * GRID_WIDTH) // 2
GRID_OFFSET_Y = SCREEN_HEIGHT - BLOCK_SIZE * GRID_HEIGHT - 50

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),    # Cyan (I)
    (255, 165, 0),    # Orange (L)
    (0, 0, 255),      # Blue (J)
    (255, 255, 0),    # Yellow (O)
    (0, 255, 0),      # Green (S)
    (255, 0, 0),      # Red (Z)
    (128, 0, 128)     # Purple (T)
]

# Tetromino shapes
SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1],
          [1, 1]],
    'T': [[0, 1, 0],
          [1, 1, 1]],
    'L': [[1, 0],
          [1, 0],
          [1, 1]],
    'J': [[0, 1],
          [0, 1],
          [1, 1]],
    'S': [[0, 1, 1],
          [1, 1, 0]],
    'Z': [[1, 1, 0],
          [0, 1, 1]]
}

class Tetromino:
    def __init__(self, shape):
        self.shape = shape
        self.color = COLORS[random.randint(0, len(COLORS)-1)]
        self.rotation = 0
        self.x = GRID_WIDTH // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def get_blocks(self):
        blocks = []
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    blocks.append((self.x + x, self.y + y))
        return blocks

class Tetris:
    def __init__(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_piece = None
        self.score = 0
        self.game_over = False
        self.spawn_piece()

    def spawn_piece(self):
        shape = random.choice(list(SHAPES.values()))
        self.current_piece = Tetromino(shape)
        if self.check_collision(self.current_piece.get_blocks()):
            self.game_over = True

    def check_collision(self, blocks):
        for x, y in blocks:
            if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT:
                return True
            if y >= 0 and self.grid[y][x]:
                return True
        return False

    def move(self, dx, dy):
        self.current_piece.x += dx
        self.current_piece.y += dy
        if self.check_collision(self.current_piece.get_blocks()):
            self.current_piece.x -= dx
            self.current_piece.y -= dy
            return False
        return True

    def rotate(self):
        original_shape = self.current_piece.shape
        self.current_piece.rotate()
        if self.check_collision(self.current_piece.get_blocks()):
            self.current_piece.shape = original_shape

    def lock_piece(self):
        for x, y in self.current_piece.get_blocks():
            if y >= 0:
                self.grid[y][x] = self.current_piece.color
        self.clear_lines()
        self.spawn_piece()

    def clear_lines(self):
        lines_cleared = 0
        new_grid = []
        for row in self.grid:
            if 0 not in row:
                lines_cleared += 1
            else:
                new_grid.append(row)
        self.grid = [[0]*GRID_WIDTH for _ in range(lines_cleared)] + new_grid
        self.score += lines_cleared * 100

    def update(self):
        if not self.move(0, 1):
            self.lock_piece()

def draw_grid(screen):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(GRID_OFFSET_X + x * BLOCK_SIZE, 
                             GRID_OFFSET_Y + y * BLOCK_SIZE,
                             BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)

def draw_piece(screen, piece):
    for x, y in piece.get_blocks():
        if y >= 0:
            rect = pygame.Rect(GRID_OFFSET_X + x * BLOCK_SIZE,
                             GRID_OFFSET_Y + y * BLOCK_SIZE,
                             BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, piece.color, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

def draw_game(screen, game):
    screen.fill(BLACK)
    
    # Draw grid background
    grid_rect = pygame.Rect(GRID_OFFSET_X, GRID_OFFSET_Y,
                          BLOCK_SIZE * GRID_WIDTH, BLOCK_SIZE * GRID_HEIGHT)
    pygame.draw.rect(screen, WHITE, grid_rect)
    
    # Draw locked pieces
    for y, row in enumerate(game.grid):
        for x, color in enumerate(row):
            if color:
                rect = pygame.Rect(GRID_OFFSET_X + x * BLOCK_SIZE,
                                 GRID_OFFSET_Y + y * BLOCK_SIZE,
                                 BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, GRAY, rect, 1)
    
    # Draw current piece
    if game.current_piece:
        draw_piece(screen, game.current_piece)
    
    # Draw grid lines
    draw_grid(screen)
    
    # Draw score
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {game.score}", True, WHITE)
    screen.blit(text, (20, 20))
    
    if game.game_over:
        font = pygame.font.Font(None, 72)
        text = font.render("GAME OVER", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2))

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    game = Tetris()
    
    fall_time = 0
    fall_speed = 500  # Milliseconds
    
    while True:
        screen.fill(BLACK)
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if game.game_over:
                    game = Tetris()
                else:
                    if event.key == pygame.K_LEFT:
                        game.move(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        game.move(1, 0)
                    elif event.key == pygame.K_DOWN:
                        game.move(0, 1)
                    elif event.key == pygame.K_UP:
                        game.rotate()
        
        # Automatic falling
        if not game.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                fall_speed = 50
            else:
                fall_speed = 500
            
            if current_time - fall_time > fall_speed:
                game.update()
                fall_time = current_time
        
        draw_game(screen, game)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()