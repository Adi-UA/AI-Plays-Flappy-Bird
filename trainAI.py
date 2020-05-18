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
    window.blit(BKG_IMAGE, (0,0))

    for pipe in pipes:
        pipe.draw(window)

    score_txt = STAT_FONT.render("Score: " + str(score),1,(255,255,255))
    window.blit(score_txt, (WIN_WIDTH-10-score_txt.get_width(),10))

    gen_txt = STAT_FONT.render("Generation: " + str(generation),1,(255,255,255))
    window.blit(gen_txt, (10,10))

    ground.draw(window)

    for bird in birds:
        bird.draw(window)

    pygame.display.update()


def eval(genomes, config):
    global GEN_NO
    GEN_NO += 1

    networks_list = []
    genome_list = []
    birds = []

    for g_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        networks_list.append(net)

        genome.fitness = 0

        birds.append(Bird(230,350))
        genome_list.append(genome)



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
        if len(birds) > 0:
            if len(pipes) > 1:
                if birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                    pipe_idx =1
        else:
            isRunning = False
            break

        for i,bird in enumerate(birds):
            bird.move()
            genome_list[i].fitness += 0.01

            output = networks_list[i].activate((bird.y, abs(bird.y - pipes[pipe_idx].height), abs(bird.y - pipes[pipe_idx].bottom)))
            if output[0] > 0.6:
                bird.jump()



        add_pipe = False

        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collide(bird):
                    genome_list[i].fitness -=1
                    birds.pop(i)
                    networks_list.pop(i)
                    genome_list.pop(i)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                pipes.remove(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            for genome in genome_list:
                genome.fitness += 2

            if score < 10:
                pipes.append(Pipe(600))
            elif score <= 20:
                pipes.append(HardPipe(600))
            else:
                pipes.append(RandomPipe(600))

        for i, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(i)
                networks_list.pop(i)
                genome_list.pop(i)

        if score >= 50:
            best_model = networks_list[0]
            nn_file = open("best_model.pickle", "wb")
            pickle.dump(best_model, nn_file)
            nn_file.close()
            break

        ground.move()
        draw_window(window, birds, pipes, ground, score, GEN_NO)



def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(eval,10)

def main():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "resources\config-feedforward.txt")
    run(config_path)

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

