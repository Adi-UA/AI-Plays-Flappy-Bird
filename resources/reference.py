import pygame
import os

def image_reader(directory, filename):
    return pygame.transform.scale2x(pygame.image.load(os.path.join(directory,filename)))

WIN_WIDTH = 500
WIN_HEIGHT = 800
GEN_NO = 0

pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 50)
resource_path = os.path.join(os.path.dirname(__file__), "images")

BIRD_IMAGES = [image_reader(resource_path, "bird1.png"),
                image_reader(resource_path, "bird2.png"),
                image_reader(resource_path, "bird3.png")]

PIPE_IMAGE = image_reader(resource_path, "pipe.png")
GROUND_IMAGE = image_reader(resource_path, "base.png")
BKG_IMAGE = image_reader(resource_path, "bg.png")

