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
        for p in player_types:
            netWin = np.array([])
            for _ in range(self.repeat):
                self.game.add_player(player_type = p)
                self.game.set_game_round(100)
                self.game.play()
                netWin = np.append(netWin, self.game.state.returnResult())
                self.game.reset()
            sns.distplot(netWin, hist=False, label = p)
        plt.title('Martingale System Return Rate')
        plt.xlabel('Net Return in Unit (Starting from 100)')
        plt.ylabel('Frequency')
        # plt.savefig('result/100-500_martingale.png')
        plt.show()


    def train(self, iteration = 100, print_result = False):
        ''' train reinforcement learning agent with the given number of iterations

        Args:
            iteration: number of iteration the agent plays the game
        '''

        self.game = Game()
        Vtable = {}
        netWin = np.array([])
        counter = 0
        for i in range(iteration):
            self.game.add_player(player_type = 'rl')
            self.game.set_game_round(10)
            mod100 = (counter % 1000 == 0)
            Vtable = self.game.train(do_print = mod100)
            self.game.update_Vtable(Vtable)
            if mod100:
                netWin = np.append(netWin, self.game.state.returnResult())
            self.game.reset()
            counter += 1
        print self.get_Vtable_size(Vtable)
        if print_result:
            plt.plot(netWin)
            plt.show()


    def get_Vtable_size(self, vtable):
        '''Return the number of states the Vtable has visited

        Args:
            vtable: vtable to investigate

        Returns:
            number of states that vtable includes
        '''
        count = len(vtable)
        for i in (vtable.keys()):
            count += len(vtable[i])
            for j in vtable[i].keys():
                count += len(vtable[i][j])
                for k in vtable[i][j].keys():
                    count += len(vtable[i][j][k])
        return count


if __name__ == '__main__':
    s = Simulation()
    s.train(print_result = True)
