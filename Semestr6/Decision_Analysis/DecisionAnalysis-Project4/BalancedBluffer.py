import random
from player import Player

class BalancedBluffer(Player):
    def startGame(self, cards):
        self.cards = cards
        self.opponent_cards = set()
        self.stack = []
        self.n_opponent_cards = 8
        self.check_aggression = 0.02

    def putCard(self, declared_card):
        self.opponent_cards -= set(self.cards)
        self.cards.sort(key=lambda x: x[0])  # sort ascending

        valid_cards = [card for card in self.cards if declared_card is None or card[0] >= declared_card[0]]

        if valid_cards:
            card = valid_cards[0]
            declaration = card
        else:
            card = self.cards[0]  # use lowest card
            # Try to pick a believable fake declaration
            candidates = [(r, s) for r in range(9, 15) for s in range(4) 
                          if (r, s) not in self.cards and (declared_card is None or r >= declared_card[0])]
            if not candidates:
                # fallback fake
                declaration = (random.randint(9, 14), random.randint(0, 3))
            else:
                declaration = random.choice(candidates)

        self.stack.append((card, True))
        return card, declaration

    def checkCard(self, opponent_declaration):
        self.opponent_cards -= set(self.cards)
        self.stack.append((opponent_declaration, False))
        self.n_opponent_cards -= 1

        # Cheat detection heuristics
        if opponent_declaration in self.cards:
            return True

        for card, is_self in self.stack:
            if card == opponent_declaration and is_self:
                return True

        if opponent_declaration[0] > max(self.cards, default=(0, 0))[0]:
            return True

        if opponent_declaration in self.opponent_cards:
            return False

        known = len(self.opponent_cards)
        unknown = 24 - len(self.cards) - known
        if unknown <= 0:
            return False

        est_prob = (self.n_opponent_cards - known) / unknown

        return random.random() < est_prob + self.check_aggression

    def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=True):
        if log:
            print(f"Feedback ({self.name}) - checked: {checked}, iChecked: {iChecked}, "
                  f"drew: {iDrewCards}, revealed: {revealedCard}, taken: {noTakenCards}")

        if checked:
            if iDrewCards:
                self.check_aggression = max(0, self.check_aggression - 0.01)
            else:
                for card, is_self in self.stack[-noTakenCards:]:
                    if is_self:
                        self.opponent_cards.add(card)
                self.check_aggression = min(0.2, self.check_aggression + 0.01)
                self.n_opponent_cards += noTakenCards

            self.stack = self.stack[:-noTakenCards]
        elif not iChecked and not iDrewCards and revealedCard is None and noTakenCards is not None:
            for card, is_self in self.stack[-noTakenCards:]:
                if is_self:
                    self.opponent_cards.add(card)
            self.stack = self.stack[:-noTakenCards]