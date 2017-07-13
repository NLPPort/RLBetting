import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from game import *

class Simulation(object):
    ''' Class to automize learning / testing process

    the density plot is shown using seaborn library

    Attributes:
        game: Game object
    '''
    game = None
    repeat = 0
    def __init__(self, repeat = 1000):
        ''' Constructor

        Create a single Simulation class that controls training / testing
        graphing / storing the result

        Args:
            (optional) repeat: number of simulations for each models. default is 1000
        '''
        self.repeat = repeat

    def plot_density(self, player_types):
        '''plot the result of repeated simulation of models

        Args:
            player_types: an array of player types

        Raises:
            Exception: when the player_type is invalid
        '''
        # instanciate game class

        self.game = Game()
        for i in range(6,11):
            netWin = np.array([])
            for _ in range(self.repeat):
                for n in player_types:
                    self.game.add_player(player_type = n)
                self.game.set_game_round(i*10)
                self.game.play()
                netWin = np.append(netWin, self.game.state.returnResult())
                self.game.reset()
            sns.distplot(netWin, hist=False, label = str(i*10) + ' rounds')
        plt.title('Random Bet Return Rate')
        plt.xlabel('Net Return in Unit (Starting from 100)')
        plt.ylabel('Frequency')
        plt.savefig('result/60-100_random.png')
        # plt.show()

if __name__ == '__main__':
    s = Simulation()
    s.plot_density(['random'])
