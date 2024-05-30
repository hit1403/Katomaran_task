import pygame
import sys

pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Autonomous Navigation Robot')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


clock = pygame.time.Clock()

# Coordinates of the rectangular pillar (x1, y1), (x2, y2), (x3, y3), (x4, y4)
pillar_corners = [(300, 200), (500, 200), (500, 400), (300, 400)]
#pillar_corners = [(300, 300), (200, 400), (300, 500), (400, 400)]

def calculate_center(corners):
    x_coords = [corner[0] for corner in corners]
    y_coords = [corner[1] for corner in corners]
    center_x = sum(x_coords) / len(corners)
    center_y = sum(y_coords) / len(corners)
    return int(center_x), int(center_y)

center_x, center_y = calculate_center(pillar_corners)

# Robot's starting position
robot_pos = [250, 250]

left = min(corner[0] for corner in pillar_corners)
right = max(corner[0] for corner in pillar_corners)
top = min(corner[1] for corner in pillar_corners)
bottom = max(corner[1] for corner in pillar_corners)
# Navigating to center avoiding the pillar
def navigate_to_center(robot_pos, center_x, center_y, pillar_corners):
    path = []
    # Navigating horizontally first, then vertically
    if robot_pos[0] < center_x:

            
        while robot_pos[0] < center_x:
            flag=0
            if (robot_pos[0]+1,robot_pos[1]) in pillar_corners and center_x>=robot_pos[0]:
                flag=1
                for p in pillar_corners:
                    if p==(robot_pos[0]+1,robot_pos[1]):
                        res = p
                if res[1]==top:
                    path.append((robot_pos[0], robot_pos[1]+1))
                    robot_pos[1]+=1
                    path.append((robot_pos[0]+1, robot_pos[1]))
                    robot_pos[0]+=1

                elif res[1]==bottom:
                    path.append((robot_pos[0], robot_pos[1]-1))
                    robot_pos[1]-=1
                    path.append((robot_pos[0]+1, robot_pos[1]))
                    robot_pos[0]+=1
                else:

                    path.append((robot_pos[0], robot_pos[1]+1))
                    robot_pos[1]+=1
                    path.append((robot_pos[0]+1, robot_pos[1]))
                    robot_pos[0]+=1
                    path.append((robot_pos[0]+1, robot_pos[1]))
                    robot_pos[0]+=1
                    path.append((robot_pos[0], robot_pos[1]-1))
                    robot_pos[1]-=1
            if flag==0:
                robot_pos[0] += 1
                path.append((robot_pos[0], robot_pos[1]))
    else:

            
        while robot_pos[0] > center_x:
            flag=0
            if (robot_pos[0]-1,robot_pos[1]) in pillar_corners and center_x<=robot_pos[0]:
                flag=1
                for p in pillar_corners:
                    if p==(robot_pos[0]-1,robot_pos[1]):
                        res = p
                if res[1]==top:
                    path.append((robot_pos[0], robot_pos[1]+1))
                    robot_pos[1]+=1
                    path.append((robot_pos[0]-1, robot_pos[1]))
                    robot_pos[0]-=1

                elif res[1]==bottom:
                    path.append((robot_pos[0], robot_pos[1]-1))
                    robot_pos[1]-=1
                    path.append((robot_pos[0]-1, robot_pos[1]))
                    robot_pos[0]-=1
                else:
                    path.append((robot_pos[0], robot_pos[1]+1))
                    robot_pos[1]+=1
                    path.append((robot_pos[0]-1, robot_pos[1]))
                    robot_pos[0]-=1
                    path.append((robot_pos[0]-1, robot_pos[1]))
                    robot_pos[0]-=1
                    path.append((robot_pos[0], robot_pos[1]-1))
                    robot_pos[1] -= 1

            if flag==0:
                robot_pos[0] -= 1
                path.append((robot_pos[0], robot_pos[1]))
    
    if robot_pos[1] < center_y:

   
        while robot_pos[1] < center_y:
            flag=0

            if(robot_pos[0],robot_pos[1]+1) in pillar_corners and center_y>=robot_pos[1]:
                flag=1
            
                path.append((robot_pos[0]+1, robot_pos[1]))
                robot_pos[0]+=1
                path.append((robot_pos[0], robot_pos[1]+1))
                robot_pos[1]+=1
                path.append((robot_pos[0], robot_pos[1]+1))
                robot_pos[1]+=1
                path.append((robot_pos[0]-1, robot_pos[1]))
                robot_pos[0]-=1
            if flag==0:
                robot_pos[1] += 1
                path.append((robot_pos[0], robot_pos[1]))
    else:

 
        while robot_pos[1] > center_y:
            flag=0

            if (robot_pos[0],robot_pos[1]-1) in pillar_corners and center_y<=robot_pos[1]:
                flag=1
                for p in pillar_corners:
                    if p==(robot_pos[0],robot_pos[1]-1):
                        res = p
                path.append((robot_pos[0]+1, robot_pos[1]))
                robot_pos[0]+=1
                path.append((robot_pos[0], robot_pos[1]-1))
                robot_pos[1]-=1
                path.append((robot_pos[0], robot_pos[1]-1))
                robot_pos[1]-=1
                path.append((robot_pos[0]-1, robot_pos[1]))
                robot_pos[0]-=1
                
            if flag==0:
                robot_pos[1] -= 1
                path.append((robot_pos[0], robot_pos[1]))
    
    return path

# pillar
def draw_pillar(screen, corners):
    pygame.draw.polygon(screen, RED, corners, 1)

# robot
def draw_robot(screen, pos):
    pygame.draw.circle(screen, BLUE, pos, 1)

# path getting
path = navigate_to_center(robot_pos, center_x, center_y, pillar_corners)
print(path)


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(WHITE)
    
    draw_pillar(screen, pillar_corners)
    draw_robot(screen, robot_pos)
    if path:
        next_pos = path.pop(0)
        robot_pos[0], robot_pos[1] = next_pos
    
    pygame.display.flip()
    clock.tick(10)

pygame.quit()
sys.exit()
