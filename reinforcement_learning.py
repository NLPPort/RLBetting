from player import *
from random import random

class ReinforcementLearning(Player):
    ''' subclass from player

    Discover its own betting system through learning
    In reinforcement learning, the agent learns to find the mapping function from the state to the possible commands

    player class includes all information that the agent needs to learn

    Attributes:
        Value: store state value for the value iteration

    State
    - budget : how much do they have left
    - net_gain : how much do they have won
    - last_win : is it on a streak ?
    - consecutive_wins : used for 31

    Operation
    - 0. bet current bet
    - 1. double current bet
    - 2. triple current bet
    - 3. quadruple current bet
    - 4. bet 1
    - 5. bet 2
    - 6. bet 4
    - 7. bet 8

    Use bellman equation and value iteration to find the optimal policy

    V(s) = [max gamma expected reward from the value of next state] + reward of current state
    '''
    def __init__(self, name = 'guest', gamma = 0.9):
        '''Constructor for RandomBet

        Args:
            name: name for the player. Defalut is 'guest'
        '''
        Player.__init__(self,name)

        # create state -> value dictionary
        # use tree structure
        # budget -> converted to percentage 90% -> 9, 128% -> 13
        # value = {budget: {gain: {last_win: {consecutive_wins: }}}}

        self.Value = {}
        self.Policy = {}
        self.gamma = gamma

    def percentRound(self, value, base):
        '''helper function

        value/base and return rounded value for the key

        Args:
            value: numerator
            base: denomenator

        Return:
            rounded value to be used as a key
        '''
        return round(float(value)/float(base),1)*10

    def search_next_state(self, state_tuple):
        ''' search for the state in V table. If this is the first time to
        explore this state, return a random value. otherwise return a
        state value.

        Args:
            state_tuple: a tuple representation of current state
        '''
        # layer to return
        last_states = len(state_tuple)-1
        # initialize local variables
        next_layer = {}
        next_state_value = 0
        for i,s in enumerate(state_tuple):
            if i == last_states:
                # if already registered, return the value
                try:
                    next_state_value = next_layer[s]
                # else register random value
                except:
                    next_state_value = random()
                    next_layer[s] = next_state_value
            elif i == 0:
                # iterate Value dict tree
                # whenever sees a new key, create a new dict
                try:
                    next_layer = self.Value[s]
                except:
                    self.Value[s] = {}
                    next_layer = self.Value[s]
            else:
                try:
                    next_layer = next_layer[s]
                except:
                    next_layer[s] = {}
                    next_layer = next_layer[s]
        return next_state_value

    def update_state_value(self, state_tuple, value):
        ''' search for the state in V table. register value to the given state

        Args:
            state_tuple: a tuple representation of a state
            value : a value to register
        '''
        # layer to return
        last_states = len(state_tuple)-1
        # initialize local variables
        next_layer = {}
        next_state_value = 0
        for i,s in enumerate(state_tuple):
            if i == last_states:
                next_layer[s] = value
            elif i == 0:
                # iterate Value dict tree
                # whenever sees a new key, create a new dict
                try:
                    next_layer = self.Value[s]
                except:
                    self.Value[s] = {}
                    next_layer = self.Value[s]
            else:
                try:
                    next_layer = next_layer[s]
                except:
                    next_layer[s] = {}
                    next_layer = next_layer[s]


    def reward_win(self, bet):
        ''' get the value of next state if you play given action and wins

        Args:
            bet: how much you bet on this round
        Return:
            value: the float value for the state value
        '''
        # assuming the AI will bet on the dealer
        # if wins, the budget will increase by .95 of current bet
        budget = self.percentRound(self.budget + .95 * bet, 100)
        # if wins, net gain will increase by .95 of current bet
        gain = self.percentRound(self.net_gain + .95 * bet, 100)
        # last win will be 0
        last_win = 0
        # add 1 to consective win, if 2 reset to 0
        consecutive_wins = self.consecutive_wins + 1
        if consecutive_wins == 2:
            consecutive_wins = 0

        # search for the next state
        state = (budget, gain, last_win, consecutive_wins)
        nextState = self.search_next_state(state)
        return nextState

    def reward_lose(self, bet):
        ''' get the value of next state if you play given action and loses

        Args:
            bet: how much you bet on this round
        Return:
            value: the float value for the state value
        '''
        # assuming the AI will bet on the dealer
        # if loses, the budget will decrease by current bet
        budget = self.percentRound(self.budget - bet, 100)
        # if wins, net gain will decrease by current bet
        gain = self.percentRound(self.net_gain - bet, 100)
        # last win will be current last win + 1
        last_win = self.last_win + 1
        # consecutive_wins will be 0
        consecutive_wins = 0

        # search for the next state
        state = (budget, gain, last_win, consecutive_wins)
        nextState = self.search_next_state(state)
        return nextState

    def command_map(self, command):
        ''' return the betting price of given command

        Args:
            command : the encoding of the command
                    - 0. bet current bet
                    - 1. double current bet
                    - 2. triple current bet
                    - 3. quadruple current bet
                    - 4. bet 1
                    - 5. bet 2
                    - 6. bet 4
                    - 7. bet 8
        Raises:
            Excaption: when the input was not a valid command
        Return:
            the result of betting price after taking the input command
        '''
        if command == 0:
            bet = self.current_bet
        elif command == 1:
            bet = 2 * self.current_bet
        elif command == 2:
            bet = 3 * self.current_bet
        elif command == 3:
            bet = 4 * self.current_bet
        elif command == 4:
            bet = 1
        elif command == 5:
            bet = 2
        elif command == 6:
            bet = 4
        elif command == 7:
            bet = 8
        else:
            raise Exception('invalid command')
        return bet


    def valueIteration(self):
        '''update the current state value using bellman equation
        '''
        # current state
        reward  = self.net_gain
        budget  = self.percentRound(self.budget, 100)
        gain  = self.percentRound(self.net_gain, 100)
        last_win = self.last_win
        consecutive_wins = self.consecutive_wins

        # craete a state tuple
        current_state = (budget, gain, last_win, consecutive_wins)

        max_expectation = float('-inf')
        best_command = -1
        for i in range(8):
            bet = self.command_map(i)
            # bet on dealer
            # win .4585
            # lose .4462
            # tie .0953
            expectation = .4585*self.reward_win(bet)+.4462*self.reward_lose(bet)+.0953*self.search_next_state(current_state)
            if max_expectation < expectation:
                max_expectation = expectation
                best_command = i

        # the value iteration using bellman equation
        new_V = self.gamma * max_expectation + reward
        # register the value
        self.update_state_value(current_state, new_V)
        return best_command

    def bet(self):
        ''' decides bet price and guess for the next deal

        Overload this method so that every turn it will output random betting price

        Returns:
            a tuple representing guess and bet
            ('guess', 'bet')
            guess: the integer encoding for the game result, default is set to 1 (dealer)
            bet: integer representation of the betting price (0 - 20)

        Raises:
            Exception: when the player tries to bet without any money left
        '''
        # throw an exception if the player does not have any money left
        if self.budget == 0:
            raise Exception ('you lost the game')
        # random bet
        bet = self.command_map(self.valueIteration())
        # if player tries to bet more than they have, it automatically plays all-in
        if bet > self.budget:
            bet = self.budget
        # update current bet
        self.current_bet = bet
        # pay commission
        self.budget -= bet
        # TODO if we implement interactive version, player should be able to choose the bet
        return 1, bet

    def end_game_reward(self, encoding, total):
        ''' Update 7/16 version
        When agent wins or loses, we need to teach them the value other than the net gain.
        For example, if the agent survive all round, we need to give them award,
        if the agent loses early, we need to give them penalty

        Args:
            encoding: 0 means survived, 1 means lost
            total: total number of games to be played. Used to calculate the penalty
        '''

        # current state
        budget  = self.percentRound(self.budget, 100)
        gain  = self.percentRound(self.net_gain, 100)
        last_win = self.last_win
        consecutive_wins = self.consecutive_wins

        state = (budget, gain, last_win, consecutive_wins)
        if encoding == 0:
            self.update_state_value(state, gain + self.round)
        elif encoding == 1:
            self.update_state_value(state, gain - 100*(total - self.round))



if __name__ == '__main__':
    p = ReinforcementLearning()
    print p.search_next_state((1,2,3,4))
    print p.search_next_state((1,2,3,4))
    print p.update_state_value((1,2,3,4), 1)
    print p.search_next_state((1,2,3,4))
