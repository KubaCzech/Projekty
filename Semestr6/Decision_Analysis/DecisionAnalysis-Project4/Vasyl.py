import numpy as np
from player import Player
import random

class Vasia(Player):
    n_opponent_cards = 8
    opponent_cards = set()
    potential_opponent_cards = set()
    pile = []
    
    def putCard(self, declared_card):
        self.opponent_cards.difference(set(self.cards))
        self.potential_opponent_cards.difference(set(self.cards))

        if len(self.cards) == 1 and declared_card is not None and self.cards[0][0] < declared_card[0]:
            self.pile = self.pile[:-3]
            return "draw"
         
        if declared_card is None:  # no cards in the pile put the lowest truthfully
            card = min(self.cards)
            self.pile.append([card, True])
            return card, card

        if max(self.cards)[0] < declared_card[0]:  # if I don't have larger card
            ### Say a card that was never declared
            potential_cards = set(
                [(number, color) for color in range(4) for number in range(9, 15) if number >= declared_card[0] and (number, color) != declared_card]
            ).difference(set(self.cards))

            if not len(potential_cards):
                self.pile.append(min(self.cards, True))
                return min(self.cards), declared_card
            
            card = list(potential_cards)[random.randint(0, len(potential_cards) - 1)]
            self.pile.append([min(self.cards), True])
            return min(self.cards), card
        
        cards_to_put = []
        for card in self.cards:
            if card[0] >= declared_card[0]:
                cards_to_put.append(card)
        
        card = min(cards_to_put)
        self.pile.append([card, True])

        return card, card
    
    
    def checkCard(self, opponent_declaration):
        self.opponent_cards.difference(set(self.cards))
        self.potential_opponent_cards.difference(set(self.cards))

        self.pile.append([opponent_declaration, False])  # potentially this card is in the pile
        self.n_opponent_cards -= 1

        if opponent_declaration in self.cards:  # if I have the declared card
            return True
        
        if opponent_declaration[0] > max(self.cards)[0]:
            return True
        
        if opponent_declaration in self.opponent_cards:  # if I know opponent has the card
            self.opponent_cards.add(opponent_declaration)  # now we don't know if they have it
            self.potential_opponent_cards.discard(opponent_declaration)
            return False
        
        denominator = 24 - len(self.cards) - len(self.opponent_cards)
        if denominator <= 0:
            return False

        prob = (self.n_opponent_cards - len(self.opponent_cards)) / denominator

        if random.random() < prob:
            return True

        return False

    
    def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=True):
        if log: print("Feedback = " + self.name + " : checked this turn = " + str(checked) +
              "; I checked = " + str(iChecked) + "; I drew cards = " + 
                      str(iDrewCards) + "; revealed card = " + 
                      str(revealedCard) + "; number of taken cards = " + str(noTakenCards))
                 
        if checked:  # someone checked the cards
            if iDrewCards:  # I failed
                self.opponent_cards.difference(set(self.cards))
                self.potential_opponent_cards.difference(set(self.cards))
            else:  # opponent failed
                self.n_opponent_cards += noTakenCards

                for card in self.pile[-noTakenCards:]:
                    if card[1]:  # if that was our card we are sure about
                        self.opponent_cards.add(card[0])
                        self.potential_opponent_cards.discard(card[0])

            self.pile = self.pile[:-noTakenCards]
        else:
            if not iChecked and not iDrewCards and revealedCard is None and noTakenCards is not None:  # opponent draws
                for card in self.pile[-noTakenCards:]:
                    if card[1]:  # if that was our card we are sure about
                        self.opponent_cards.add(card[0])
                        self.potential_opponent_cards.discard(card[0])

                self.pile = self.pile[:-noTakenCards]

        
    def startGame(self, cards):
        self.cards = cards
        self.n_opponent_cards = 8
        self.pile = []
        self.opponent_cards = set()
        self.potential_opponent_cards = set(
            [(number, color) for color in range(4) for number in range(9, 15)]
        ).difference(set(cards))