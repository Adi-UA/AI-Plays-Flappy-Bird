# Overview
This project uses [`NEAT`](https://neat-python.readthedocs.io/en/latest/neat_overview.html) and [`Pygame`](https://www.pygame.org/news) to create a variation of Flappy Bird and beat it using NEAT's Neural Networks. 

This project is based on [Tech With Tim's](https://www.youtube.com/channel/UC4JX40jDee_tINbkjycV4Sg) Flappy Bird AI tutorial but they aren't quite the same. The differences will become apparent in the following sections, but in general, this project trains a neural net on variying pipe gaps and adds functionality to store and test models using `pickle`. This does mean, however, that the model takes longer to train and the `best_model.pickle` file provided isn't the finest architecture by a long shot, but it still works very well for the most part.

# The Game
For context, it is good to understand what the game is so you understand what the neural network is trying to do. 

In Flappy Bird, the person (or machine!) controlling the bird must ask the bird to "jump" at exactly the right times to make sure the bird can pass through the narrow gaps in the pipes it encounters (it encounters a shockingly large number of them). 

Pipes with the same gap size are boring, however, so in this variation of Flappy Bird the pipes get harder and more random as the game progresses. Currently there are three types of pipes:
1. The normal pipe with huge gap sizes. The first 10 pipes are always normal pipes.
2. The hard pipes with much smaller gap sizes. These pipes are encountered after the bird has crossed its first 10 pipes. It stops constantly encountering these when it has crossed 20 pipes.
3. The random pipes with varying gaps. These pipes are encountered once the bird has crossed the 20-point score mark. Their gap sizes vary from being as difficult as the hard pipes to a little more difficult than the normal pipe.

All the modules used to create the game can be found in `gamesrc`

# Using
## Before Running (Assuming you have pip)
* Run `pip install pygame` in the terminal
* Run `pip install neat-python`

**Note:** I am using `pygame 1.9.6`, `neat-python 0.92` and `python 3.7.4`

## Running
### Training (Optional)
If you don't want to use the trained model that comes with this repository in `best_model.pickle`, simply run the `trainAI.py` module. Running the module will train the model for upto 15 generations with a population size of 100 in each generation; when it finds a satisfactory model then it will store it inside `best_model.pickle`. Once done, it will prompt you to enter yes or no (y/n) for if you want to run the best model you just trained.

### Testing
When you're ready to see a trained AI controlling the bird, simply run the `testAI.py` module. Running the module will fire up a game of Flappy Bird in which the bird is controlled by the neural net stored in `best_model.pickle`. See how far it gets!

## Modifying Neural Net Parameters
Chances are you don't just want to train the AI on my category values and are looking to spice things up with some of yuor own. In that case, I will assume you are at least somewhat familiar with `NEAT` so I won't explain in detail below.

### Modify the config file for the NN
The config file can be found in the `resources` directory as `config-feedforward.txt`
You can change any or all of the parameters in this file and see how that affects model training and accuracy.

### Modify the code in trainAI.py
I've documented each step of the code fairly well, so if you're familiar with `NEAT` it should be easy to follow the code and figure out where genome fitness values are being incremented and decremented. 
