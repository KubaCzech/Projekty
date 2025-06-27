import numpy as np
import random
from player import Player

class NaiveHistoryTracker(Player):
    def __init__(self, name):
        super().__init__(name)
        self.history = []  # store tuples of (my_move, declared_card, true_card, opponent_checked, result)
        self.last_opponent_declared = None

    def putCard(self, declared_card):
        self.cards.sort(key=lambda x: x[0])  # sort by card number (low to high)
        
        # First turn or after a draw — no restriction, play lowest card truthfully
        if declared_card is None:
            card = self.cards[0]
            self.history.append(("play", card, card, None, None))
            return card, card
        
        # Try to play a card equal or higher
        legal_cards = [card for card in self.cards if card[0] >= declared_card[0]]
        if legal_cards:
            card = legal_cards[0]
            self.history.append(("play", declared_card, card, None, None))
            return card, card  # play legally
        else:
            # Cheating scenario — play lowest card but lie
            card = self.cards[0]
            self.history.append(("cheat", declared_card, card, None, None))
            return card, declared_card  # bluff

    def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=True):
        super().getCheckFeedback(checked, iChecked, iDrewCards, revealedCard, noTakenCards, log)
        
        # Record result of previous round
        if checked:
            if iChecked:
                result = "success" if not iDrewCards else "fail"
                self.history.append(("check", self.last_opponent_declared, revealedCard, iChecked, result))

    def checkCard(self, opponent_declaration):
        if opponent_declaration in self.cards:
            return True
        if opponent_declaration[0]>max(self.cards)[0]:
            return True
        if opponent_declaration[0] >= 13:
            return True
        if len(self.cards) < 4:
            return True
        if random.random()>0.7:
            return True
        return False