import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import random
import numpy as np

CARD_DISPLAY_PATH = str(Path(__file__).parent / "card_pngs")

RANK_MAPS={
    "ACE_HIGH": {
        "2": 0,
        "3": 1,
        "4": 2,
        "5": 3,
        "6": 4,
        "7": 5,
        "8": 6,
        "9": 7,
        "10": 8,
        "J": 9,
        "Q": 10,
        "K": 11,
        "A": 12
    }
}

@dataclass
class Suit:
    name: str
    symbol: str
    color: str
    order: int

@dataclass
class Card:
    rank: str
    suit: Suit

class Suits(Enum):
    CLUBS = Suit(name="Clubs", symbol="C", color="black",order=0)
    DIAMONDS = Suit(name="Diamonds", symbol="D", color="red", order=1)
    HEARTS = Suit(name="Hearts", symbol="H", color="red",order=2)
    SPADES = Suit(name="Spades", symbol="S", color="black",order=3)


class Card:
    def __init__(self, rank, suit):
        self.rank_symbol = rank.upper()
        self.rank_value = RANK_MAPS["ACE_HIGH"][rank.upper()]
        self.is_trump = False
        self.suit = suit
        # self.value = self.build_int_mapper()[rank]
        self.is_leading = False
        self.is_played = False
        self.filename = os.path.join(
            CARD_DISPLAY_PATH,
            f"{rank}_of_{suit.name.lower()}.png"
        )
        self.symbol=f"{self.rank_symbol}{self.suit.symbol}"

    
    def is_heart(self):
        return self.suit.symbol.lower() == 'h'
    
    def is_queen_of_spades(self):
        return (self.symbol.lower() == 'qs')

    def assign_integer_key(self):
        return self.suit.order * 13 + self.rank_value
    
    def display(self):
        # print(f"{self.rank_symbol}{self.suit.symbol}")
        return self.filename

class Hand():
    def __init__(self, cards=list()):
        self.cards = cards


class Deck:
    def __init__(self, n_players=4):
        self.build_deck()
        self.players = n_players
        self._playable = list(range(52))
        if n_players not in [3,4]:
            raise ValueError("Only 3 or 4 players supported")
        if n_players == 3:
            self.trick_size = 17
            self._playable.remove(0)
        if n_players == 4:
            self.trick_size = 13

    def build_deck(self):
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self._cards = {ii: None for ii in range(52)}
        for suit in Suits:
            for rank in ranks:
                temp = Card(rank, suit.value)
                key = temp.assign_integer_key()
                self._cards[key] = Card(rank, suit.value)
    
    def shuffle(self):
        self._playable = list(range(52))
        random.shuffle(self._playable)
    
    def deal(self):
        self.shuffle()
        hands = {ii: None for ii in range(self.players)}
        # deal chunks
        for player in range(self.players):
            hands[player] = [
                self._cards[ii] for ii in\
                    self._playable[player*self.trick_size:player*self.trick_size + self.trick_size]
            ]
        return hands
        

# class Trick():

# Test Dealer Logic
if __name__ == "__main__":
    n_players=4
    deck = Deck(
        n_players
    )
    hands=deck.deal()
    for i in range(deck.size):
        for j in range(n_players):
            print(f"Player {j+1}: {hands[j][i].symbol}")
            fname=hands[j][i].display()
            # print(fname)
        print("\nNext Trick")

    


