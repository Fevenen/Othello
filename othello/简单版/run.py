from othellolib import game, create_player, move_input, move_random


def main():
    player1 = create_player('玩家 1', move_input)
    player2 = create_player('玩家 2', move_random)
    game(player1, player2)


if __name__ == "__main__":
    main()
