import pygame
import os

# This file contains all the constants used in this project including the
# images.

def image_reader(directory, filename):
    """
    This function grabs the images from the specified filepath using pygame's
    image.load functionality and then returns them. It also scales the images to
    2x and uses convert() to boost performance.

    Arguments: directory   -- Path to the directory in which the image is
        located filename  -- The filename for the image.

    Returns: -- The image at the given location
    """
    return pygame.transform.scale2x(pygame.image.load(os.path.join(directory,filename))).convert()

WIN_WIDTH = 500
WIN_HEIGHT = 800
GEN_NO = 0  # Keeping gen number as a common constant

# Initializting window for performance boost using convert(). The same variable
# can be used anywhere since the winow doesn't need to change
WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 50)

resource_path = os.path.join(os.path.dirname(__file__), "images")


BIRD_IMAGES = [image_reader(resource_path, "bird1.png"),
                image_reader(resource_path, "bird2.png"),
                image_reader(resource_path, "bird3.png")]

PIPE_IMAGE = image_reader(resource_path, "pipe.png")
GROUND_IMAGE = image_reader(resource_path, "base.png")
BKG_IMAGE = image_reader(resource_path, "bg.png")

