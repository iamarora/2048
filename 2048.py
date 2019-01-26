import random
import sys

###########################################################################
user = ""
num_to_add = (2,4)
array_positions = (0,1,2,3)
board_size = 4
game_board = [[0 for x in range(board_size)] for x in range(board_size)]
print '''2048 :: w = up, s = down, a = left, d = right
q = quit, please hit enter after your input
'''
###########################################################################

def print_board(game_board):
    for row in game_board:
        print row

def transpose(arr):
    new=[]
    for i in range(len(arr[0])):
        new.append([])
        for j in range(len(arr)):
            new[i].append(arr[j][i])
    return new

def reverse(arr):
    new=[]
    for i in range(len(arr)):
        new.append([])
        for j in range(len(arr[0])):
            new[i].append(arr[i][len(arr[0])-j-1])
    return new

def slide_and_add_arr(col):
    new_col = [0, 0, 0, 0]
    j = 0
    previous = None
    for i in range(len(col)):
        if col[i] != 0: # number different from zero
            if previous == None:
                previous = col[i]
            else:
                if previous == col[i]:
                    new_col[j] = 2 * col[i]
                    j += 1
                    previous = None
                else:
                    new_col[j] = previous
                    j += 1
                    previous = col[i]
    if previous != None:
        new_col[j] = previous
    return new_col

def check_remaining_zero(game_board):
    for i in range(len(game_board)):
        for j in range(len(game_board[0])):
            if game_board[i][j]==0:
                return True

def add_tile(game_board):
    a=random.choice(array_positions)
    b=random.choice(array_positions)
    if check_remaining_zero(game_board):
        while(game_board[a][b]!=0):
            a=random.choice(array_positions)
            b=random.choice(array_positions)
        game_board[a][b]=random.choice(num_to_add)
    return game_board

def check_win_state(game_board):
    for i in range(len(game_board)):
        for j in range(len(game_board[0])):
            if game_board[i][j]==2048:
                return True

def check_move_allowed(game_board):
    move_allowed = False
    ##Move allowed if zeros are remaining
    for row in game_board:
        for col in row:
	    if col == 0:
	        move_allowed = True

    if not move_allowed:
        # #Move allowed if next number number is row and column are the same.
        for row in range (0, board_size-1):
            for col in range (0, board_size - 1):
                if (game_board[row][col] == game_board[row+1][col]):
                    move_allowed = True
                if (game_board[row][col] == game_board[row][col+1]):
                    move_allowed = True
    return move_allowed

def tile_moved(new_game_board, old_game_board):
    moved = False
    if new_game_board != old_game_board:
        moved = True
    return moved

def shift_left(game_board):
    new_game_board = []
    for row in game_board:
        new_game_board.append(slide_and_add_arr(row))
    moved = tile_moved(new_game_board, game_board)
    return new_game_board, moved

def shift_up(game_board):
    original_game_board = game_board
    game_board = transpose(game_board)
    game_board, moved = shift_left(game_board)
    new_game_board = transpose(game_board)
    moved = tile_moved(new_game_board, original_game_board)
    return new_game_board, moved

def shift_down(game_board):
    original_game_board = game_board
    game_board = reverse(transpose(game_board))
    game_board, moved = shift_left(game_board)
    new_game_board = transpose(reverse(game_board))
    moved = tile_moved(new_game_board, original_game_board)
    return new_game_board, moved

def shift_right(game_board):
    original_game_board = game_board
    game_board = reverse(game_board)
    game_board, moved = shift_left(game_board)
    new_game_board = reverse(game_board)
    moved = tile_moved(new_game_board, original_game_board)
    return new_game_board, moved

def move(method, game_board):
    game_board, moved = method(game_board)
    if moved:
        game_board = add_tile(game_board)
        print_board(game_board)
    else:
        print "Board couldn't move"
    return game_board

##Initialize Game Board
game_board = add_tile(game_board)
game_board = add_tile(game_board)
print_board(game_board)
##Start game
while (user != "q"):
    user = raw_input('')
    print "User input", user
    successful = False
    if user in ('w', 'a', 's', 'd'):
        if check_win_state(game_board):
            print "WIN!!!"
            print_board(game_board)
            sys.exit()
        if not check_move_allowed(game_board):
            print "No moves left"
            print_board(game_board)
            sys.exit()

    if user == "w":
        print "Up"
        game_board = move(shift_up, game_board)
    elif user == "a":
        print "Left"
        game_board = move(shift_left, game_board)
    elif user == "s":
        print "Down"
        game_board = move(shift_down, game_board)
    elif user == "d": # Right
        print "Right"
        game_board = move(shift_right, game_board)
    elif user == "q":
        print "Exiting."
    else:
        print "Error: input not recognized. Please enter w, a, s, or d or q to quit."

