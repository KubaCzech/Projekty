import numpy as np
from player import Player

class Wiktor(Player):
    def __init__(self,
                 name,
                 opponent_cheat_p = 0.99,
                 ratio_to_cheat = 0.5):
        self.cards = []

        self.pile_correct = []
        self.pile_declared = []
        self.num_of_opponent_cards = 8
        self.num_of_opponent_bluffs = 0
        self.num_of_opponent_correct = 0
        self.opponent_cards = []
        self.known_cards = set()
        self.factorials = [1]
        self.cards_not_in_game = []
        self.add_to_cards_not_in_game = True
        self.opponent_cheat_p = opponent_cheat_p
        self.ratio_to_cheat = ratio_to_cheat
        self.first_card_placed = False
        self.first_check = False
        self.probabilities = [[1 / 2 for x in range(4)] for y in range(0, 15)]

        for i in range(1, 25):
            self.factorials.append(self.factorials[-1] * i)

        super().__init__(name)
        
    
    def putCard(self, declared_card):
        for card in self.cards:
            self.known_cards.add(card)

        self.cards = list(sorted(self.cards))

        if declared_card == None:
            self.pile_correct.append(self.cards[0])
            self.pile_declared.append(self.cards[0])
            return self.cards[0], self.cards[0]

        if self.num_of_opponent_cards / len(self.cards) < self.ratio_to_cheat:
            return self.put_card_cheat(declared_card)

        for card in self.cards:
            if card[0] >= declared_card[0]:
                self.pile_correct.append(card)
                self.pile_declared.append(card)
                return card, card

        if declared_card[1] == 3:
            self.pile_correct.append(self.cards[0])
            self.pile_declared.append((declared_card[0], 1))
            return self.cards[0], (declared_card[0], 1)
        else:
            self.pile_correct.append(self.cards[0])
            self.pile_declared.append((declared_card[0], 3))
            return self.cards[0], (declared_card[0], 3)

    def put_card_cheat(self, declared_card):
        self.cards_not_in_game = list(sorted(self.cards_not_in_game))
        for card in self.cards_not_in_game:
            if card[0] >= declared_card[0]:
                self.pile_correct.append(self.cards[0])
                self.pile_declared.append(card)
                return self.cards[0], card

        for card in self.cards:
            if card[0] >= declared_card[0]:
                self.pile_correct.append(card)
                self.pile_declared.append(card)
                return self.cards[0], card
        
        self.pile_correct.append(self.cards[0])
        self.pile_declared.append((declared_card[0], (declared_card[1] + 1) % 4))
        return self.cards[0], (declared_card[0], (declared_card[1] + 1) % 4)

    def get_probability_of_correct(self, opponent_declaration):
        probability = self.probabilities[opponent_declaration[0]][opponent_declaration[1]]

        return probability

    def update_probabilities(self, x, y, new, sum_delta=0):
        to_dirtribute = self.probabilities[x][y] - new + sum_delta
        self.probabilities[x][y] = new

        non_zero = 0
        for i in range(9, 15):
            for j in range(0, 4):
                if (i != x or j != y) and self.probabilities[i][j] > 0:
                    non_zero += 1

        probabilities_sum = 0
        for i in range(9, 15):
            for j in range(0, 4):
                if (i != x or j != y) and self.probabilities[i][j] > 0:
                    self.probabilities[i][j] += to_dirtribute / non_zero

                probabilities_sum += self.probabilities[i][j]


    def checkCard(self, opponent_declaration):
        self.pile_correct.append(None)
        self.pile_declared.append(opponent_declaration)

        if not self.first_card_placed:
            for x in range(9, opponent_declaration[0]):
                for y in range(4):
                    if (x, y) > opponent_declaration:
                        break
                    self.update_probabilities(x, y, 0)
                    self.cards_not_in_game.append((x, y))

            self.first_card_placed = True

        probability_of_correct = self.get_probability_of_correct(opponent_declaration)
        self.num_of_opponent_cards -= 1
        self.update_probabilities(opponent_declaration[0], opponent_declaration[1], 1 - self.opponent_cheat_p, -1)

        if opponent_declaration in self.cards:
            return True
        if opponent_declaration in self.pile_correct:
            return True
        if len(self.cards) == 1 and opponent_declaration[0] > self.cards[0][0]:
            return True
        if opponent_declaration in self.pile_declared:
            return False

        return True if probability_of_correct < 0.5 else False

    def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=True):
        if noTakenCards is None:
            return

        if revealedCard is None:
            revealedCard = self.pile_correct[-1]

        self.known_cards.add(revealedCard)
        if not iChecked:
            self.last_checked = checked
            self.i_drew_cards = iDrewCards
            self.revealed_card = revealedCard

            self.num_takien_cards = noTakenCards
            if not iDrewCards:
                self.num_of_opponent_cards += noTakenCards
                for x in range(noTakenCards):
                    if self.pile_correct[-1] is not None:
                        self.opponent_cards.append(self.pile_correct[-1])
                        self.update_probabilities(self.pile_correct[-1][0], self.pile_correct[-1][1], 1, 1)
                    elif x == 0:
                        self.update_probabilities(revealedCard[0], revealedCard[1], 1, 1)
                    else:
                        self.update_probabilities(0, 0, 0.5, 1)
                    self.pile_correct.pop()
                    self.pile_declared.pop()
            else:
                if noTakenCards >= 2 and self.cards[-2] != self.pile_declared[-2]:
                    self.num_of_opponent_bluffs += 1
                if noTakenCards >= 2 and self.cards[-2] == self.pile_declared[-2]:
                    self.num_of_opponent_correct += 1
                for x in range(noTakenCards):
                    self.pile_correct.pop()
                    self.pile_declared.pop()
                    self.update_probabilities(self.cards[-x][0], self.cards[-x][1], 0)
        else:
            if not iDrewCards:
                self.num_of_opponent_cards += noTakenCards
                for x in range(noTakenCards):
                    if self.pile_correct[-1] is not None:
                        self.opponent_cards.append(self.pile_correct[-1])
                        self.update_probabilities(self.pile_correct[-1][0], self.pile_correct[-1][1], 1, 1)
                    elif x == 0:
                        self.update_probabilities(revealedCard[0], revealedCard[1], 1, 1)
                    else:
                        self.update_probabilities(0, 0, 0.5, 1)
                    self.pile_correct.pop()
                    self.pile_declared.pop()
            else:
                if self.cards[-1] != self.pile_declared[-1]:
                    self.num_of_opponent_bluffs += 1
                else:
                    self.num_of_opponent_correct += 1
                    
                if noTakenCards >= 3 and self.cards[-3] != self.pile_declared[-3]:
                    self.num_of_opponent_bluffs += 1
                elif noTakenCards >= 3 and self.cards[-3] == self.pile_declared[-3]:
                    self.num_of_opponent_correct += 1
                for x in range(noTakenCards):
                    self.pile_correct.pop()
                    self.pile_declared.pop()
                    self.update_probabilities(self.cards[-x][0], self.cards[-x][1], 0)