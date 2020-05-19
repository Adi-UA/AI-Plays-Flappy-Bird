import pygame
from resources import reference
from gamesrc import pipe
from resources.reference import *
from gamesrc.pipe import *


class HardPipe(Pipe):
    """
    This class represents a complete more difficult Pipe in Flappy Bird.
    """

    def __init__(self, x):
        """
        Initialize the pipe. y coordinates are chosen at random so only the
        inital x spawnpoint needs to be provided

        Arguments:
            x  -- The x coordinate at which the pipe must be spawned
        """
        super().__init__(x)
        self.GAP = 155  # Uses a much smaller gap
        self.set_height()  # Update sprite calculations accordingly
