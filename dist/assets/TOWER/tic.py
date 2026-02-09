import numpy as np
import random

board = np.zeros((3, 3)).astype(int)
turn = 1
move = 9

def check_win():
    # Check rows and columns
    for i in range(3):
        if abs(board[i, :].sum()) == 3:  # Check rows
            return True
        if abs(board[:, i].sum()) == 3:  # Check columns
            return True
    
    # Check diagonals
    if abs(board.trace()) == 3 or abs(np.fliplr(board).trace()) == 3:
        return True
    
    return False

def play_turn():
    global turn  # Declare turn as global since we're modifying it
    
    if turn == 1:
        x = int(input(f"What is player {turn}'s x position? "))
        y = int(input(f"What is player {turn}'s y position? "))
    else:
        x = random.randint(0, 2)
        y = random.randint(0, 2)
    
    try:
        if board[y, x] == 0:
            board[y, x] = turn
        else:
            if turn == 1:
                print("The board already contains a mark at this position")
            play_turn()
    except IndexError:
        print("Input error - position must be between 0 and 2")
        play_turn()

while move > 0:
    print(board)
    play_turn()
    
    if check_win():
        print(f"Player {turn} has won!")
        break
    
    turn = turn * -1
    move = move - 1

# If no one won
if move == 0 and not check_win():
    print("It's a tie!")