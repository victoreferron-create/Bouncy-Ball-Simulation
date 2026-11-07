import pygame
import numpy as np
import sys

# define global variables

# usual pygame boilerplate
WIDTH, HEIGHT = 1200, 1000
BG_COLOR = (30, 30, 35)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball Simulation")
clock = pygame.time.Clock()

# simulation variables
NUM_BALLS = 1000
BALL_SIZE = 20
BALL_STARTING_SPEED_RANGE = 20
DRAG = 1
BOUNCE = 0.99
GROUND_FRICTION = 0.99
GRAVITY = 2

positions = np.random.rand(NUM_BALLS, 2) * np.array([WIDTH, HEIGHT])
velocities = (np.random.rand(NUM_BALLS, 2) - 0.5) * 2 * BALL_STARTING_SPEED_RANGE
colors = np.random.rand(NUM_BALLS, 3) * 255

def main():
    while True:
        gameloop()

def gameloop():
    global positions, velocities

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BG_COLOR)
    # handle ball-to-ball collisions
    for i in range(NUM_BALLS):
        x1, y1 = positions[i]
        sx1, sy1 = velocities[i]
        for j in range(NUM_BALLS):
            x2, y2 = positions[j]
            sx2, sy2 = velocities[j]

            # check if the balls are ovelapping
            distance_sq = (x1 - x2)**2 + (y1 - y2)**2
            if (distance_sq > BALL_SIZE**2):
                continue
                
            distance = distance_sq ** 0.5
            

    # handle walls
    for i in range(NUM_BALLS):
        x, y = positions[i]
        sx, sy = velocities[i]
        # handle walls x (vertical)
        if x < BALL_SIZE / 2:
            x = BALL_SIZE / 2
            sx = -sx * BOUNCE
        elif x > WIDTH - BALL_SIZE / 2:
            x = WIDTH - BALL_SIZE / 2
            sx = -sx * BOUNCE
        # handle walls y (horizontal)
        if y < BALL_SIZE / 2:
            y = BALL_SIZE / 2
            sy = -sy * BOUNCE
            sx *= GROUND_FRICTION
        elif y > HEIGHT - BALL_SIZE / 2:
            y = HEIGHT - BALL_SIZE / 2
            sy = -sy * BOUNCE
            sx *= GROUND_FRICTION
    
        positions[i] = x, y
        velocities[i] = sx, sy

    

    velocities += 0, GRAVITY
    velocities *= DRAG
    positions += velocities

    # render balls
    for i in range(NUM_BALLS):
        x, y = positions[i]
        color = colors[i]
        pygame.draw.circle(screen, color, (int(x), int(y)), BALL_SIZE / 2)

    pygame.display.flip()

    clock.tick(60)


if __name__ == '__main__':
    main()