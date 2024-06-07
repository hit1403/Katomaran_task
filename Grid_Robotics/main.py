import pygame
import random
import heapq
import sys


pygame.init()

# display setup
width, height = 500, 500
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Robot Navigation Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


font = pygame.font.SysFont(None, 24)


ROWS, COLS = 10, 10
CELL_SIZE = width // COLS

# Create grid and obstacles
def create_grid():
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    obstacles = set()
    while len(obstacles) < 30:
        x, y = random.randint(0, ROWS - 1), random.randint(0, COLS - 1)
        if (x, y) not in obstacles:
            obstacles.add((x, y))
            grid[x][y] = 1  # 1 represents an obstacle
    print("errvrv",obstacles)
    return grid, obstacles

def draw_grid(window, grid, path=None, start=None, end=None):
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[row][col] == 1:
                pygame.draw.rect(window, BLACK, rect)
            else:
                pygame.draw.rect(window, WHITE, rect)
            pygame.draw.rect(window, BLACK, rect,1)
            
            # Drawing coordinates
            text = font.render(f'({row},{col})', True, BLACK)
            window.blit(text, (col * CELL_SIZE + 5, row * CELL_SIZE + 5))
    
    if path:
        for point in path:
            rect = pygame.Rect(point[1] * CELL_SIZE, point[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(window, BLUE, rect)
            # Drawing coordinates on the path
            text = font.render(f'({point[0]},{point[1]})', True, WHITE)
            window.blit(text, (point[1] * CELL_SIZE + 5, point[0] * CELL_SIZE + 5))
    
    if start:
        start_rect = pygame.Rect(start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(window, GREEN, start_rect)
        # Drawing coordinates on the start point
        text = font.render(f'({start[0]},{start[1]})', True, WHITE)
        window.blit(text, (start[1] * CELL_SIZE + 5, start[0] * CELL_SIZE + 5))
    
    if end:
        end_rect = pygame.Rect(end[1] * CELL_SIZE, end[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(window, RED, end_rect)
        # Drawing coordinates on the end point
        text = font.render(f'({end[0]},{end[1]})', True, WHITE)
        window.blit(text, (end[1] * CELL_SIZE + 5, end[0] * CELL_SIZE + 5))

grid, obstacles = create_grid()

def get_user_input(grid):
    while True:
        start = input("Enter start point (x y): ").split()
        end = input("Enter end point (x y): ").split()
        start = (int(start[0]), int(start[1]))
        end = (int(end[0]), int(end[1]))
        if start in obstacles or end in obstacles or not (0 <= start[0] < ROWS and 0 <= start[1] < COLS) or not (0 <= end[0] < ROWS and 0 <= end[1] < COLS):
            print("Invalid points, please enter again.")
        else:
            return start, end

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(grid, start, end):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {(row, col): float('inf') for row in range(ROWS) for col in range(COLS)}
    g_score[start] = 0
    f_score = {(row, col): float('inf') for row in range(ROWS) for col in range(COLS)}
    f_score[start] = heuristic(start, end)
    
    while open_set:
        current = heapq.heappop(open_set)[1]
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < COLS and grid[neighbor[0]][neighbor[1]] == 0:
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    print(open_set)
    return []

def main():
    clock = pygame.time.Clock()
    
    # Initial visualization of the grid with obstacles
    window.fill(WHITE)
    draw_grid(window, grid)
    pygame.display.flip()
    clock.tick(2)
    
    # Get user input for start and end points
    while True:
        start, end = get_user_input(grid)
        
        # Perform A* pathfinding
        path = a_star(grid, start, end)
        if path:
            print("PATH:", path)
        else:
            print("NO PATH FOUND")
        
        # Main loop for visualization with path
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
            
            window.fill(WHITE)
            draw_grid(window, grid, path, start, end)
            pygame.display.flip()
            clock.tick(60)
        
        cont = input("Do you want to continue (1/0): ")
        if cont != "1":
            break

    pygame.quit()

if __name__ == "__main__":
    main()
