import pygame
import neat
import time
import os
import pickle
from resources.reference import *
from gamesrc.bird import Bird
from gamesrc.ground import Ground
from gamesrc.pipe import Pipe
from gamesrc.hardpipe import HardPipe
from gamesrc.randompipe import RandomPipe


def draw_window(window, birds, pipes, ground, score, generation):
    """T
    his function draws game frames. It simultaenously displays all the birds
    being controlled by the neural net.

    Arguments: window  -- The pygame display window birds  -- The list of Bird
     objects which are being controlled by NNs. This should only contain living
     birds.  pipes  -- This list contains the pipes that must be drawn. All pipe
     classes implement draw so this list can have objects of type Pipe, HardPipe
     and RandomPipe.  ground  -- The Ground object score {int} -- The current
     score. This score will be equal for all birds since the NNs go through an
     equal number of frames in an equal amount of time.  generation {int} -- The
     current generation number of the NNs.
    """
    window.blit(BKG_IMAGE, (0, 0))

    for pipe in pipes:
        pipe.draw(window)

    score_txt = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    window.blit(
        score_txt,
        (WIN_WIDTH -
         10 -
         score_txt.get_width(),
         10))  # top right of screen

    gen_txt = STAT_FONT.render(
        "Generation: " + str(generation), 1, (255, 255, 255))
    window.blit(gen_txt, (10, 10))  # top left of screen

    ground.draw(window)

    for bird in birds:
        bird.draw(window)

    pygame.display.update()


def eval(genomes, config):
    """
    This function runs through the game allowing the NNs built from the given
    genomes to control the bird's moves at each frame. The parameters must be
    provided in the config file.

    The decision made by the NN at each frame is wheter or not it should jump.
    This decision is made based on the NN's bird's current height and its
    distance from the top and bottom of the gap in the upcoming pipe.
    """
    global GEN_NO
    GEN_NO += 1

    # Store corresponding birds, networks and genomes
    networks_list = []
    genome_list = []
    birds = []

    # We don't require the genome id
    for g_id, genome in genomes:

        net = neat.nn.FeedForwardNetwork.create(genome, config)
        networks_list.append(net)

        genome.fitness = 0

        birds.append(Bird(230, 350))
        genome_list.append(genome)

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
        if len(birds) > 0:
            if len(pipes) > 1:
                if birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                    pipe_idx = 1
        else:
            isRunning = False
            break

        for i, bird in enumerate(birds):
            bird.move()
            # 'reward' for making it to this frame
            genome_list[i].fitness += 0.01

            # NN Decision absed its bird's position as well as the position of
            # the top and bottom of the gap in the relevant pipe.
            output = networks_list[i].activate((bird.y, abs(
                bird.y - pipes[pipe_idx].height), abs(bird.y - pipes[pipe_idx].bottom)))
            if output[0] > 0.6:
                bird.jump()

        # Update pipes after the bird has made its move
        add_pipe = False
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collide(bird):
                    # The bird died so we subtract fitness from the genome and
                    # remove its controlling genome and NN from the lists.
                    genome_list[i].fitness -= 1
                    birds.pop(i)
                    networks_list.pop(i)
                    genome_list.pop(i)

                if not pipe.passed and pipe.x < bird.x:
                    # If we pass a pipe we must remember to add a new one
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                # When a pipe leaves the game window we clean up the object
                pipes.remove(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            for genome in genome_list:
                # All genomes in this list must have passed a pipe (since we are
                # adding a new pipe) so all of them are given fitness points
                genome.fitness += 2

            # Depending on the score, we change the type of pipe to add
            if score < 10:
                pipes.append(Pipe(600))
            elif score <= 20:
                pipes.append(HardPipe(600))
            else:
                pipes.append(RandomPipe(600))

        for i, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                # Birds at ground level or above the top edge level are dead and
                # will be removed.
                birds.pop(i)
                networks_list.pop(i)
                genome_list.pop(i)

        if score >= 55:
            # Reaching 55 is sufficient to demonstrate a reasonably accurate
            # model, so we store the model in a .pickle file.

            best_model = networks_list[0]
            nn_file = open("best_model.pickle", "wb")
            pickle.dump(best_model, nn_file)
            nn_file.close()
            break

        ground.move()
        draw_window(WINDOW, birds, pipes, ground, score, GEN_NO)


def run(config_path):
    """
    This function runs each generation of NNs using the configuration file
    passed to it.

    Arguments:
        config_path  -- Path to the NNs config file
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    population = neat.Population(config)  # Population of NNs
    population.add_reporter(neat.StdOutReporter(True))

    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(eval, 15)
    # Run 15 generations at most. This usually results in a very accurate
    # 'checkpoint' model


def main():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, r"resources\config-feedforward.txt")
    run(config_path)

    # Once the model is trained and a best model has been generated, the user
    # may choose to test the best model.
    ch = -1
    while(ch == -1):
        print("Do you want to run the trained model? (y/n)")
        ch = input()[0].lower()
        if ch == "y":
            os.system('python testAI.py')
        elif ch == "n":
            break
        else:
            print("Not a valid choice")


if __name__ == "__main__":
    main()
