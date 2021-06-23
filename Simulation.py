import pygame
from Board import Board

class Simulation:
    def __init__(self, width=640, height=480):
        pygame.init()

        self.width = width
        self.height = height

        self.surface = pygame.display.set_mode((width,height))

        self.board = Board(width, height, 100)

        self.running = True

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.board.update()
    
    def draw(self):
        self.surface.fill((0, 0, 0))
        self.board.draw(self.surface)
        pygame.display.flip()

    def play(self):
        while self.running:
            self.handleEvents()
            self.update()
            self.draw()
