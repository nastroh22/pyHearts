import random 

class Player:
    def __init__(self,pid=0):
        self.id = pid
        # TODO: extend Hand Object
        self.hand = list()
        self.is_leader = False
    
    def select_card(self):
        pass

    def hand_is_all_hearts(self):
        for card in self.hand:
            if card.suit.symbol.lower() != 'h':
                return False
        return True
    
    def mask_out_hearts(self):
        mask=list()
        return
    
    def get_valid_cards(self,lead_suit, heart_is_broken=False):
        valid = list()
        if (self.is_leader and self.hand_is_all_hearts()):
            return [c for c in self.hand]
        
        if (self.is_leader and heart_is_broken):
            return [c for c in self.hand]
    
        if (self.is_leader and not heart_is_broken):
            for card in self.hand:
                if card.suit.symbol.lower() != 'h':
                    valid.append(card)
            return valid

        for card in self.hand:
            if card.suit.symbol.lower() == lead_suit.lower():
                valid.append(card)
        
        if not valid:
            valid = [c for c in self.hand]
        
        return valid


class RandomPlayer(Player):
    
    def select_card(self, lead_suit='h', heart_is_broken=False):
        options=self.get_valid_cards(lead_suit,heart_is_broken)
        card = random.choice(options)
        self.hand.remove(card)
        return card
