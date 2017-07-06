from random import randint

class Player(object):
    ''' Player class represents each player of bacarrat

    Contains important player-specific information
    Later extend the AI, all information they need to compute the commands should be found
    inside of this class

    Attributes:
        name: sting for the name of the player
        round: the current round of the game of baccarat
        budget: the total money the player has
        win: total times the player wins
        net_gain: total money the player has won
        current_bet: player's current bet
        biggest_win: player's biggest win from one game
        biggest_loss: player's biggest loss from one game
        consecutive_wins: player's consective wins
        consecutive_loss: player's consecutive loss
        total_win_in_past_n: player's total win in recent n games
        total_loss_in_past_n: player's total loss in recent n games
        game_record: an array to store all game results
    '''
    # player is initialized with 1000 initial capital if not specified
    def __init__(self, name = 'guest'):
        '''Constructor for Player

        Args:
            name: name for the player. Defalut is 'guest'
        '''
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

    def bet(self):
        ''' decides bet price and guess for the next deal

        Every turn, state object will call this method as long as the player has money to play
        By default, player will bet on dealer and waits for the user input to determine the betting price.
        For AI player, this method should be overloaded

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
        # ask for the user input
        # this part is the brain of AI
        bet = 0
        while bet not in range(1,21):
            bet = raw_input("How much do you want to bet (1 - 20): ")
            try:
                bet = int(bet)
            except:
                bet = 0
        # if player tries to bet more than they have, it automatically plays all-in
        if bet > self.budget:
            bet = self.budget
        # update current bet
        self.current_bet = bet
        # pay commission
        self.budget -= bet
        # TODO if we implement interactive version, player should be able to choose the bet
        return 1, bet


    def retrieve(self, value):
        ''' Update the current budget by input value

        Args:
            value: the amount of money to be added to the player's budget
        '''
        self.budget += value


    def get_name(self):
        '''Return the name of the player

        The name of player is a key for the players dictionary in state obj

        Returns:
            name of the player in string
        '''
        return self.name

    def __countX(self, x, array):
        ''' Private method to count number of X in array

        Helper method for update function

        Args:
            x: element to count
            array: the array to iterate

        Returns:
            int value of how many x are in the array
        '''
        count = 0
        for i in array:
            if x == i:
                count += 1
        return count

    def update(self, value):
        '''update each turn

        update class attributes based on the result from the previous game

        Args:
            value: the rewards the player gets from the previous bet
            if value is 0, the player lost the last game
            if value is current bet, the player gets the commission back (tie)
            else player won
        '''
        # increment round
        self.round += 1
        # define the game result
        if value == 0:
            result = 'L'
        elif value == self.current_bet:
            result = 'T'
        else:
            result = 'W'
        # append the previous game result to the record
        self.game_record.append(result)

        # update the recent wins / loses from the record
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

    def show_stats(self):
        '''Print the stats of player on console
        '''
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
        print 'record: ' + str(self.game_record) 
        print ' '
