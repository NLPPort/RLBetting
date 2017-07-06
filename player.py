from deck import *
from random import randint
'''
Player class represents each player of bacarrat
'''
class Player:
    name  = ''
    budget = 0
    # player is initialized with 1000 initial capital if not specified
    def __init__(self, name = 'guest'):
        # name is a key for the players dictionary
        self.name = name
        # current game round
        self.round = 0
        # budget
        self.budget = 100
        # total win games
        self.win = 0
        # total win money
        self.net_gain = 0
        # last win since
        self.last_win = 0
        # current bet
        self.current_bet = 1
        # return for the biggest win
        self.biggest_win = 0
        # loss for the biggest loses
        self.biggest_loss = 0
        # consecutive win
        self.consecutive_wins = 0
        # consecutive loss
        self.consecutive_loss = 0
        # total wins in previous 3 games
        self.total_win_in_past_3 = 0
        # total wins in previous 5 games
        self.total_win_in_past_5 = 0
        # total wins in previous 10 games
        self.total_win_in_past_10 = 0
        # total loss in previous 3 games
        self.total_loss_in_past_3 = 0
        # total loss in previous 5 games
        self.total_loss_in_past_5 = 0
        # total wins in previous 10 games
        self.total_loss_in_past_10 = 0
        # save the game record
        self.game_record = []

    '''
    Each player is able to bet money on dealer.
    Decide how much unit of money they will bet
    '''
    def bet(self):
        bet = randint(1,20)
        if self.budget == 0:
            raise Exception ('you lost the game')
        bet = 0
        while bet not in range(1,21):
            bet = raw_input("How much you want to bet (1 - 20): ")
            try:
                bet = int(bet)
            except:
                bet = 0
        if bet > self.budget:
            bet = self.budget
        self.current_bet = bet
        self.budget -= bet
        # TODO if we implement interactive version, player should be able to choose the bet
        return 1, bet

    '''
    update the current budget by input value
    '''
    def retrieve(self, value):
        self.budget += value

    '''
    Return the name of the player
    The name of player is a key for the players dictionary in state obj
    '''
    def get_name(self):
        return self.name

    '''
    Private method to count number of X in array
    '''
    def __countX(self, x, array):
        count = 0
        for i in array:
            if x == i:
                count += 1
        return count

    def update(self, value):
        self.round += 1
        if value == 0:
            result = 'L'
        elif value == self.current_bet:
            result = 'T'
        else:
            result = 'W'
        self.game_record.append(result)
        if len(self.game_record) >= 3:
            self.total_win_in_past_3 = self.__countX('W', self.game_record[-3:])
        if len(self.game_record) >= 5:
            self.total_win_in_past_5 = self.__countX('W', self.game_record[-5:])
        if len(self.game_record) >= 10:
            self.total_win_in_past_10 = self.__countX('W', self.game_record[-10:])
        if len(self.game_record) >= 3:
            self.total_loss_in_past_3 = self.__countX('L', self.game_record[-3:])
        if len(self.game_record) >= 5:
            self.total_loss_in_past_5 = self.__countX('L', self.game_record[-5:])
        if len(self.game_record) >= 10:
            self.total_loss_in_past_10 = self.__countX('L', self.game_record[-10:])

        # lost the previous game
        if value == 0:
            self.last_win += 1
            self.net_gain -= self.current_bet
            if self.biggest_loss > -self.current_bet:
                self.biggest_loss = -(self.current_bet)
            self.consecutive_wins = 0
            self.consecutive_loss += 1
            return None

        # tied the previous game
        elif value == self.current_bet:
            self.last_win += 1
            return None

        # won the previous game
        else:
            self.win += 1
            self.last_win = 0
            self.net_gain += (value - self.current_bet)
            self.consecutive_wins += 1
            self.consecutive_loss = 0
            if self.biggest_win < (value - self.current_bet):
                self.biggest_win = value - self.current_bet
            return None


    '''
    Print the stats of player on console
    '''
    def show_stats(self):
        print 'total played: ' + str(self.round)
        print 'total win: ' + str(self.win)
        print 'last win since: ' + str(self.last_win)
        print 'net win: ' + str(self.net_gain)
        print 'biggest win: ' + str(self.biggest_win)
        print 'biggest loss: ' + str(self.biggest_loss)
        print 'consecutive wins: ' + str(self.consecutive_wins)
        print 'consecutive loss: ' + str(self.consecutive_loss)
        print 'total win in recent 3: ' + str(self.total_win_in_past_3)
        print 'total win in recent 5: ' + str(self.total_win_in_past_5)
        print 'total win in recent 10: ' + str(self.total_win_in_past_10)
        print 'total loss in recent 3: ' + str(self.total_loss_in_past_3)
        print 'total loss in recent 5: ' + str(self.total_loss_in_past_5)
        print 'total loss in recent 10: ' + str(self.total_loss_in_past_10)
