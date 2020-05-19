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
    """
    This function draws game frames. It simultaenously displays all the birds
    being controlled by the neural net.

    Arguments: window  -- The pygame display window birds  -- The list of Bird
     objects which are being controlled by NNs. This should only contain living
     birds.  pipes  -- This list contains the pipes that must be drawn. All pipe
     classes implement draw so this list can have objects of type Pipe, HardPipe
     and RandomPipe.  ground  -- The Ground object score {int} -- The current
     score. This score will be equal for all birds since the NNs go through an
     equal number of frames in an equal amount of time.
    """
    window.blit(BKG_IMAGE, (0, 0))

    for pipe in pipes:
        pipe.draw(window)

    score_txt = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    window.blit(
        score_txt,
        (WIN_WIDTH - 10 - score_txt.get_width(), 10))  # top right of screen

    ground.draw(window)

    bird.draw(window)

    pygame.display.update()


def run_model(neural_net):
    """
    This funtion runs the Flappy Bird Game and allows the NN passed in to make
    decisons about when to jump. The activate function is given details about
    the bird's position at each frame as well as the bird's distance from the
    top and bottom of the gap in the upcoming pipe

    Arguments:
        neural_net  -- The NN with which the game is supposed to be run
    """

    bird = Bird(230, 350)
    ground = Ground(730)
    pipes = [Pipe(700)]  # Starting off with a normal pipe
    score = 0

    game_clock = pygame.time.Clock()

    isRunning = True
    while isRunning:
        game_clock.tick(60)

        # Handle Quitting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
                pygame.quit()
                quit()

        # At any time, there are at most two pipes on the screen becase that is
        # all it can accomodate. Here we tell the NN which pipe to look at when
        # deciding its bird's behavior
        pipe_idx = 0
        if len(pipes) > 1:
            if bird.x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_idx = 1

        # Move the bird and then allow the NN to choose if the bird should jump
        bird.move()
        output = neural_net.activate((bird.y,
                                      abs(bird.y - pipes[pipe_idx].height),
                                      abs(bird.y - pipes[pipe_idx].bottom)))
        if output[0] > 0.5:
            bird.jump()

        # Update pipes after the bird has made its move
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

            # Choose which pipe to add based on the score
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

        # Arbitrarily stop execution when score = 500
        if score >= 500:
            print(":)")
            break

        ground.move()
        draw_window(WINDOW, bird, pipes, ground, score)


def main():

    # Load stored NN
    nn_file = open("best_model.pickle", "rb")
    neural_net = pickle.load(nn_file)
    nn_file.close()

    # Use NN to run Flappy Bird
    run_model(neural_net)


if __name__ == "__main__":
    main()
