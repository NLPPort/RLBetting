from player import *
from ai import *
from reinforcement_learning import *
from random import random

class State(object):
    ''' Class to represent game state

    This class contains all information that requires to update each turn.
    State object will be instanciated at the beginneing of game.
    Every turn the State instance will be updated uing update method.

    Attributes:
        players: an array of Player object, when player finished playing, push to this array
        active_players: an array of players who are still playing the game
        names: Hashset of player names to avoid duplicate players
        set_up: Boolean to block setting modifications once the game starts
    '''

    def __init__(self, player_type = 'human', player_name = 'Player 0'):
        ''' Constructor

        Create a State object by specifying at least one player
        Args:
            player_type: specifies the type of Player object. Default is an interactive human player
            player_name: the name of the player. Has to be unique from other players. Default is Player followed by the number of player (0 indexed)

        Raises:
            Exception : when the player names have duplicates
        '''
        # players
        self.players = []
        # name
        self.names = set()
        # players who are still playing
        self.active_players = []
        # allowing setup
        self.set_up = True

        if player_type == 'human':
            if not player_name in self.names:
                # instanciate player
                player = Player(player_name)
                # append player objet
                self.active_players.append(player)
                # add name list
                self.names.add(player_name)
            else:
                raise Exception('player already exists')

        if player_type == 'random':
            if not player_name in self.names:
                # instanciate player
                player = RandomBet(player_name)
                # append player objet
                self.active_players.append(player)
                # add name list
                self.names.add(player_name)
            else:
                raise Exception('player already exists')

        if player_type == '1324':
            if not player_name in self.names:
                # instanciate player
                player = System1324(player_name)
                # append player objet
                self.active_players.append(player)
                # add name list
                self.names.add(player_name)
            else:
                raise Exception('player already exists')

        if player_type == '31':
            if not player_name in self.names:
                # instanciate player
                player = Parlay31(player_name)
                # append player objet
                self.active_players.append(player)
                # add name list
                self.names.add(player_name)
            else:
                raise Exception('player already exists')

        if player_type == 'martingale':
            if not player_name in self.names:
                # instanciate player
                player = Martingale(player_name)
                # append player objet
                self.active_players.append(player)
                # add name list
                self.names.add(player_name)
            else:
                raise Exception('player already exists')

        if player_type == 'flat':
            if not player_name in self.names:
                # instanciate player
                player = Flat(player_name)
                # append player objet
                self.active_players.append(player)
                # add name list
                self.names.add(player_name)
            else:
                raise Exception('player already exists')

        if player_type == 'rl':
            if not player_name in self.names:
                # instanciate player
                player = ReinforcementLearning(player_name)
                # append player objet
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
                    name = 'Player ' + str(len(self.active_players))
                if not name in self.names:
                    # initialize player
                    self.active_players.append(Player(name))
                    # append name list
                    self.names.add(name)
                else:
                    raise Exception('player already exists')

            if player_type == 'random':
                if len(name) == 0:
                    name = 'Player ' + str(len(self.active_players))
                if not name in self.names:
                    # initialize player
                    self.active_players.append(RandomBet(name))
                    # append name list
                    self.names.add(name)
                else:
                    raise Exception('player already exists')

            if player_type == '1324':
                if len(name) == 0:
                    name = 'Player ' + str(len(self.active_players))
                if not name in self.names:
                    # initialize player
                    self.active_players.append(System1324(name))
                    # append name list
                    self.names.add(name)
                else:
                    raise Exception('player already exists')

            if player_type == '31':
                if not name in self.names:
                    # instanciate player
                    player = Parlay31(name)
                    # append player objet
                    self.active_players.append(player)
                    # add name list
                    self.names.add(name)
                else:
                    raise Exception('player already exists')

            if player_type == 'martingale':
                if not name in self.names:
                    # instanciate player
                    player = Martingale(name)
                    # append player objet
                    self.active_players.append(player)
                    # add name list
                    self.names.add(name)
                else:
                    raise Exception('player already exists')

            if player_type == 'flat':
                if not name in self.names:
                    # instanciate player
                    player = Flat(name)
                    # append player objet
                    self.active_players.append(player)
                    # add name list
                    self.names.add(name)
                else:
                    raise Exception('player already exists')

            if player_type == 'rl':
                if not name in self.names:
                    # instanciate player
                    player = ReinforcementLearning(name)
                    # append player objet
                    self.active_players.append(player)
                    # add name list
                    self.names.add(name)
                else:
                    raise Exception('player already exists')

    def return_Vtable(self):
        '''should be called only when the traning phase

        return the V table from the learning agent
        '''
        rl = self.players[0]
        return rl.Value

    def set_vtable(self, vtable):
        '''should be called only when the traning phase

        set the vtable for the learining agent
        '''
        rl = self.players[0]
        rl.Value = vtable


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

        # at least one player has to be playing the game
        if len(self.active_players)>0:

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
                # if player's budget is 0, remove player from the active game
                if player.budget == 0:
                    self.active_players.remove(player)
                    self.players.append(player)
                # player.show_stats()

    def returnResult(self, index = 0):
        ''' Return the net win of the player at given index

        Args:
            index: the index of player in the list, default is 0

        Return:
            the net win of given player

        Raises:
            Exception: when index is out of range
        '''
        if index+1 < len(self.players):
            raise Exception('Index out of range')

        return self.players[0].net_gain


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

    Attributes:
        state: the game state
        rounds: how many games of baccarat the player wants to play
        default is 10
        ready_to_play: boolean to block users to play the game without setting
    '''

    state = None
    rounds = 10
    ready_to_play = False
    def __init__(self):
        pass

    def set_up(self, console = True):
        '''instantiate the game state

        This method has to be called before starting the game
        change the ready_to_play attribute to True at the end of
        this function

        Args:
            console: if True set up is done in console
        '''

        player_type = ''

        set_up = True

        # terminal setting
        if console:
            # wait user input for the correct player type
            while player_type not in ['human', 'random', '1324', '31', 'martingale', 'flat', 'rl']:
                player_type = raw_input("select player type (human, random, 1324, 31, martingale, flat, rl): ")
            # wait user input fot the player name, default if empty
            player_name = raw_input("select player name (default if empty): ")

            # set up state
            if len(player_name) == 0:
                self.state = State(player_type = player_type)
            else:
                self.state = State(player_type = player_type, player_name = player_name)

            # wait user input for additional
            while set_up:
                YorN = ''
                while YorN not in ['Y', 'N']:
                    YorN = raw_input("select more players? (Y or N): ")

                # if N, move exit the function
                if YorN == 'N':
                    set_up = False
                # if Y, ask for another player
                else:
                    player_type = ''
                    while player_type not in ['human', 'random', '1324', '31', 'martingale', 'flat', 'rl']:
                        player_type = raw_input("select player type (human, random, 1324, 31, martingale, flat, rl): ")

                    player_name = raw_input("select player name (default if empty): ")

                    self.state.add_player(player_type = player_type, name = player_name)

        self.ready_to_play = True

    def add_player(self, player_type = 'random'):
        '''add player to the game state

        Args:
            player_type: type of player to add

        Raises:
            Exception: when the invalid player type is detected
        '''
        if player_type not in ['human', 'random', '1324', '31', 'martingale', 'flat', 'rl']:
            Exception('invalid player type')

        if not self.state:
            self.state = State(player_type = player_type)
        else:
            self.state.add_player(player_type = player_type)

    def set_game_round(self, rounds):
        '''set the number of games the player want to play before finishing the game
        default is set to 10 games
        When training AI, this value should be high, (1000 ~)

        Args:
            rounds: int value specifying the number of games to play

        Raises:
            Exception: if the input is 0 or not a number
        '''

        if type(rounds) != type(0) or rounds == 0:
            raise  Exception('Invalid round number')

        else:
            self.rounds = rounds

    def play(self, do_print = True):
        '''start the game loop

        check if the set up is complete.
        If so, start iterating the state update by the number of rounds

        Args:
            do_print: boolean to control if you want to print game stats on console
        '''
        if self.set_up:
            for _ in range(self.rounds):
                self.state.update_state()

            # all active players to players
            for p in self.state.active_players:
                self.state.players.append(p)

            if do_print:
                for p in self.state.players:
                    print 'Stats for ' + p.get_name()
                    print ' '
                    p.show_stats()
        else:
            print ('finish setup first')

    def train(self, do_print = True):
        '''start the game loop for reinforcement learning agent

        check if the set up is complete.
        If so, start iterating the state update by the number of rounds

        Args:
            do_print: boolean to control if you want to print game stats on console

        Return:
            Vtable from the learning agent
        '''
        if self.set_up:
            for _ in range(self.rounds):
                self.state.update_state()

            # all active players to players
            for p in self.state.active_players:
                self.state.players.append(p)

            if do_print:
                for p in self.state.players:
                    print 'Stats for ' + p.get_name()
                    print ' '
                    p.show_stats()

        return self.state.return_Vtable()

    def update_Vtable(self, vtable):
        ''' update the Vtable from the previous learning iteration

        Args:
            vtable: dict representation of vtable
        '''
        self.state.set_vtable(vtable)

    def reset(self):
        '''Clean up the setting for the another game
        '''
        del self.state
        self.state = None
        self.rounds = 10
        self.ready_to_play = False


def main():
    '''main game loop
    set up Game object, and enter the loop
    '''
    # create an object
    g = Game()
    # set_up
    g.set_up()
    g.set_game_round(30)
    # enter the loop
    g.play()


if __name__ == '__main__':
    main()
