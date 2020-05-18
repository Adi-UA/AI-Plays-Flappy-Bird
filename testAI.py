import pygame
import time
import os
import pickle
from resources.reference import *
from gamesrc.bird import Bird
from gamesrc.ground import Ground
from gamesrc.pipe import Pipe
from gamesrc.hardpipe import HardPipe
from gamesrc.randompipe import RandomPipe


def draw_window(window, bird, pipes, ground, score):
    window.blit(BKG_IMAGE, (0,0))

    for pipe in pipes:
        pipe.draw(window)

    score_txt = STAT_FONT.render("Score: " + str(score),1,(255,255,255))
    window.blit(score_txt, (WIN_WIDTH-10-score_txt.get_width(),10))

    ground.draw(window)

    bird.draw(window)

    pygame.display.update()


def run_model(neural_net):

    bird = Bird(230,350)
    ground = Ground(730)
    pipes = [Pipe(700)]
    score = 0

    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    game_clock = pygame.time.Clock()

    isRunning = True
    while isRunning:
        game_clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
                pygame.quit()
                quit()

        pipe_idx = 0
        if len(pipes) > 1:
            if bird.x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_idx =1

        bird.move()
        output = neural_net.activate((bird.y, abs(bird.y - pipes[pipe_idx].height), abs(bird.y - pipes[pipe_idx].bottom)))
        if output[0] > 0.5:
            bird.jump()

        add_pipe = False

        for pipe in pipes:
            if pipe.collide(bird):
                print("You Lost")
                print("Score: " + str(score))
                return

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                pipes.remove(pipe)

            pipe.move()

        if add_pipe:
            score += 1

            if score < 10:
                pipes.append(Pipe(600))
            elif score <= 20:
                pipes.append(HardPipe(600))
            else:
                pipes.append(RandomPipe(600))


        if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
            print("You Lost")
            print("Score: " + str(score))
            return

        if score >= 500:
            break

        ground.move()
        draw_window(window, bird, pipes, ground, score)

def main():
    nn_file = open("best_model.pickle", "rb")
    neural_net = pickle.load(nn_file)
    nn_file.close()

    run_model(neural_net)

if __name__ == "__main__":
    main()
