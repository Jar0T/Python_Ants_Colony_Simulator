from Field import Field
from Ant import Ant
from Anthill import Anthill

import random

class Board:
    def __init__(self, x_size, y_size, number_of_ants = 100):
        self.x_size = x_size
        self.y_size = y_size
        self.fields = []
        for _ in range(x_size * y_size):
            self.fields.append(Field(0.8))
        self.ants = []
        ant_start_x = random.random() * x_size
        ant_start_y = random.random() * y_size
        for _ in range(number_of_ants):
            self.ants.append(Ant(ant_start_x, ant_start_y, random.random() * 2 - 0.5, random.random() * 2 - 0.5))
        self.anthill = Anthill(ant_start_x, ant_start_y, 10)

        for x in range(150, 170):
            for y in range(150, 170):
                self.fields[y * x_size + x].addFood(255)

    def draw(self, surface):
        for x in range(self.x_size):
            for y in range(self.y_size):
                self.fields[y * self.x_size + x].draw(surface, x, y)

        for ant in self.ants:
            ant.draw(surface)

        self.anthill.draw(surface)

    def update(self):
        for x in range(self.x_size):
            for y in range(self.y_size):
                self.fields[y * self.x_size + x].update()
        
        for ant in self.ants:
            ant.update(self.fields, self.x_size, self.y_size)
        
        self.anthill.update(self.ants)