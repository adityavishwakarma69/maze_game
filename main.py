import pygame
import sys
import random

# --- Configuration ---
TILE_SIZE = 30
# Must be odd numbers for the wall-carving logic to work perfectly
COLS, ROWS = 21, 15
SCREEN_WIDTH = COLS * TILE_SIZE
SCREEN_HEIGHT = ROWS * TILE_SIZE
FPS = 60

# Colors
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
PLAYER_COLOR, GOAL_COLOR, WALL_COLOR = (
    52, 152, 219), (46, 204, 113), (44, 62, 80)


def generate_maze(width, height):
    # Start with a grid of all walls (1)
    maze = [[1 for _ in range(width)] for _ in range(height)]

    def walk(x, y):
        maze[y][x] = 0  # Mark current cell as path

        # Randomize directions: North, South, East, West
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(dirs)

        for dx, dy in dirs:
            # Check 2 steps ahead to ensure we leave a wall between paths
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                maze[y + dy][x + dx] = 0  # Remove wall between
                walk(nx, ny)

    walk(1, 1)  # Start carving from (1, 1)
    maze[height-2][width-2] = "G"  # Place Goal at bottom right
    return maze


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(
            x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def move(self, dx, dy, MAZE):
        new_x = self.rect.x + dx * TILE_SIZE
        new_y = self.rect.y + dy * TILE_SIZE
        grid_x, grid_y = new_x // TILE_SIZE, new_y // TILE_SIZE

        if 0 <= grid_x < COLS and 0 <= grid_y < ROWS:
            if MAZE[grid_y][grid_x] != 1:
                self.rect.x, self.rect.y = new_x, new_y

    def draw(self, surface):
        pygame.draw.rect(surface, PLAYER_COLOR, self.rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze")
    clock = pygame.time.Clock()
    player = Player(1, 1)
    font = pygame.font.SysFont("Arial", 32)
    MAZE = generate_maze(COLS, ROWS)
    vx, vy = 0, 0
    dt = 0
    timer = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    vy = -1
                elif event.key == pygame.K_DOWN:
                    vy = 1
                elif event.key == pygame.K_LEFT:
                    vx = -1
                elif event.key == pygame.K_RIGHT:
                    vx = 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    vy = 0
                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    vx = 0

        timer += dt
        if timer >= 100:
            player.move(vx, vy, MAZE)
            timer = timer - 100
        # Win Condition
        gx, gy = player.rect.x // TILE_SIZE, player.rect.y // TILE_SIZE
        win_screen = False
        if MAZE[gy][gx] == "G":
            win_screen = True
        while win_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        MAZE = generate_maze(COLS, ROWS)
                        player = Player(1, 1)
                        win_screen = False
            screen.fill((44, 62, 80))
            text = font.render("YOU WIN", True, (200, 200, 200))
            t_rect = text.get_rect()
            screen.blit(text, (SCREEN_WIDTH//2 - t_rect.center[0],
                        SCREEN_HEIGHT//2 - t_rect.center[1]))
            pygame.display.flip()

        # Draw
        screen.fill(WHITE)
        for r in range(ROWS):
            for c in range(COLS):
                tile = MAZE[r][c]
                rect = (c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if tile == 1:
                    pygame.draw.rect(screen, WALL_COLOR, rect)
                elif tile == "G":
                    pygame.draw.rect(screen, GOAL_COLOR, rect)

        player.draw(screen)
        pygame.display.flip()
        dt = clock.tick(FPS)


if __name__ == "__main__":
    main()
