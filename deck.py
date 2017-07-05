'''
Class for playing cards
'''
import numpy as np
class Card():
    suite = ''
    number = 0
    # when instanciate, Card object will get suite and number
    # throw an exception when suite or number is invalid
    def __init__(self, s, n):
        if s != 'H' and s != 'S' and s != 'C' and s != 'D':
            raise Exception('invalid suite')
        if not (0 < n and n < 14):
            raise Exception('invalid number')

        self.suite = s
        self.number = n

    # overload print functionp
    def __str__(self):
        return self.suite + ' ' + str(self.number)


class Deck():
    cards = []
    def __init__(self):
        # initialize by creating 13 x 4 card objects
        for s in ['H', 'S', 'C', 'D']:
            for n in range(1,14):
                self.cards.append(Card(s,n))
        self.cards = np.array(self.cards)

    # overload str for the comvenience
    def print_deck(self):
        print [str(c) for c in self.cards]

    # inplace shuffle using numpy methods
    def shuffle(self):
        np.random.shuffle(self.cards)

    # draw one card from the deck
    # throw an exception if there is no cards left
    def draw(self):
        if len(self.cards) == 0:
            raise Exception('no cards left')
        else:
            pop = self.cards.item(0)
            self.cards = np.delete(self.cards, 0)
            return pop


if __name__ == '__main__':
    d = Deck()
    d.print_deck()
    print d.draw()
    d.print_deck()
