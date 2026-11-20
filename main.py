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
NUM_BALLS = 20
BALL_SIZE = 100
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
        ipos = positions[i]
        ivel = velocities[i]
        for j in range(i + 1 ,NUM_BALLS):

            jpos = positions[j]
            jvel = velocities[j]

            distance_sq = np.sum((ipos - jpos)**2)
            if not distance_sq < BALL_SIZE**2:
                continue

            distance = distance_sq ** 0.5

            collision_vector = (ipos - jpos) / distance

            overlap = BALL_SIZE - distance

            ipos = ipos + (overlap / 2) * collision_vector
            jpos = jpos - (overlap / 2) * collision_vector

            rel_vel = ivel - jvel

            closing_speed = rel_vel @ collision_vector

            if closing_speed > 0:
                continue

            ivel = (ivel - closing_speed * collision_vector) * BOUNCE
            jvel = (jvel + closing_speed * collision_vector) * BOUNCE

            positions[i] = ipos
            positions[j] = jpos

            velocities[i] = ivel
            velocities[j] = jvel


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