import numpy as np
from player import Player
import random

# Greedy player with card counting
class CardCounter(Player):
    n_opponent_cards = 8 # Number of all cards opponent has
    opponent_cards = set() # List of known cards
    potential_opponent_cards = set() # List of potentially known cards
    pile = [] # Pile where players stack their cards (card, whether it was put by me or opponent)
    
    def putCard(self, declared_card):
        self.opponent_cards.difference(set(self.cards))
        self.potential_opponent_cards.difference(set(self.cards))

        # 1. If I have one card left, play truthfully or draw (can't cheat)
        if len(self.cards) == 1 and declared_card is not None and self.cards[0][0] < declared_card[0]:
            self.pile = self.pile[:-3]
            return "draw"
         
        # 2. If there are no cards on the pile, put lowest and play truthfully
        if declared_card is None:
            card = min(self.cards)
            self.pile.append([card, True])
            return card, card

        # 3. If I don't have larger card, cheat and say a card that was never declared
        if max(self.cards)[0] < declared_card[0]:
            potential_cards = set(
                [(number, color) for color in range(4) for number in range(9, 15) if number >= declared_card[0] and (number, color) != declared_card]
            ).difference(set(self.cards))

            if not len(potential_cards):
                self.pile.append(min(self.cards, True))
                return min(self.cards), declared_card
            
            card = list(potential_cards)[random.randint(0, len(potential_cards) - 1)]
            self.pile.append([min(self.cards), True])
            return min(self.cards), card
        
        # 4. If I have a larger card, play truthfully
        cards_to_put = []
        for card in self.cards:
            if card[0] >= declared_card[0]:
                cards_to_put.append(card)
        
        card = min(cards_to_put)
        self.pile.append([card, True])

        return card, card
    
    
    def checkCard(self, opponent_declaration):
        self.pile.append([opponent_declaration, False])  # Potentially this card is in the pile
        self.n_opponent_cards -= 1

        self.opponent_cards.difference(set(self.cards))
        self.potential_opponent_cards.difference(set(self.cards))

        # 1. Check if I have the declared card in my cards
        if opponent_declaration in self.cards:
            return True
        
        # 2. Don't check if I suspect opponent has a card
        if opponent_declaration in self.opponent_cards:
            self.opponent_cards.discard(opponent_declaration)  
            self.potential_opponent_cards.discard(opponent_declaration)
            return False
        
        # 3. Check if I don't have better card
        if opponent_declaration[0] > max(self.cards)[0]:
            return True

        # 4. Check if card is relatively high - high risk of cheating
        if opponent_declaration[0] > 14:
            return True
        
        denominator = 24 - len(self.cards) - len(self.opponent_cards)
        # 5. Don't check if ...
        if denominator <= 0:
            return False

        prob = (self.n_opponent_cards - len(self.opponent_cards)) / denominator
        # 6. Check if number of unknown cards is high
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

class CardCounter2(Player):
    n_opponent_cards = 8
    opponent_cards = set()
    potential_opponent_cards = set()
    stack = []
    check_ratio=0
    
    def putCard(self, declared_card):
        self.opponent_cards=self.opponent_cards-set(self.cards)
        self.potential_opponent_cards=self.potential_opponent_cards-set(self.cards)

        self.cards.sort(key=lambda x: x[0])


        if len(self.cards) == 1 and declared_card is not None and self.cards[0][0] < declared_card[0]:
            self.stack=self.stack[:-3]
            return "draw"

        # Try to find valid cards (rank >= declared)
        valid_cards = [c for c in self.cards if declared_card is None or c[0] >= declared_card[0]]

        if valid_cards:
            card = valid_cards[0]# play the lowest valid card
            declaration = card        # truthfully declare
        else:
            playable_cards = set([(number, color) for color in range(4) for number in range(9, 15) if number >= declared_card[0] and (number, color) != declared_card])-self.opponent_cards
            # No valid cards -> cheat
            card = self.cards[-1]     # play the lowest card (to get rid of it)
            if len(playable_cards)>0:
                declaration = playable_cards[random.randint(0,len(playable_cards)-1)]
            else:
                if declared_card is not None:
                    # Declare a higher believable card
                    declared_rank = min(declared_card[0] + 1, 14)
                else:
                    declared_rank = random.randint(9, 14)

                declared_suit = random.choice([0, 1, 2, 3])
                declaration = (declared_rank, declared_suit)

        self.stack.append([card, True])
        # print(self.stack)
        return card, declaration
    
    
    def checkCard(self, opponent_declaration):
        self.opponent_cards-=set(self.cards)
        self.potential_opponent_cards-=set(self.cards)
        self.stack.append([opponent_declaration, False])  
        self.n_opponent_cards -= 1

        if opponent_declaration in self.cards: 
            return True

        for card in self.stack:
            if card[0]==opponent_declaration and card[1]==True:
                return True
        
        if opponent_declaration[0] > max(self.cards)[0]:
            return True
        
        if opponent_declaration in self.opponent_cards:  
            self.opponent_cards.add(opponent_declaration) 
            self.potential_opponent_cards.discard(opponent_declaration)
            return False
        
        denominator = 24 - len(self.cards) - len(self.opponent_cards)
        if denominator <= 0:
            return False

        prob = (self.n_opponent_cards - len(self.opponent_cards)) / denominator

        if random.random() < prob + self.check_ratio:
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
                self.check_ratio-=0.01
                self.check_ratio=min(self.check_ratio,0)
            else:
                for card in self.stack[-noTakenCards:]:
                    if card[1]:  # if that was our card we are sure about
                        self.opponent_cards.add(card[0])
                        self.potential_opponent_cards.discard(card[0])
                self.check_ratio+=0.01
                self.check_ratio=max(self.check_ratio,0.1)
                self.n_opponent_cards += noTakenCards
            self.stack = self.stack[:-noTakenCards]
        else:
            if not iChecked and not iDrewCards and revealedCard is None and noTakenCards is not None:  # opponent draws
                for card in self.stack[-noTakenCards:]:
                    if card[1]:  # if that was our card we are sure about
                        self.opponent_cards.add(card[0])
                        self.potential_opponent_cards.discard(card[0])

                self.stack = self.stack[:-noTakenCards]

        
    def startGame(self, cards):
        self.cards = cards
        self.n_opponent_cards = 8
        self.stack = []
        self.opponent_cards = set()
        self.potential_opponent_cards = set([(rank, suit) for suit in range(4) for rank in range(9, 15)])-set(self.cards)

