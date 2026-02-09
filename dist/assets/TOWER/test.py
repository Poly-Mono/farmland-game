import numpy as np
import random

board = np.zeros((3, 3)).astype(int)
turn = 1
move = 9

def play_turn():
    if(turn ==1):
        x = int(input(f"What is player {turn}'s x position?")) # kode akan dijelaskan dibawah
        y = int(input(f"What is player {turn}'s y position?")) # dalam bagian (a)
    else:
        x = random.randint(0,2); # kode akan dijelaskan dibawah
        y = random.randint(0,2); # dalam bagian (b)
    else:
    # Tambahkan di dalam play_turn() setelah else statement
        try: # dijelaskan dibagian (a)
            if board[y, x]==0:   # dijelaskan dibagian (b)
                board[y, x]=turn # dijelaskan dibagian (b)
            else:                                       # dijelaskan dibagian (C)
                if(turn == 1):                          # dijelaskan dibagian (C) 
                    print("The board already contains") # dijelaskan dibagian (C)
                play_turn() 
        except IndexError:        # dijelaskan dibagian (D)
            print("Input error")  # dijelaskan dibagian (D)
            play_turn()           # dijelaskan dibagian (D)

while move >0:
    # Draw the board
#         a
#----------------------
    print (board) 
    play_turn()   
#----------------------
    if check_win():
#         b
#--------------------------------------------
        print (f"Player {turn} has won!")
        break
#--------------------------------------------
#         c
#--------------------------------------------
    turn = turn*-1
    move = move -1
#--------------------------------------------