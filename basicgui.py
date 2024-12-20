import pygame as pyg
import os
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


CARDIR="card_pngs/"
RANKORDER=[]
DECK={ii:None for ii in range(1,53)}

def build_deck():
    suits={0:'clubs',1:'diamonds',2:'spades',3:'hearts'}
    for n in range(1,53):
        rank,suit = (n-1)%13,suits[(n-1)//13]
        pre=str(rank+2)
        token=pre

        if rank == 9:
            pre, token ='J','jack'
        if rank == 10:
            pre, token ='Q','queen'
        if rank == 11:
            pre,token ='K','king'
        if rank == 12:
            pre,token='A','ace'
        
        symbol=f"{pre}{suit[0].upper()}"
        file=f"{token}_of_{suit}.png"

        # print(f"{symbol}, {file}")

        DECK[n]=(symbol,file)

##TODO/NOTE: Wait this way is dumb because rank ordering will be hard to interpret if I'm using weird random lezicvogrpahical order

class GameState:
    def __init__(self,
        nplayers=3,
        player_hands={},
        player_scores=[],
        player_tallies=[],
    ):
        self.nplayers=nplayers
        self.random_seed=42
        self.player_scores={}
        self.player_tallies={}
        self.flop=[]
        self.cards_remaining=[]
        self.cards_burned=[]
        self.tricks_remaining=int(52/nplayers)
        self.players=[] #TODO: store player objects
        self.order=[ii for ii in range(nplayers)]
        self.leading_suit = 'H'
        self.suits={0:'clubs',1:'diamonds',2:'spades',3:'hearts'}
        self.order=[ii for ii in range(nplayers)]

        self.players = [Player(name=name,id=n) for (n,name) in enumerate(['Kaate','bob','alice','mary'])]
    
    
    def find_starting_player(self):
        for (id,hand) in self.player_hands.items():
            if 1 in hand:
                return id
            
    def determine_order(self,pointer=0,two_of_clubs=True):
        if (two_of_clubs):
            first=self.find_starting_player()
        else:
            first=pointer
        self.order=[(first+ii)%self.nplayers for ii in range(self.nplayers)]

        print(self.order)

    def determine_suit(self,card: int):
        return self.suits[(card-1)//13]

    def is_a_heart(self,card):
        return (self.determine_suit(card)==3)
    
    def is_queen_of_spades(self,card):
        return (card==37)

    def tally_trick(self,trick : list):
        tally=sum([self.is_a_heart(card) for card in trick])
        tally += 13*(sum([self.is_queen_of_spades(card) for card in trick]))
        self.cards_burned.extend(trick), print(f"\ntally: {tally}\n") # TODO: remove printing
        return tally

    import numpy as np
    def determine_winning_card(self,flop: dict, leading_suit: int = 0):
        wp,top_card=0,1
        for (k,v) in flop.items():
            if (self.determine_suit(v) == leading_suit):
                v+=1000
            if v > top_card: 
                top_card=v
                wp=k
        return wp
    
    def shuffle_deal_hands(self):
        k,deck=int(52//self.nplayers),list(DECK.keys())
        for _ in range(random.randint(1,15)): random.shuffle(deck)
        hands={ii: sorted(deck[ii*k:(ii+1)*k]) for ii in range(self.nplayers)}
        return hands

    def play_hand(self):
        hands=self.shuffle_deal_hands()
        self.player_hands=hands #NOTE: this is a bug, fix later
        for (n,player) in enumerate(self.players):
            player.set_hand(hands[n])
        # self.complete_passing step # NOTE: figure asynchronous execute potentially
        player_tallies={ii:0 for ii in range(self.nplayers)}
        self.determine_order(two_of_clubs=True)
        
        while self.tricks_remaining > 0:
            
            print("\n")
            self.players[0].display_hand()
            flop={}

            for player in self.order:
                p=self.players[player]
                ## TODO (DISPLAY FLOP)
                flop[p.id]=p.get_player_card()
                print(DECK[flop[p.id]][0])
                ## TODO display_flop(flop[p.id])
            
            ## TODO:
            wp=self.determine_winning_card(flop)
            player_tallies[wp]=self.tally_trick(list(flop.values()))
            print(wp)

            ## TODO: Move the order pointer to the leading player
            # self.leading_pointer=wp
            self.determine_order(pointer=int(wp),two_of_clubs=False)
            self.tricks_remaining-=1
        ## NOTE: Next complete scoring
                
class Player:
    def __init__(self,
        name='Kaaaate',
        score=0,
        id=0
    ):
        self.name=name
        self.score=score
        self.hand=[]
        self.id=id
        self.has_qos=False
        self.hand

    def set_hand(self,hand): 
        self.hand=list(hand)

    def get_player_card(self):
        return self.play()

    def play(self):
        card=random.sample(self.hand,1)[0]
        self.hand.remove(card)
        return card

    def display_hand(self):
        disp=[DECK[card][0] for card in self.hand]
        return disp


class Agent:
    """AI Player"""
    def __init__(self):
        self.difficulty=0
        return

if __name__ == "__main__":

    # codes=display_hand(myhand)
    # for c in codes:
    #     display_card(c)
    build_deck()
    Game=GameState(nplayers=4)
    Game.play_hand()

