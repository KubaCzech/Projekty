import numpy as np
import random
from player import Player

class AggresivePlayer(Player):
    
    def putCard(self, declared_card):
        # Sort cards in descending order of rank
        self.cards.sort(reverse=True, key=lambda x: x[0])

        if len(self.cards) == 1 and declared_card is not None and self.cards[0][0] < declared_card[0]:
            return "draw"

        # Try to find valid cards (rank >= declared)
        valid_cards = [c for c in self.cards if declared_card is None or c[0] >= declared_card[0]]

        if valid_cards:
            card = valid_cards[0]     # play the highest valid card
            declaration = card        # truthfully declare
        else:
            # No valid cards -> cheat
            card = self.cards[-1]     # play the lowest card (to get rid of it)
            if declared_card is not None:
                # Declare a higher believable card
                declared_rank = min(declared_card[0] + 1, 14)
            else:
                declared_rank = random.randint(9, 14)

            declared_suit = random.choice([0, 1, 2, 3])
            declaration = (declared_rank, declared_suit)


        return card, declaration

    def checkCard(self, opponent_declaration):
        if opponent_declaration in self.cards:
            return True
        if opponent_declaration[0]>max(self.cards)[0]:
            return True
        if random.random()>0.7:
            return True
        return False