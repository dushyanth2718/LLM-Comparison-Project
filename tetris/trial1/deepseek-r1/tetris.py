import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30

# Colors
COLORS = [
    (0, 0, 0),          # Black (empty)
    (0, 255, 255),      # Cyan (I)
    (255, 255, 0),      # Yellow (O)
    (128, 0, 128),      # Purple (T)
    (0, 0, 255),        # Blue (J)
    (255, 165, 0),      # Orange (L)
    (0, 255, 0),        # Green (S)
    (255, 0, 0)         # Red (Z)
]

# Shapes and their rotations
SHAPES = [
    # I
    [
        [(-1, 0), (0, 0), (1, 0), (2, 0)],
        [(0, -1), (0, 0), (0, 1), (0, 2)]
    ],
    # O
    [
        [(0, 0), (1, 0), (0, 1), (1, 1)]
    ],
    # T
    [
        [(-1, 0), (0, 0), (1, 0), (0, 1)],
        [(0, -1), (0, 0), (0, 1), (-1, 0)],
        [(-1, 0), (0, 0), (1, 0), (0, -1)],
        [(0, -1), (0, 0), (0, 1), (1, 0)]
    ],
    # L
    [
        [(-1, 0), (0, 0), (1, 0), (1, 1)],
        [(0, -1), (0, 0), (0, 1), (-1, 1)],
        [(-1, -1), (-1, 0), (0, 0), (1, 0)],
        [(0, -1), (1, -1), (0, 0), (0, 1)]
    ],
    # J
    [
        [(-1, 0), (0, 0), (1, 0), (-1, 1)],
        [(0, -1), (-1, 0), (0, 0), (0, 1)],
        [(1, -1), (-1, 0), (0, 0), (1, 0)],
        [(0, -1), (0, 0), (1, 1), (0, 1)]
    ],
    # S
    [
        [(-1, 0), (0, 0), (0, 1), (1, 1)],
        [(0, -1), (0, 0), (-1, 0), (-1, 1)],
        [(-1, -1), (0, -1), (0, 0), (1, 0)],
        [(1, -1), (1, 0), (0, 0), (0, 1)]
    ],
    # Z
    [
        [(-1, 1), (0, 1), (0, 0), (1, 0)],
        [(0, -1), (-1, 0), (0, 0), (-1, 1)],
        [(-1, 0), (0, 0), (0, -1), (1, -1)],
        [(0, -1), (0, 0), (1, 0), (1, 1)]
    ]
]

def is_valid_move(piece, rotation, x, y, grid):
    """Check if piece can be placed at (x, y) with current rotation"""
    for dx, dy in SHAPES[piece][rotation]:
        new_x = x + dx
        new_y = y + dy
        if new_x < 0 or new_x >= GRID_WIDTH:
            return False
        if new_y >= GRID_HEIGHT:
            return False
        if new_y >= 0 and grid[new_y][new_x] != 0:
            return False
    return True

def merge_piece(piece, rotation, x, y, grid):
    """Merge piece into grid"""
    color = piece + 1
    for dx, dy in SHAPES[piece][rotation]:
        new_x = x + dx
        new_y = y + dy
        if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
            grid[new_y][new_x] = color

def check_lines(grid):
    """Check and clear completed lines"""
    lines_cleared = 0
    y = GRID_HEIGHT - 1
    while y >= 0:
        if all(cell != 0 for cell in grid[y]):
            del grid[y]
            grid.insert(0, [0]*GRID_WIDTH)
            lines_cleared += 1
        else:
            y -= 1
    return lines_cleared

def draw_grid(screen, grid):
    """Draw game grid"""
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = COLORS[grid[y][x]]
            pygame.draw.rect(screen, color, (x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE-1, BLOCK_SIZE-1))

def draw_piece(screen, piece, rotation, x, y):
    """Draw current piece"""
    color = COLORS[piece + 1]
    for dx, dy in SHAPES[piece][rotation]:
        block_x = (x + dx) * BLOCK_SIZE
        block_y = (y + dy) * BLOCK_SIZE
        pygame.draw.rect(screen, color, (block_x, block_y, BLOCK_SIZE-1, BLOCK_SIZE-1))

def draw_next_piece(screen, piece, x, y):
    """Draw next piece preview"""
    color = COLORS[piece + 1]
    rotation = 0
    for dx, dy in SHAPES[piece][rotation]:
        block_x = x + dx * BLOCK_SIZE
        block_y = y + dy * BLOCK_SIZE
        pygame.draw.rect(screen, color, (block_x, block_y, BLOCK_SIZE-1, BLOCK_SIZE-1))

def main():
    """Main game loop"""
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    current_piece = random.randint(0, len(SHAPES)-1)
    next_piece = random.randint(0, len(SHAPES)-1)
    current_rotation = 0
    current_x = GRID_WIDTH // 2 - 2
    current_y = 0
    score = 0
    fall_speed = 0.5
    fall_time = 0
    game_over = False

    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    continue
                if event.key == pygame.K_LEFT:
                    new_x = current_x - 1
                    if is_valid_move(current_piece, current_rotation, new_x, current_y, grid):
                        current_x = new_x
                elif event.key == pygame.K_RIGHT:
                    new_x = current_x + 1
                    if is_valid_move(current_piece, current_rotation, new_x, current_y, grid):
                        current_x = new_x
                elif event.key == pygame.K_DOWN:
                    new_y = current_y + 1
                    if is_valid_move(current_piece, current_rotation, current_x, new_y, grid):
                        current_y = new_y
                elif event.key == pygame.K_UP:
                    new_rotation = (current_rotation + 1) % len(SHAPES[current_piece])
                    if is_valid_move(current_piece, new_rotation, current_x, current_y, grid):
                        current_rotation = new_rotation
                elif event.key == pygame.K_SPACE:
                    while is_valid_move(current_piece, current_rotation, current_x, current_y + 1, grid):
                        current_y += 1
                    merge_piece(current_piece, current_rotation, current_x, current_y, grid)
                    score += check_lines(grid) * 100
                    current_piece = next_piece
                    next_piece = random.randint(0, len(SHAPES)-1)
                    current_rotation = 0
                    current_x = GRID_WIDTH // 2 - 2
                    current_y = 0
                    if not is_valid_move(current_piece, current_rotation, current_x, current_y, grid):
                        game_over = True

        # Automatic falling
        if not game_over:
            delta_time = clock.tick(60) / 1000
            fall_time += delta_time
            if fall_time >= fall_speed:
                fall_time = 0
                new_y = current_y + 1
                if is_valid_move(current_piece, current_rotation, current_x, new_y, grid):
                    current_y = new_y
                else:
                    merge_piece(current_piece, current_rotation, current_x, current_y, grid)
                    score += check_lines(grid) * 100
                    current_piece = next_piece
                    next_piece = random.randint(0, len(SHAPES)-1)
                    current_rotation = 0
                    current_x = GRID_WIDTH // 2 - 2
                    current_y = 0
                    if not is_valid_move(current_piece, current_rotation, current_x, current_y, grid):
                        game_over = True

        # Drawing
        draw_grid(screen, grid)
        if not game_over:
            draw_piece(screen, current_piece, current_rotation, current_x, current_y)
        
        # UI Elements
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (GRID_WIDTH * BLOCK_SIZE + 50, 250))
        next_text = font.render("Next Piece:", True, (255, 255, 255))
        screen.blit(next_text, (GRID_WIDTH * BLOCK_SIZE + 50, 50))
        draw_next_piece(screen, next_piece, GRID_WIDTH * BLOCK_SIZE + 50, 100)
        
        if game_over:
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
        
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()