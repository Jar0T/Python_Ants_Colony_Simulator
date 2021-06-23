from numpy import sqrt
import pygame

class Anthill:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, surface):
        pygame.draw.circle(surface, (160, 82, 45), (self.x, self.y), self.radius)

    def checkCollisions(self, ants):
        for ant in ants:
            position = (ant.position[0] - self.x, ant.position[1] - self.y)
            distance = sqrt((position[0] * position[0]) + (position[1] * position[1]))
            if distance <= self.radius:
                ant.visitAnthill()

    def update(self, ants):
        self.checkCollisions(ants)
