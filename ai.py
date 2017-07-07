from player import *
from random import randint

class RandomBet(Player):
    '''subclass from Player

    Simply bet a rondom amount
    '''

    def __init__(self, name = 'guest'):
        '''Constructor for RandomBet

        Args:
            name: name for the player. Defalut is 'guest'
        '''
        Player.__init__(self,name)

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


class System1324(Player):
    '''subclass from Player

    Simulate 1-3-2-4 system from http://www.fortunepalace.co.uk/1324.html
    Quote from the website:
        If a bet wins, you progress to the next bet in the sequence.
        If a bet loses, you go back to the start.
        If you win all four bets and complete the sequence, you go back to the start, having made 10 units profit!
    '''

    def __init__(self, name = 'guest'):
        '''Constructor for RandomBet

        Args:
            name: name for the player. Defalut is 'guest'
        '''
        Player.__init__(self,name)
        self.current_bet = 4

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

        # 1-3-2-4 system
        # won previous game
        if self.last_win == 0:
            if self.current_bet == 1:
                bet = 3
            elif self.current_bet == 3:
                bet = 2
            elif self.current_bet == 2:
                bet = 4
            elif self.current_bet == 4:
                bet = 1
            # if you can onlt bet 1 and cannot proceed to the next level
            # you have to win until you collect 3
            else:
                bet = 1
        # lost previous game
        else:
            bet = 1

        # if player tries to bet more than they have, it automatically plays all-in
        if bet > self.budget:
            bet = self.budget
        # update current bet
        self.current_bet = bet
        # pay commission
        self.budget -= bet
        # TODO if we implement interactive version, player should be able to choose the bet
        return 1, bet


class Parlay31(Player):
    '''subclass from Player

    Simulate 31 Parlay from http://www.gamblinghelp.biz/wpblog/review-of-beat-the-casino-by-frank-barstow/

    Follow the sequence of 111224488.
    Each time you win the number, you parlay the number (bet everything you won from the previous game). If win consecutively before completing 111224488, you will start over.
    '''

    def __init__(self, name = 'guest'):
        '''Constructor for RandomBet

        Args:
            name: name for the player. Defalut is 'guest'
        '''
        Player.__init__(self,name)

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

        # 31 Parlay
        # won first time
        if self.last_win == 0 and self.win != 0 and self.consecutive_wins == 1:
            bet = self.prev_win
        # won second time
        elif self.last_win == 0 and self.win != 0 and self.consecutive_wins == 2:
            bet = 1
        # 0,1,2 since last consecutive wins
        elif self.last_consecutive_wins < 3:
            bet = 1
        # 3,4 since last consecutive wins
        elif self.last_consecutive_wins < 5:
            bet = 2
        # 5,6 since last consecutive wins
        elif self.last_consecutive_wins < 7:
            bet = 4
        # 7,8 since last consecutive wins
        elif self.last_consecutive_wins < 9:
            bet = 8
        else:
            bet = 1

        # if player tries to bet more than they have, it automatically plays all-in
        if bet > self.budget:
            bet = self.budget
        # update current bet
        self.current_bet = bet
        # pay commission
        self.budget -= bet
        # TODO if we implement interactive version, player should be able to choose the bet
        return 1, bet
