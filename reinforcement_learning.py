from player import *

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

    def RewardWin(self, bet):
        ''' get the value of next state if you play given action and wins

        Args:
            bet: how much you bet on this round
        Return:
            value: the float value for the state value
        '''
        # assuming the AI will bet on the dealer
        # if wins, the budget will increase by .95 of current bet
        budget = self.budget + .95 * bet
        # if wins, net gain will increase by .95 of current bet
        gain = self.gain + .95 * bet
        # last win will be 0
        last_win = 0
        # add 1 to consective win, if 2 reset to 0
        consecutive_wins = self.consecutive_wins + 1
        if consecutive_wins == 2:
            consecutive_wins = 0




    def valueIteration(self):
        '''update the current state value using bellman equation
        '''
        # current state
        reward  = self.current_net
        budget  = self.percentRound(self.budget, 100)
        gain  = self.percentRound(self.gain, 100)
        last_win = self.last_win
        consecutive_wins = self.consecutive_wins

        # bet on dealer
        # win .4585

        # lose .4462
        # tie .0953





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
        bet = randint(1,20) # choose randomly from 1 to 20
        # if player tries to bet more than they have, it automatically plays all-in
        if bet > self.budget:
            bet = self.budget
        # update current bet
        self.current_bet = bet
        # pay commission
        self.budget -= bet
        # TODO if we implement interactive version, player should be able to choose the bet
        return 1, bet
