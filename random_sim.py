from engine import HeartsGame

rounds = 3
game=HeartsGame()

if __name__ == "__main__":
    print("Welcome to Hearts!")
    game = HeartsGame()
    for round in range(rounds):
        game.play_hand()
