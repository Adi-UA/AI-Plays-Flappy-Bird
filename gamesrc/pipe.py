import pygame
import random
from resources import reference
from resources.reference import *

class Pipe:
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.GAP = 200

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.PIPE_BOTTOM = PIPE_IMAGE

        self.passed =  False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom =  self.height + self.GAP


    def move(self):
        self.x -= self.VEL

    def draw(self, window):
        window.blit(self.PIPE_TOP, (self.x,self.top))
        window.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        top_overlaps = bird_mask.overlap(top_mask, top_offset)
        bot_overlaps = bird_mask.overlap(bottom_mask, bottom_offset)

        if top_overlaps or bot_overlaps:
            return True
        else:
            return False

