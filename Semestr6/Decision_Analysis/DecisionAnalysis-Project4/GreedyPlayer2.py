import numpy as np
import random
from player import Player

class GreedyPlayer2(Player):
    
    def putCard(self, declared_card):
        # Sort cards in descending order of rank
        self.cards.sort(reverse=True, key=lambda x: x[0])

        if len(self.cards) == 1 and declared_card is not None and self.cards[0][0] < declared_card[0]:
            return "draw"

        # Try to find valid cards (rank >= declared)
        valid_cards = [c for c in self.cards if declared_card is None or c[0] >= declared_card[0]]
        
        if declared_card is None:
            if len(self.cards)==1:
                return self.cards[-1], self.cards[-1]
            else:
                return self.cards[-1], self.cards[-2]

        if valid_cards:
            card = valid_cards[-1]     # play the lowest valid card
            declaration = card        # truthfully declare
        else:
            # No valid cards -> cheat
            card = self.cards[-1]     # play the lowest card (to get rid of it)
            if declared_card is not None:
                # Declare rank equal or a bit higher
                declared_rank = min(declared_card[0], 14)

            declared_suit = random.choice([0, 1, 2, 3])
            declaration = (declared_rank, declared_suit)
        return card, declaration

    def checkCard(self, opponent_declaration):
        if opponent_declaration in self.cards:
            return True
        if opponent_declaration[0]>max(self.cards)[0]:
            return True
        if opponent_declaration[0] == 14:
            return True
        if random.random()>0.7:
            return True
        return False