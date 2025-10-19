from engine.deck import *
from engine.deck import Deck
from engine.player import RandomPlayer
# import gym
import numpy as np


class HeartsGame:

    def __init__(self):
        self.num_rounds = 3
        self.num_players = 4
        self.player_scores = {ii:0 for ii in range(self.num_players)}
        self.player_tallies = {ii:0 for ii in range(self.num_players)}
        self.player_hands = {ii:list() for ii in range(self.num_players)}
        self.players = [RandomPlayer(ii) for ii in range(self.num_players)]
        self.leader = 0
        self.deck = Deck(
            self.num_players
        )
        self.hand_id = 0
        
        self.queen_penalty = 13
        self.heart_penalty = 1
        # self.tricks_per_hand = self.deck.trick_size

    def evaluate_card(self,card):
        x = card.rank_value
        x += 12 if self.leading_suit == card.suit.symbol else 0
        x += 12 if card.is_trump else 0
        print(f"DEBUG Eval Card: {card.symbol} {x}")
        return x

    def adjudicate(self):
        winner,max_rank=0,-1
        for key,card in self.trick.items():
            rank=self.evaluate_card(card)
            if rank > max_rank:
                winner = key
                max_rank = rank
        tally=np.sum(
            [int(self.heart_penalty*card.is_heart()) + int(self.queen_penalty*card.is_queen_of_spades()) for card in self.trick.values()]
        )
        self.player_tallies[winner] += tally
        print(f"Winner is: {winner} played {self.trick[winner].symbol}. Tally: {tally}")
        self.leader = winner
        for player in self.players:
            player.is_leader = True if player.id == winner else False
        return (winner,tally)

    def collect_trick(self):
        
        self.trick={pid:None for pid in range(self.num_players)}
        self.leading_suit = 's' # arbitrary 
        order=[
            (self.leader + ii)%self.num_players for ii in range(self.num_players)
        ]
        print(f"\nTrick {self.trick_count} Order Is: {order}")
        self.players[order[0]].is_leader = True
        
        for (n,pid) in enumerate(order):
            self.trick[pid] = self.players[pid].select_card(
                lead_suit = self.leading_suit,
                heart_is_broken = self.heart_is_broken
            )

            if n == 0:
                self.leading_suit = self.trick[pid].suit.symbol

            if self.trick[pid].suit.symbol == 'h':
                self.heart_is_broken = True
        
        ## debug:
        print(f"New leader is {order[0]}. Lead Suit is {self.leading_suit}")
            
        

    def query_player():
        pass


    def summarize_round(self):
        print("\nHand Summary:\n"+"\n".join(
            [f"Player {ii} Score: {score}" for ii,score in self.player_scores.items()]
        ))


    def play_hand(self):

        print(f"\nNew Hand {self.hand_id}"+"\n"+"-"*15)
        ## reset hand (TODO: add passing phase)
        for pid, hand in self.deck.deal().items():
            if '2d' in [card.symbol.lower() for card in hand]:
                self.leader = pid
                self.players[pid].is_leader = True
                print(f"First Leader: {self.leader}")
            self.players[pid].hand = hand
        self.heart_is_broken = False
        self.trick_count = 1
        
        for i in range(self.deck.trick_size):
            # print("Length player hands: ", [len(self.players[pid].hand) for pid in range(self.num_players)])
            self.collect_trick()
            winner,tally=self.adjudicate()
            self.trick_count += 1

        moonshot, moonid = False, 0
        for i, tally in self.player_tallies.items():
            # TODO make dynamic for 3 player
            if tally != 26: 
                continue
            moonshot = True
            moonid = i
        
        if moonshot:
            for i in range(self.num_players):
                if i == moonid:
                    continue
                self.player_scores[i] += 26
        else:
            for i in range(self.num_players):
                self.player_scores[i] += self.player_tallies[i]
                self.player_tallies[i] = 0
        
        self.summarize_round()
        print("")
        self.hand_id += 1
        return


if __name__ == "__main__":
    print("Welcome to Hearts!")
    game = HeartsGame()
    for round in range(2):
        game.play_hand()
