import numpy as np
import random
from player import Player

class LowCardThrower(Player):
    # getting rid of low cards as quickly as possible
    def putCard(self, declared_card):
        if declared_card is None:
            self.cards.sort(key = lambda x: x[0])
            return self.cards[0], self.cards[0]
        invalid_cards = [c for c in self.cards if c[0] < declared_card[0]]
        invalid_cards.sort(key = lambda x: x[0])

        valid_cards = [c for c in self.cards if c[0] >= declared_card[0]]
        valid_cards.sort(key = lambda x: x[0])
        if invalid_cards:
            declared = (declared_card[0], random.choice(range(4)))
            return invalid_cards[0], declared
        else:
            return valid_cards[0], valid_cards[0]

    def checkCard(self, opponent_declaration):
        if opponent_declaration in self.cards:
            return True
        if opponent_declaration[0] == 14:
            return True
        if opponent_declaration[0]>max(self.cards)[0]:
            return True
        if random.random()>0.8:
            return True
        return False