# import statements
from GameManager import *  # used for game logic
from Player import *  # used for player
from os import system  # used for clearing console
import GUI

# global vars
GAME_BOARD = [
    ['\u25FC', '\u25FB', '\u25FC', '\u25FB', '\u25FC', '\u25FB', '\u25FC', '\u25FB'],
    ['\u25FB', '\u25FC', '\u25FB', '\u25FC', '\u25FB', '\u25FC', '\u25FB', '\u25FC'],
    ['\u25FC', '\u25FB', '\u25FC', '\u25FB', '\u25FC', '\u25FB', '\u25FC', '\u25FB'],
    ['\u25FB', '\u25FC', '\u25FB', '\u25FC', '\u25FB', '\u25FC', '\u25FB', '\u25FC'],
    ['\u25FC', '\u25FB', '\u25FC', '\u25FB', '\u25FC', '\u25FB', '\u25FC', '\u25FB'],
    ['\u25FB', '\u25FC', '\u25FB', '\u25FC', '\u25FB', '\u25FC', '\u25FB', '\u25FC'],
    ['\u25FC', '\u25FB', '\u25FC', '\u25FB', '\u25FC', '\u25FB', '\u25FC', '\u25FB'],
    ['\u25FB', '\u25FC', '\u25FB', '\u25FC', '\u25FB', '\u25FC', '\u25FB', '\u25FC']
]

GAME_BOARD2 = [
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
]


def sanitize_move(s):
    """
    splits the move into two parts, beginning and end and returns as a tuple
    :param s: the move string (in the form of "A2 A3")
    :return: a tuple containing the start position and end position
    """
    space_idx = s.find(' ')
    out = (s[:space_idx], s[space_idx + 1:])
    return out


def prompt_players():
    """
    prompts players to input names and
    :return:
    """
    player_list = []
    teams = ['w', 'b']
    for i in range(0, 2):
        name = str(input("Enter player " + str(i + 1) + " name: "))
        p = Player(name, i, teams[i], None)
        player_list.append(p)
    return player_list


def main():
    # func def
    def clear():
        system('cls')

    # init game
    num_players = 2 #int(input("number of players: "))
    player_list = prompt_players()

    game_proc = Engine(num_players, player_list)
    game_proc.load_board(GAME_BOARD)
    game_proc.load_pieces()
    game_proc.display_board()

    # get first move
    player_id = 0
    player_move = sanitize_move(input(player_list[player_id].get_name() + " to move: "))
    winner_found = False
    # TODO: get/sanitize input and init engine using list of num players, player names, teams
    while not winner_found:
        try:
            game_proc.perform_move(player_id, player_move[0], player_move[1])
            clear()
            game_proc.display_board()
            player_id = (player_id + 1) % 2
            player_move = sanitize_move(input(player_list[player_id].get_name() + " to move: "))
        except ValueError:
            player_move = sanitize_move(input("Invalid move. Please try again: "))
            pass

    return 0


main()

