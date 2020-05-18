from resources import reference
from resources.reference import *

class Ground:
    """
    This class represents the Ground in Flappy Bird. It uses two ground sprites
    and cycles them to give the illusion of moing ground. One sprite moves
    behind the other and when the first have dissapeared from the screen the
    sprite is recycled to the front.

    Some useful methods are:

    move() which should be called every game tick to figure out where the ground
    object has moved and where the pair ground object has to be drawn from.
    """

    VEL =5
    WIDTH = GROUND_IMAGE.get_width()
    IMG = GROUND_IMAGE

    def __init__(self, y):
        """
        Initializes the Ground object. pass the y coordinate of where the ground
        should spawn. x coordinates are not required because the ground object
        spans the entire horizontal distance.

        Arguments: y  -- y coordinate of the ground
        """
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        """
        This method should be called every tick to move the pair of ground
        objects and give the effect of a moving ground.
        """
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        # Adjust draw coordinates after moving pair of ground
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, window):
        """
        Draw the pair of ground spires

        Arguments: window -- The window where this object must be drawn
        """
        window.blit(self.IMG, (self.x1,self.y))
        window.blit(self.IMG, (self.x2,self.y))


