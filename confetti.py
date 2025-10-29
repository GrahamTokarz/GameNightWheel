import pygame
import random
import math

# You already have this
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Confetti particle class
class Confetti:
    def __init__(self):
        self.x = 400  # Center of the screen (start position)
        self.y = 300
        self.size = random.randint(2, 5)
        self.color = random.choice([
            (255, 0, 0), (0, 255, 0), (0, 0, 255),
            (255, 255, 0), (255, 0, 255), (0, 255, 255)
        ])
        
        # Random velocity angle in radians
        self.angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)  # Speed at which the confetti moves
        self.vel_x = speed * math.cos(self.angle)
        self.vel_y = speed * math.sin(self.angle)

        self.rotation_speed = random.uniform(-5, 5)

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.angle += self.rotation_speed
        
        # Reset position if it goes out of screen bounds
        if self.x < 0 or self.x > 800 or self.y < 0 or self.y > 600:
            self.__init__()

    def draw(self, surface):
        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(surface, self.color, rect)

# Confetti list
confetti_particles = [Confetti() for _ in range(100)]
show_confetti = True  # <- Toggle this to show/hide confetti

# Game loop
running = True
while running:
    screen.fill((30, 30, 30))  # dark background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update and draw confetti
    if show_confetti:
        for particle in confetti_particles:
            particle.update()
            particle.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
