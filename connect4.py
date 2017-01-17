# Henry Olson
# A Connect 4 game implementation without player UI
# 12/4/2016

# use Python 3's printing function
from __future__ import print_function
from random import randint
import time

def create_board():
    """
    Creates a new Connect 4 game board.

    Returns:
        The board object as a 2-d list
    """
    columns = 7
    rows = 6
    board = [["*" for x in range(columns)] for y in range(rows)]
    return board

def build_combo_hash_table(board):
    """
    Builds a dictionary (hash table) of all the possible combinations that can lead to a victory.
    Best used when the output is copied and directly fed into the game loop, since this won't 
    change as long as we use the same board.

    Args:
        board: a 2-d list

    Returns:
        A dictionary representation of a hash table of the possible combos.
    """
    hash_table = {}
    for i in range(len(board)):
        for j in range(len(board[0])):
            key = str(i) + "~" + str(j)
            arr = []

            # vertical
            if (i <= len(board) - 4):
                arr.append([(i + 1, j), (i + 2, j), (i + 3, j)])
                
            # horizontal and diagonal
            start_range = [-3, -2, -1, 0]
            for k in start_range:
                if (j + k) >= 0 and (j + k + 3) < len(board[0]):
                    arr.append([(i, j+k), (i, j+k+1), (i, j+k+2), (i, j+k+3)])
                    if (i + k) >= 0 and (i + k + 3) < len(board):
                        arr.append([(i+k, j+k), (i+k+1, j+k+1), (i+k+2, j+k+2), (i+k+3, j+k+3)])
                    if (i - k) < len(board) and (i - k - 3) >= 0:
                        arr.append([(i-k, j+k), (i-k-1, j+k+1), (i-k-2, j+k+2), (i-k-3, j+k+3)])

            hash_table[key] = arr

    print(hash_table)
    return hash_table

def print_board(board):
    """
    Prints the current state of a Connect 4 game board.

    Args:
        board: a 2-d list
    """
    for i in range(len(board)):
        for j in range(len(board[i])):
            print(board[i][j], end=" ")
        print("", end="\n")
    print("", end="\n")


def place_piece(board, player, column):
    """
    Places a new piece onto the Connect 4 game board.

    Args:
        board: a 2-d list
        player: a character used to represent the player ('x' or 'o')
        column: the array index of the column to place the piece into
    
    Returns:
        Returns a key of the last played piece, or if unsuccessful, a blank string.
    """
    # starting at the bottom, find the next unoccupied space in the column
    row = 5
    if column < 0 or column >= len(board[0]):
        print("invalid move, outside of column range")
        return ""
    while board[row][column] != "*":
        if row == 0:
            print("invalid move, column is full")
            return ""
        row -= 1
    board[row][column] = player
    return str(row) + "~" + str(column)

def check_combinations(board, combinations, player, key):
    """
    Check the possible winning combinations of the last played chip at key i~j to see if there is a match.

    Args:
        board: a 2-d list
        combinations: the dictionary of possible winning combinations
        player: a character used to represent the player ('x' or 'o')
        key: the concatenation of the row and column of the last played move (i.e. 3~4)
    
    Returns:
        Returns True if the last played move created a valid 4 chain.
    """
    valid_chains = []
    if key in combinations:
        valid_chains = combinations[key]
    else:
        return False
    
    for chain in valid_chains:
        valid = True
        for tup in chain:
            if board[tup[0]][tup[1]] != player:
                valid = False
                break
        if valid:
            print(player + " wins!")
            return True
    return False

def check_win(board, player, piece_count, combinations, key):
    """
    Check to see if the player has won the game.

    Args:
        board: a 2-d list
        player: a character used to represent the player ('x' or 'o')
        piece_count: the total number of pieces placed in the game so far.
        combinations: the dictionary of possible winning combinations used in check_combinations
        key: the concatenation of the row and column of the last played move (i.e. 3~4)
    
    Returns:
        Returns True if a player has won or there is a draw. Returns False if the game will continue.
    """
    if piece_count == len(board) * len(board[0]):
        print ("It's a draw!")
        return True
    result = check_combinations(board, combinations, player, key)
    if result:
        return True
    return False