# Greedy player with card counting with random cheating
class CardCounter3(Player):
    n_opponent_cards = 8 # Number of all cards opponent has
    opponent_cards = set() # List of known cards
    potential_opponent_cards = set() # List of potentially known cards
    pile = [] # Pile where players stack their cards (card, whether it was put by me or opponent)
    
    def putCard(self, declared_card):
        self.opponent_cards.difference(set(self.cards))
        self.potential_opponent_cards.difference(set(self.cards))

        # 1. If I have one card left, play truthfully or draw (can't cheat)
        if len(self.cards) == 1 and declared_card is not None and self.cards[0][0] < declared_card[0]:
            self.pile = self.pile[:-3]
            return "draw"
         
        # 2. If there are no cards on the pile, put lowest and play truthfully
        if declared_card is None:
            card = min(self.cards)
            self.pile.append([card, True])
            return card, card

        # 3. If I don't have larger card, cheat and say a card that was never declared
        if max(self.cards)[0] < declared_card[0]:
            potential_cards = set(
                [(number, color) for color in range(4) for number in range(9, 15) if number >= declared_card[0] and (number, color) != declared_card]
            ).difference(set(self.cards))

            if not len(potential_cards):
                self.pile.append(min(self.cards, True))
                return min(self.cards), declared_card
            
            card = list(potential_cards)[random.randint(0, len(potential_cards) - 1)]
            self.pile.append([min(self.cards), True])
            return min(self.cards), card
        
        # 4. If I have a larger card, play truthfully with some probability
        cards_to_put = []
        for card in self.cards:
            if card[0] >= declared_card[0]:
                cards_to_put.append(card)
        invalid_cards = list(set(self.cards).difference(set(cards_to_put)))

        if random.random() < 0.9 or len(invalid_cards) == 0:
            card = min(cards_to_put)
            declared_card = card
        # 5. Even if I have a lrager card, cheat with some probability 
        else:
            invalid_cards.sort(key = lambda x: x[0])

            card = min(invalid_cards, key = lambda x: x[0])
            declared_card = min(cards_to_put)
        self.pile.append([card, True])
        return card, declared_card
    
    
    def checkCard(self, opponent_declaration):
        self.pile.append([opponent_declaration, False])  # Potentially this card is in the pile
        self.n_opponent_cards -= 1

        self.opponent_cards.difference(set(self.cards))
        self.potential_opponent_cards.difference(set(self.cards))

        # 1. Check if I have the declared card in my cards
        if opponent_declaration in self.cards:
            return True
        
        # 2. Don't check if I suspect opponent has a card
        if opponent_declaration in self.opponent_cards:
            self.opponent_cards.discard(opponent_declaration)  
            self.potential_opponent_cards.discard(opponent_declaration)
            return False
        
        # 3. Check if I don't have better card
        if opponent_declaration[0] > max(self.cards)[0]:
            return True

        # 4. Check if card is relatively high - high risk of cheating
        if opponent_declaration[0] > 14:
            return True
        
        denominator = 24 - len(self.cards) - len(self.opponent_cards)
        # 5. Don't check if ...
        if denominator <= 0:
            return False

        prob = (self.n_opponent_cards - len(self.opponent_cards)) / denominator
        # 6. Check if number of unknown cards is high
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

