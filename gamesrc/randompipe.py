import pygame
import random
from resources import reference
from gamesrc import pipe
from resources.reference import *
from gamesrc.pipe import Pipe

class RandomPipe(Pipe):

    def __init__(self, x):
        super().__init__(x)
        self.GAP = random.randrange(155, 190)
        self.set_height()