# game loop for randomized computer moves
def game_loop():
    """
    Runs a randomized simulation of Connect 4.
    """
    game_board = create_board()

    # obtained from output of build_combo_hash_table
    # ideally, if we were doing a number of trials, we could run that function again to build the table
    # while building the table takes O(n^2) time, it allows us to do O(1) lookups for win conditions,
    # therefore this strategy is advantages when we run a lot of games after building this table
    combinations = {'3~6': [[(3, 3), (3, 4), (3, 5), (3, 6)], [(0, 3), (1, 4), (2, 5), (3, 6)]], '3~4': [[(3, 1), (3, 2), (3, 3), (3, 4)], [(0, 1), (1, 2), (2, 3), (3, 4)], [(3, 2), (3, 3), (3, 4), (3, 5)], [(1, 2), (2, 3), (3, 4), (4, 5)], [(5, 2), (4, 3), (3, 4), (2, 5)], [(3, 3), (3, 4), (3, 5), (3, 6)], [(2, 3), (3, 4), (4, 5), (5, 6)], [(4, 3), (3, 4), (2, 5), (1, 6)]], '3~5': [[(3, 2), (3, 3), (3, 4), (3, 5)], [(0, 2), (1, 3), (2, 4), (3, 5)], [(3, 3), (3, 4), (3, 5), (3, 6)], [(1, 3), (2, 4), (3, 5), (4, 6)], [(5, 3), (4, 4), (3, 5), (2, 6)]], '3~2': [[(3, 0), (3, 1), (3, 2), (3, 3)], [(1, 0), (2, 1), (3, 2), (4, 3)], [(5, 0), (4, 1), (3, 2), (2, 3)], [(3, 1), (3, 2), (3, 3), (3, 4)], [(2, 1), (3, 2), (4, 3), (5, 4)], [(4, 1), (3, 2), (2, 3), (1, 4)], [(3, 2), (3, 3), (3, 4), (3, 5)], [(3, 2), (2, 3), (1, 4), (0, 5)]], '3~3': [[(3, 0), (3, 1), (3, 2), (3, 3)], [(0, 0), (1, 1), (2, 2), (3, 3)], [(3, 1), (3, 2), (3, 3), (3, 4)], [(1, 1), (2, 2), (3, 3), (4, 4)], [(5, 1), (4, 2), (3, 3), (2, 4)], [(3, 2), (3, 3), (3, 4), (3, 5)], [(2, 2), (3, 3), (4, 4), (5, 5)], [(4, 2), (3, 3), (2, 4), (1, 5)], [(3, 3), (3, 4), (3, 5), (3, 6)], [(3, 3), (2, 4), (1, 5), (0, 6)]], '3~0': [[(3, 0), (3, 1), (3, 2), (3, 3)], [(3, 0), (2, 1), (1, 2), (0, 3)]], '3~1': [[(3, 0), (3, 1), (3, 2), (3, 3)], [(2, 0), (3, 1), (4, 2), (5, 3)], [(4, 0), (3, 1), (2, 2), (1, 3)], [(3, 1), (3, 2), (3, 3), (3, 4)], [(3, 1), (2, 2), (1, 3), (0, 4)]], '2~3': [[(3, 3), (4, 3), (5, 3)], [(2, 0), (2, 1), (2, 2), (2, 3)], [(5, 0), (4, 1), (3, 2), (2, 3)], [(2, 1), (2, 2), (2, 3), (2, 4)], [(0, 1), (1, 2), (2, 3), (3, 4)], [(4, 1), (3, 2), (2, 3), (1, 4)], [(2, 2), (2, 3), (2, 4), (2, 5)], [(1, 2), (2, 3), (3, 4), (4, 5)], [(3, 2), (2, 3), (1, 4), (0, 5)], [(2, 3), (2, 4), (2, 5), (2, 6)], [(2, 3), (3, 4), (4, 5), (5, 6)]], '2~2': [[(3, 2), (4, 2), (5, 2)], [(2, 0), (2, 1), (2, 2), (2, 3)], [(0, 0), (1, 1), (2, 2), (3, 3)], [(4, 0), (3, 1), (2, 2), (1, 3)], [(2, 1), (2, 2), (2, 3), (2, 4)], [(1, 1), (2, 2), (3, 3), (4, 4)], [(3, 1), (2, 2), (1, 3), (0, 4)], [(2, 2), (2, 3), (2, 4), (2, 5)], [(2, 2), (3, 3), (4, 4), (5, 5)]], '2~1': [[(3, 1), (4, 1), (5, 1)], [(2, 0), (2, 1), (2, 2), (2, 3)], [(1, 0), (2, 1), (3, 2), (4, 3)], [(3, 0), (2, 1), (1, 2), (0, 3)], [(2, 1), (2, 2), (2, 3), (2, 4)], [(2, 1), (3, 2), (4, 3), (5, 4)]], '2~0': [[(3, 0), (4, 0), (5, 0)], [(2, 0), (2, 1), (2, 2), (2, 3)], [(2, 0), (3, 1), (4, 2), (5, 3)]], '2~6': [[(3, 6), (4, 6), (5, 6)], [(2, 3), (2, 4), (2, 5), (2, 6)], [(5, 3), (4, 4), (3, 5), (2, 6)]], '2~5': [[(3, 5), (4, 5), (5, 5)], [(2, 2), (2, 3), (2, 4), (2, 5)], [(5, 2), (4, 3), (3, 4), (2, 5)], [(2, 3), (2, 4), (2, 5), (2, 6)], [(0, 3), (1, 4), (2, 5), (3, 6)], [(4, 3), (3, 4), (2, 5), (1, 6)]], '2~4': [[(3, 4), (4, 4), (5, 4)], [(2, 1), (2, 2), (2, 3), (2, 4)], [(5, 1), (4, 2), (3, 3), (2, 4)], [(2, 2), (2, 3), (2, 4), (2, 5)], [(0, 2), (1, 3), (2, 4), (3, 5)], [(4, 2), (3, 3), (2, 4), (1, 5)], [(2, 3), (2, 4), (2, 5), (2, 6)], [(1, 3), (2, 4), (3, 5), (4, 6)], [(3, 3), (2, 4), (1, 5), (0, 6)]], '4~5': [[(4, 2), (4, 3), (4, 4), (4, 5)], [(1, 2), (2, 3), (3, 4), (4, 5)], [(4, 3), (4, 4), (4, 5), (4, 6)], [(2, 3), (3, 4), (4, 5), (5, 6)]], '4~4': [[(4, 1), (4, 2), (4, 3), (4, 4)], [(1, 1), (2, 2), (3, 3), (4, 4)], [(4, 2), (4, 3), (4, 4), (4, 5)], [(2, 2), (3, 3), (4, 4), (5, 5)], [(4, 3), (4, 4), (4, 5), (4, 6)], [(5, 3), (4, 4), (3, 5), (2, 6)]], '5~2': [[(5, 0), (5, 1), (5, 2), (5, 3)], [(5, 1), (5, 2), (5, 3), (5, 4)], [(5, 2), (5, 3), (5, 4), (5, 5)], [(5, 2), (4, 3), (3, 4), (2, 5)]], '4~6': [[(4, 3), (4, 4), (4, 5), (4, 6)], [(1, 3), (2, 4), (3, 5), (4, 6)]], '4~1': [[(4, 0), (4, 1), (4, 2), (4, 3)], [(5, 0), (4, 1), (3, 2), (2, 3)], [(4, 1), (4, 2), (4, 3), (4, 4)], [(4, 1), (3, 2), (2, 3), (1, 4)]], '4~0': [[(4, 0), (4, 1), (4, 2), (4, 3)], [(4, 0), (3, 1), (2, 2), (1, 3)]], '4~3': [[(4, 0), (4, 1), (4, 2), (4, 3)], [(1, 0), (2, 1), (3, 2), (4, 3)], [(4, 1), (4, 2), (4, 3), (4, 4)], [(2, 1), (3, 2), (4, 3), (5, 4)], [(4, 2), (4, 3), (4, 4), (4, 5)], [(5, 2), (4, 3), (3, 4), (2, 5)], [(4, 3), (4, 4), (4, 5), (4, 6)], [(4, 3), (3, 4), (2, 5), (1, 6)]], '4~2': [[(4, 0), (4, 1), (4, 2), (4, 3)], [(2, 0), (3, 1), (4, 2), (5, 3)], [(4, 1), (4, 2), (4, 3), (4, 4)], [(5, 1), (4, 2), (3, 3), (2, 4)], [(4, 2), (4, 3), (4, 4), (4, 5)], [(4, 2), (3, 3), (2, 4), (1, 5)]], '5~4': [[(5, 1), (5, 2), (5, 3), (5, 4)], [(2, 1), (3, 2), (4, 3), (5, 4)], [(5, 2), (5, 3), (5, 4), (5, 5)], [(5, 3), (5, 4), (5, 5), (5, 6)]], '5~5': [[(5, 2), (5, 3), (5, 4), (5, 5)], [(2, 2), (3, 3), (4, 4), (5, 5)], [(5, 3), (5, 4), (5, 5), (5, 6)]], '5~0': [[(5, 0), (5, 1), (5, 2), (5, 3)], [(5, 0), (4, 1), (3, 2), (2, 3)]], '5~1': [[(5, 0), (5, 1), (5, 2), (5, 3)], [(5, 1), (5, 2), (5, 3), (5, 4)], [(5, 1), (4, 2), (3, 3), (2, 4)]], '1~4': [[(2, 4), (3, 4), (4, 4)], [(1, 1), (1, 2), (1, 3), (1, 4)], [(4, 1), (3, 2), (2, 3), (1, 4)], [(1, 2), (1, 3), (1, 4), (1, 5)], [(3, 2), (2, 3), (1, 4), (0, 5)], [(1, 3), (1, 4), (1, 5), (1, 6)], [(0, 3), (1, 4), (2, 5), (3, 6)]], '1~5': [[(2, 5), (3, 5), (4, 5)], [(1, 2), (1, 3), (1, 4), (1, 5)], [(4, 2), (3, 3), (2, 4), (1, 5)], [(1, 3), (1, 4), (1, 5), (1, 6)], [(3, 3), (2, 4), (1, 5), (0, 6)]], '1~6': [[(2, 6), (3, 6), (4, 6)], [(1, 3), (1, 4), (1, 5), (1, 6)], [(4, 3), (3, 4), (2, 5), (1, 6)]], '5~3': [[(5, 0), (5, 1), (5, 2), (5, 3)], [(2, 0), (3, 1), (4, 2), (5, 3)], [(5, 1), (5, 2), (5, 3), (5, 4)], [(5, 2), (5, 3), (5, 4), (5, 5)], [(5, 3), (5, 4), (5, 5), (5, 6)], [(5, 3), (4, 4), (3, 5), (2, 6)]], '1~0': [[(2, 0), (3, 0), (4, 0)], [(1, 0), (1, 1), (1, 2), (1, 3)], [(1, 0), (2, 1), (3, 2), (4, 3)]], '1~1': [[(2, 1), (3, 1), (4, 1)], [(1, 0), (1, 1), (1, 2), (1, 3)], [(0, 0), (1, 1), (2, 2), (3, 3)], [(1, 1), (1, 2), (1, 3), (1, 4)], [(1, 1), (2, 2), (3, 3), (4, 4)]], '1~2': [[(2, 2), (3, 2), (4, 2)], [(1, 0), (1, 1), (1, 2), (1, 3)], [(3, 0), (2, 1), (1, 2), (0, 3)], [(1, 1), (1, 2), (1, 3), (1, 4)], [(0, 1), (1, 2), (2, 3), (3, 4)], [(1, 2), (1, 3), (1, 4), (1, 5)], [(1, 2), (2, 3), (3, 4), (4, 5)]], '1~3': [[(2, 3), (3, 3), (4, 3)], [(1, 0), (1, 1), (1, 2), (1, 3)], [(4, 0), (3, 1), (2, 2), (1, 3)], [(1, 1), (1, 2), (1, 3), (1, 4)], [(3, 1), (2, 2), (1, 3), (0, 4)], [(1, 2), (1, 3), (1, 4), (1, 5)], [(0, 2), (1, 3), (2, 4), (3, 5)], [(1, 3), (1, 4), (1, 5), (1, 6)], [(1, 3), (2, 4), (3, 5), (4, 6)]], '0~1': [[(1, 1), (2, 1), (3, 1)], [(0, 0), (0, 1), (0, 2), (0, 3)], [(0, 1), (0, 2), (0, 3), (0, 4)], [(0, 1), (1, 2), (2, 3), (3, 4)]], '0~0': [[(1, 0), (2, 0), (3, 0)], [(0, 0), (0, 1), (0, 2), (0, 3)], [(0, 0), (1, 1), (2, 2), (3, 3)]], '0~3': [[(1, 3), (2, 3), (3, 3)], [(0, 0), (0, 1), (0, 2), (0, 3)], [(3, 0), (2, 1), (1, 2), (0, 3)], [(0, 1), (0, 2), (0, 3), (0, 4)], [(0, 2), (0, 3), (0, 4), (0, 5)], [(0, 3), (0, 4), (0, 5), (0, 6)], [(0, 3), (1, 4), (2, 5), (3, 6)]], '0~2': [[(1, 2), (2, 2), (3, 2)], [(0, 0), (0, 1), (0, 2), (0, 3)], [(0, 1), (0, 2), (0, 3), (0, 4)], [(0, 2), (0, 3), (0, 4), (0, 5)], [(0, 2), (1, 3), (2, 4), (3, 5)]], '0~5': [[(1, 5), (2, 5), (3, 5)], [(0, 2), (0, 3), (0, 4), (0, 5)], [(3, 2), (2, 3), (1, 4), (0, 5)], [(0, 3), (0, 4), (0, 5), (0, 6)]], '0~4': [[(1, 4), (2, 4), (3, 4)], [(0, 1), (0, 2), (0, 3), (0, 4)], [(3, 1), (2, 2), (1, 3), (0, 4)], [(0, 2), (0, 3), (0, 4), (0, 5)], [(0, 3), (0, 4), (0, 5), (0, 6)]], '5~6': [[(5, 3), (5, 4), (5, 5), (5, 6)], [(2, 3), (3, 4), (4, 5), (5, 6)]], '0~6': [[(1, 6), (2, 6), (3, 6)], [(0, 3), (0, 4), (0, 5), (0, 6)], [(3, 3), (2, 4), (1, 5), (0, 6)]]}
    piece_count = 0
    players = ["x", "o"]
    player_select = 0
    win = False

    # main loop, keep going until there is a win or a draw
    while win == False:
        player = players[player_select]

        # uncomment this if you want to see the plays happen slowly
        #time.sleep(0.5)

        #place random piece
        key = place_piece(game_board, player, randint(0,6))
        if key == "":
            continue
        piece_count += 1
        print_board(game_board)
        win = check_win(game_board, player, piece_count, combinations, key)
        player_select = (player_select + 1) % 2

game_loop()