class CardCounter4(Player):
    n_opponent_cards = 8
    opponent_cards = set()
    potential_opponent_cards = set()
    stack = []
    check_ratio=0
    
    def putCard(self, declared_card):
        self.opponent_cards=self.opponent_cards-set(self.cards)
        self.potential_opponent_cards=self.potential_opponent_cards-set(self.cards)

        self.cards.sort(key=lambda x: x[0])

        if len(self.cards) == 1 and declared_card is not None and self.cards[0][0] < declared_card[0]:
            self.stack=self.stack[:-3]
            return "draw"

        # Try to find valid cards (rank >= declared)
        valid_cards = [c for c in self.cards if declared_card is None or c[0] >= declared_card[0]]
        invalid_cards = [c for c in self.cards if declared_card is None or c[0] < declared_card[0]]

        if valid_cards:
            if random.random() > self.cheat_probability and len(invalid_cards) > 0:
                card = invalid_cards[0] # play the lowest invalid card
                declaration = valid_cards[0] # declare it as lowest valid card
                self.cheat_probability += 0.01
            else:
                card = valid_cards[0] # play the lowest valid card
                declaration = card        # truthfully declare
        else:
            playable_cards = set([(number, color) for color in range(4) for number in range(9, 15) if number >= declared_card[0] and (number, color) != declared_card])-self.opponent_cards
            # No valid cards -> cheat
            card = self.cards[0]     # play the lowest card (to get rid of it)
            if len(playable_cards)>0:
                declaration = min(playable_cards, key = lambda x: x[0])
            else:
                cards_on_pile_sure = [i[0] for i in self.stack if i[1] and i[0][0]>= declared_card[0]]
                if cards_on_pile_sure:
                    declared_rank = min(cards_on_pile_sure, key=lambda x: x[0])[0]
                    declared_suit = min(cards_on_pile_sure, key=lambda x: x[0])[1]
                else:
                    declared_rank = declared_card[0]
                    declared_suit = random.choice([0, 1, 2, 3])
                declaration = (declared_rank, declared_suit)

        self.stack.append([card, True])
        return card, declaration
    
    
    def checkCard(self, opponent_declaration):
        self.opponent_cards-=set(self.cards)
        self.potential_opponent_cards-=set(self.cards)
        self.stack.append([opponent_declaration, False])  
        self.n_opponent_cards -= 1

        if opponent_declaration in self.cards: 
            return True

        for card in self.stack:
            if card[0]==opponent_declaration and card[1]==True:
                return True
        
        if opponent_declaration[0] > max(self.cards)[0]:
            return True
        
        if opponent_declaration in self.opponent_cards:  
            self.opponent_cards.add(opponent_declaration) 
            self.potential_opponent_cards.discard(opponent_declaration)
            return False

        if self.n_opponent_cards >= 12:
            return True

        if opponent_declaration[0] == 14:
            return True

        denominator = 24 - len(self.cards) - len(self.opponent_cards)
        if denominator <= 0:
            return False

        prob = (self.n_opponent_cards - len(self.opponent_cards)) / denominator

        if random.random() < prob + self.check_ratio:
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
                self.check_ratio-=0.01
                self.check_ratio=min(self.check_ratio,0)
            else:
                for card in self.stack[-noTakenCards:]:
                    if card[1]:  # if that was our card we are sure about
                        self.opponent_cards.add(card[0])
                        self.potential_opponent_cards.discard(card[0])
                self.check_ratio+=0.01
                self.check_ratio=max(self.check_ratio,0.1)
                self.n_opponent_cards += noTakenCards
            self.stack = self.stack[:-noTakenCards]
        else:
            if not iChecked and not iDrewCards and revealedCard is None and noTakenCards is not None:  # opponent draws
                for card in self.stack[-noTakenCards:]:
                    if card[1]:  # if that was our card we are sure about
                        self.opponent_cards.add(card[0])
                        self.potential_opponent_cards.discard(card[0])

                self.stack = self.stack[:-noTakenCards]

        
    def startGame(self, cards):
        self.cards = cards
        self.n_opponent_cards = 8
        self.stack = []
        self.opponent_cards = set()
        self.potential_opponent_cards = set([(rank, suit) for suit in range(4) for rank in range(9, 15)])-set(self.cards)
        self.check_ratio=0
        self.cheat_probability = 0.85