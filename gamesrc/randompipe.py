import pygame
import random
from resources import reference
from gamesrc import pipe
from resources.reference import *
from gamesrc.pipe import Pipe

class RandomPipe(Pipe):
    """
    This class represents a complete random Pipe in Flappy Bird. Its gap sizes
    range from that of the hard pipe upto a little more difficult than the
    normal pipe.
    """

    def __init__(self, x):
        """
        Initialize the pipe. y coordinates are chosen at random so only the
        inital x spawnpoint needs to be provided

        Arguments:
            x  -- The x coordinate at which the pipe must be spawned
        """
        super().__init__(x)
        self.GAP = random.randrange(155, 190)
        self.set_height()

