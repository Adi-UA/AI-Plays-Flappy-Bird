import pygame
from resources import reference
from resources.reference import BIRD_IMAGES


class Bird:
    """
    This class represents the bird in Flappy Bird.

    Some useful Methods are:

    move() which should be called every game tick to figure out how far the bird
    has fallen.

    jump() which tells the bird to 'jump' or fly up a little in that frame. This
    is the only aspect of the bird that needs to be controlled during gameplay.
    """

    IMGS = BIRD_IMAGES
    MAX_ROT = 25  # How much can it rotate
    ROT_VEL = 20  # host fast can it rotate
    ANIMATION_TIME = 5   # Costant used to switch sprites at the right time

    def __init__(self, x, y):
        """
        Initializes the Bird object. Give coordinates for the top left of the
        image as parameters

        Arguments: x  -- Top left x coordinate y  -- Top left y coordinate
        """
        self.x = x
        self.y = y
        self.height = self.y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.img_count = 0
        self.img = self.IMGS[0]
        self.img_idx = 1

    def jump(self):
        """
        This function controls bird behaviour when it is asked to jump. It sets
        the velocity to a negative value so the move function can orient the
        bird correctly depending on the resultant displacement.
        """
        self.vel = -4.55
        self.tick_count = 0  # Reset ticks so the bird doesn't fall too fast later
        self.height = self.y

    def move(self):
        """
        This function handles how the bird moves and looks at each game tick.z
        """
        self.tick_count += 1

        # terminal velocity is 16
        displacement = self.vel * self.tick_count + 0.5 * self.tick_count**2
        if displacement >= 16:
            displacement = displacement / abs(displacement) * 16
        elif displacement < 0:
            displacement -= 2

        self.y = self.y + displacement

        # Sprite Orientation. Make sure the bird isn't rotating too far.
        if(displacement < 0 or self.y < self.height + 50):
            if self.tilt < self.MAX_ROT:
                self.tilt = self.MAX_ROT
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, window):
        """
        This method controls how the bird is drawn in the given window in a
        particular frame.

        Arguments:
            window  -- The window in which the bird must be drawn
        """
        self.img_count += 1

        # Cycle between the 3 image PNGs every 5 ticks
        if (self.img_count + 1) % self.ANIMATION_TIME == 0:
            self.img = self.IMGS[self.img_idx % 3]
            self.img_idx += 1

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        rot_image = pygame.transform.rotate(
            self.img, self.tilt)  # Rotated image

        # Use current image center as reference for choosing centre in rotated
        # image. The resulting rectangular surface has the correct correspondig
        # top left.
        new_rect = rot_image.get_rect(
            center=self.img.get_rect(
                topleft=(
                    self.x,
                    self.y)).center)

        window.blit(rot_image, new_rect.topleft)

    def get_mask(self):
        """
        Get mask from the image for use in collision detection.
        """
        return pygame.mask.from_surface(self.img)
