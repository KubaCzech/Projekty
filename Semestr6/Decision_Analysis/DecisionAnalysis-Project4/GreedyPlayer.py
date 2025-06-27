import numpy as np
import random
from player import Player

class GreedyPlayer(Player):
    # Greedy Player
    def putCard(self, declared_card):
        self.cards.sort(key = lambda x: x[0], reverse=True)  # High to low
        card = self.cards[0]
        declared = card

        # Bluff if declared_card exists and hand is bad
        if declared_card is not None and card[0] < declared_card[0] and len(self.cards) > 1:
            # Try bluffing to higher card if possible
            declared_options = [c for c in self.cards if c[0] >= declared_card[0]]
            if declared_options:
                declared = random.choice(declared_options)
            else:
                declared = (declared_card[0], random.choice(range(4)))
        # You cant cheat in last round
        elif (len(self.cards) == 1) and declared_card is not None:
            if self.cards[0][0] >= declared_card[0]:
                card = self.cards[0]
            else:
                return "draw"

        return card, declared

    def checkCard(self, opponent_declaration):
        # Check if opponent declares highest card (suspicious)
        if opponent_declaration in self.cards:
            return True
        if opponent_declaration[0] == 14:
            return True
        if opponent_declaration[0]>max(self.cards)[0]:
            return True
        if random.random()>0.8:
            return True
        return False