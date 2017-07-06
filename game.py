from player import *
from random import random

class State(object):
    ''' Class to represent game state

    This class contains all information that requires to update each turn.
    State object will be instanciated at the beginneing of game.
    Every turn the State instance will be updated uing update method.

    Attributes:
        players: an array of Player object
        active_players: an array of players who are still playing the game
        names: Hashset of player names to avoid duplicate players
        set_up: Boolean to block setting modifications once the game starts
    '''

    # player
    players = []
    # players who are still playing
    active_players = []
    # names
    names = set()
    # allowing setup
    set_up = True

    def __init__(self, player_type = 'human', player_name = 'Player 0'):
        ''' Constructor

        Create a State object by specifying at least one player
        Args:
            player_type: specifies the type of Player object. Default is an interactive human player
            player_name: the name of the player. Has to be unique from other players. Default is Player followed by the number of player (0 indexed)

        Raises:
            Exception : when the player names have duplicates
        '''
        if player_type == 'human':
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

    def add_player(self, player_type = 'human', name = ''):
        '''Add new players to the object

        Args:
            player_type: specifies the type of Player object. Default is an interactive human player
            player_name: the name of the player. Has to be unique from other players. Default is Player followed by the number of player (0 indexed)

        Raises:
            Exception : when the player names have duplicates
        '''
        # allows new player only if the game has not started
        if self.set_up:
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

    def update_state(self):
        ''' Run one deal of the game by updating the state object

        The game of baccarat proceeds as follows
        1. Collect bets and guesses from all active players
        2. Deal
        3. Distribute rewards to winners
        4. Remove players if they have no money left
        5. Continue
        '''
        # block modifications in setting once the game starts
        self.set_up = False

        # 1. Collect bets and guesses from all players
        guesses = []
        for p in self.active_players:
            guesses.append(p.bet())

        # 2. Deal
        result = self.deal()

        # 3. Distribute rewards to winners
        for index, g in enumerate(guesses): # unpack guesses
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


    def deal(self):
        ''' Baccarat deal simulator based on actual probability

        Simulate one deal of bacarrat with odds from http://www.baccaratstrategies.net/Baccarat-Probabilities.html

        player odds : 44.62%
        dealer odds : 45.85%
        tie : 9.53 %

        Args: None

        Return: integer encoding of game result
            0 : player wins
            1 : dealer wins
            2 : tie
        '''
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

    def cash_back(self, result, bet, price):
        '''
        Calculate the cash_back based on the game result, bet, and bet price based on the online source
        If player bets on player and wins, return 100%
        If player bets on dealer and wins, return 95%
        If player bets on tie and wins, return 800%
        Players will lose their commission unless the game ties and the player loses the bet

        Args:
            result: the integer encoding of game result (0 ~ 2)
            bet: the guess of the player (0 ~ 2)
            price: the amount of money the player bets. (1 ~ 20)

        Return:
            The int value for the player's gain accordingly by the odds from https://wizardofodds.com/games/baccarat/basics/
        '''
        cash = 0 # the player will lose their commission by default
        # if tie
        if result == 2:
            # if win, winner will get 800% of commision
            if result == bet:
                cash = 9*float(price)
            # if lose, winner will get the commision back
            else:
                cash = price
        # if player or dealer wins
        else:
            # if wins,
            if result == bet:
                # player wins
                if result == 0:
                    # if win, winner will get 100% of commission
                    cash = 2*float(price)
                # dealer wins
                elif result == 1:
                    # if win, winner will get 95% of commission
                    cash = 1.95*float(price)
        return cash

class Game(object):
    ''' Game class will be responsible for dealing with game cycle and updating state
    '''
    def __init__(self):
        pass
        
if __name__ == '__main__':
    s = State()
    for _ in range(100):
        s.update_state()
    s.players[0].show_stats()
