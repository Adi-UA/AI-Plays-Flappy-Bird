import pygame
from resources import reference
from resources.reference import BIRD_IMAGES


class Bird:
    IMGS = BIRD_IMAGES
    MAX_ROT = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.height = self.y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -4.55
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        displacement  = self.vel*self.tick_count+0.5*self.tick_count**2
        if displacement >=16:
            displacement = displacement/abs(displacement)*16
        elif displacement < 0:
            displacement -=2

        self.y = self.y +displacement

        if(displacement <0 or self.y < self.height+50):
            if self.tilt < self.MAX_ROT:
                self.tilt = self.MAX_ROT
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, window):
        self.img_count += 1

        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        rot_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rot_image.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)
        window.blit(rot_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)