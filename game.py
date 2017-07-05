from player import *
from random import random

'''
This class represents each game state of the bacarrat
When training RL agent, this class will be its input
'''

class State:
    ## Game state##
    # player
    players = []
    # players who are still playing
    active_players = []
    # names
    names = set()
    # how many games has been played
    rounds = 0
    # current player
    current = 0

    '''
    the constructor of the state represents the initial state of each player
    '''
    def __init__(self, player_type = 'human', player_name = 'Player 0'):
        if player_type == 'human':
            # I could ask for name input here
            if not player_name in self.names:
                # instanciate player
                player = Player(player_name)
                # append player objet
                self.players.append(player)
                self.active_players.append(player)
                # add name list
                self.names.add(player_name)
            else:
                raise Exception('player already exists')

    '''
    add new player to the game
    throw an exception if the player already exists
    '''
    def add_player(self, name = '', player_type = 'human'):
        if player_type == 'human':
            if len(name) == 0:
                name = 'Player ' + str(len(self.players))
            if not name in self.names:
                # initialize player
                self.players.append(Player(name))
                self.active_players.append(Player(name))
                # append name list
                self.names.add(name)
            else:
                raise Exception('player already exists')


    '''
    update state by executing one deal of bacarrat
    1. first collect the bet from all playrs
    2. then dael the game
    3. finally return the winning value to all players
    '''
    def update_state(self):
        guesses = []
        # get current player
        for p in self.active_players:
            guesses.append(p.bet())


        # once player starts the game, they cannot quit unless player's monwy is already 0

        # bacaratt game odds
        result = self.deal()

        # # calculate the cash-back
        for index, g in enumerate(guesses):
            # get the current player
            player = self.active_players[index]
            # calculate the cash back
            value = self.cash_back(result, g[0], g[1])
            # update the budget1
            player.retrieve(value)
            # update the information in player onject
            player.update(value)
            print player.budget
            # if player's budget is 0, remove player from the active game
            if player.budget == 0:
                self.active_players.remove(player)

        # shift the index
        self.current = self.current+1 if self.current+1 < len(self.players) else 0




    '''
    simulate one deal of bacarrat with odds from online source
    player odds : 44.62%
    dealer odds : 45.85%
    tie : 9.53 %

    return integer encoding of game result
    0 : player
    1 : dealer
    2 : tie
    '''
    def deal(self):
        prob = random()
        # player wins with 44.62%
        if prob < .4462:
            return 0
        # dealer wins with 45.85%
        elif prob < .9047:
            return 1
        # tie with 9.53%
        else:
            return 2


    '''
    Calculate the cash_back based on the game result, bet, and bet price based on the online source
    '''
    def cash_back(self, result, bet, price):
        cash = 0
        # if tie
        if result == 2:
            if result == bet:
                cash = 8 * float(price)

            else:
                cash = price
        # if player or dealer wins
        else:
            # correctly guessed
            if result == bet:
                # player wins
                if result == 0:
                    cash = 2 * float(price)
                # dealer eins
                elif result == 1:
                    cash = 1.95 * float(price)

        return cash




'''
Update State
initialize state
run game
'''
class Game:
    def __init__(self):
        self.state = State()
        self.players = []


if __name__ == '__main__':
    s = State()
    for _ in range(1000):
        s.update_state()
    s.players[0].show_stats()
