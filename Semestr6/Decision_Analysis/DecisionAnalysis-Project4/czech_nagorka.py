import numpy as np
from player import Player
import random

class Czech_Nagorka(Player):
    numberOfOpponentCards = 8
    opponentCards = set()
    possibleOpponentCards = set()
    stack = []
    checkRatio=0
    
    def putCard(self, declared_card):
        self.opponentCards=self.opponentCards - set(self.cards)
        self.possibleOpponentCards=self.possibleOpponentCards - set(self.cards)

        self.cards.sort(key=lambda x: x[0])

        # If we have last card, we can't cheat
        if len(self.cards) == 1 and declared_card is not None and self.cards[0][0] < declared_card[0]:
            self.stack=self.stack[:-3]
            return "draw"

        # Try to find valid cards (rank >= declared)
        valid_cards = [c for c in self.cards if declared_card is None or c[0] >= declared_card[0]]
        invalid_cards = [c for c in self.cards if declared_card is None or c[0] < declared_card[0]]

        # If we have any cards to play, we play thruthfully or cheat (and delcare it as lowest playable card)
        if valid_cards:
            # play the lowest card and declare it as lowest valid card
            if random.random() > self.cheatProbability and len(invalid_cards) > 0:
                card = invalid_cards[0]
                declaration = valid_cards[0]
                self.cheatProbability += 0.01
            # play the lowest playable card and truthfully declare
            else:
                card = valid_cards[0]
                declaration = card
        else:
            playable_cards = set([(number, color) for color in range(4) for number in range(9, 15) if number >= declared_card[0] and (number, color) != declared_card]) - self.opponentCards
            # No valid cards -> cheat 
            # 1. put your lowest card and declare it as card not yet declared
            card = self.cards[0]
            if len(playable_cards)>0:
                declaration = min(playable_cards, key = lambda x: x[0])
            else:
                cards_on_pile_sure = [i[0] for i in self.stack if i[1] and i[0][0]>= declared_card[0]]
                # 2. put your lowest card and declare it as card declared previously (opponent doesn't have it)
                if cards_on_pile_sure:
                    declared_rank = min(cards_on_pile_sure, key=lambda x: x[0])[0]
                    declared_suit = min(cards_on_pile_sure, key=lambda x: x[0])[1]
                # 3. if we didn't find any cards, declare randomly
                else:
                    declared_rank = declared_card[0]
                    declared_suit = random.choice([0, 1, 2, 3])
                declaration = (declared_rank, declared_suit)
        self.stack.append([card, True])
        return card, declaration
    
    
    def checkCard(self, opponent_declaration):
        self.opponentCards -= set(self.cards)
        self.possibleOpponentCards -= set(self.cards)
        self.stack.append([opponent_declaration, False])  
        self.numberOfOpponentCards -= 1

        # 1. If we have a card -> opponent cheats
        if opponent_declaration in self.cards: 
            return True

        # 2. If card was put on stack by us -> opponent cheats
        for card in self.stack:
            if card[0]==opponent_declaration and card[1]==True:
                return True
        
        # 3. If we don't have higher cards, we would need to draw
        # so checking opponent might help
        if opponent_declaration[0] > max(self.cards)[0]:
            return True
        
        # 4. If declared card is in opponent deck -> opponent says truth
        if opponent_declaration in self.opponentCards:  
            self.opponentCards.add(opponent_declaration) 
            self.possibleOpponentCards.discard(opponent_declaration)
            return False

        # 5. If opponent has more than 12 cards -> check if he doesn't 
        # play too aggresively
        if self.numberOfOpponentCards >= 12:
            return True

        # 6. If opponent plays high, suspicious card -> he might cheat 
        if opponent_declaration[0] == 14:
            return True

        # 7. If we know all cards -> don't check
        unknown_cards = 24 - len(self.cards) - len(self.opponentCards)
        if unknown_cards <= 0:
            return False

        # 8. If we don't know all cards -> check with some probability
        prob = (self.numberOfOpponentCards - len(self.opponentCards)) / unknown_cards

        if random.random() < prob + self.checkRatio:
            return True
        # 9. If we didn't find a reason to check -> don't check
        return False
    
    def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=True):
        if log: print("Feedback = " + self.name + " : checked this turn = " + str(checked) +
              "; I checked = " + str(iChecked) + "; I drew cards = " + 
                      str(iDrewCards) + "; revealed card = " + 
                      str(revealedCard) + "; number of taken cards = " + str(noTakenCards))
        if checked:
            if iDrewCards:
                self.opponentCards -= set(self.cards)
                self.possibleOpponentCards -= set(self.cards)
                self.checkRatio -= 0.01
                self.checkRatio=min(self.checkRatio, 0)
            else:
                for card in self.stack[-noTakenCards:]:
                    if card[1]:
                        self.opponentCards.add(card[0])
                        self.possibleOpponentCards.discard(card[0])
                self.checkRatio += 0.01
                self.checkRatio = max(self.checkRatio,0.1)
                self.numberOfOpponentCards += noTakenCards
            self.stack = self.stack[:-noTakenCards]
        else:
            if not iChecked and not iDrewCards and revealedCard is None and noTakenCards is not None:
                for card in self.stack[-noTakenCards:]:
                    if card[1]:
                        self.opponentCards.add(card[0])
                        self.possibleOpponentCards.discard(card[0])

                self.stack = self.stack[:-noTakenCards]
        
    def startGame(self, cards):
        self.cards = cards
        self.numberOfOpponentCards = 8
        self.stack = []
        self.opponentCards = set()
        self.possibleOpponentCards = set([(rank, suit) for suit in range(4) for rank in range(9, 15)])-set(self.cards)
        self.checkRatio = 0
        self.cheatProbability = 0.85