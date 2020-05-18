import pygame
from resources import reference
from gamesrc import pipe
from resources.reference import *
from gamesrc.pipe import *

class HardPipe(Pipe):

    def __init__(self, x):
        super().__init__(x)
        self.GAP = 155
        self.set_height()

