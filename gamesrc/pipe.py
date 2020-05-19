import pygame
import random
from resources import reference
from resources.reference import *


class Pipe:
    """
    This class represents a complete Pipe in Flappy Bird including the top and
    bottom half separated by a gap.


    Some useful methods are:

    move() which should be called every game tick to figure out where the pipe
    should be placed on screen during a frame.
    """
    VEL = 5

    def __init__(self, x):
        """
        Initialize the pipe. y coordinates are chosen at random so only the
        inital x spawnpoint needs to be provided

        Arguments:
            x  -- The x coordinate at which the pipe must be spawned
        """
        self.x = x
        self.height = 0
        self.GAP = 200

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.PIPE_BOTTOM = PIPE_IMAGE

        self.passed = False
        self.set_height()

    def set_height(self):
        """
        This method calculates the height at whch the top and bottom halves of
        the pipe are to be drawn.
        """
        # Where we plan to start drawing the gap
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        """
        This method is called every tick to move the pipe further left as te
        game progresses.
        """
        self.x -= self.VEL

    def draw(self, window):
        """
        Draw the pipe in the given window.

        Arguments: window -- The window where this object must be drawn
        """
        window.blit(self.PIPE_TOP, (self.x, self.top))
        window.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        """
        This function handles collision of the pipe object with a bird. Masks
        are used to dtermine overlap and collision is decided as a result.

        Arguments:
            bird  -- The Bird object

        Returns:
            boolean -- true if a collision ocurred and false otherwise.
        """

        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        # Narrow the range
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        top_overlaps = bird_mask.overlap(top_mask, top_offset)
        bot_overlaps = bird_mask.overlap(bottom_mask, bottom_offset)

        if top_overlaps or bot_overlaps:
            return True
        else:
            return False
