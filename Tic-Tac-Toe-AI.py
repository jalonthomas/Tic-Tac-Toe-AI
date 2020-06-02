from math import inf
import time

human = 1
computer = -1

board = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]

#Checks if either player has won
def has_won(board, player):
    win_states = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]],
    ]

    if [player, player, player] in win_states:
        return True
    else:
        return False

#Handles move selection
def play(empty_cells, player):
    if player == human:
        available_moves = {
            1: [0, 0], 2: [0, 1], 3: [0, 2],
            4: [1, 0], 5: [1, 1], 6: [1, 2],
            7: [2, 0], 8: [2, 1], 9: [2, 2],
        }
        while True:
            try:
                move = int(input("Enter number 1-9: "))
                move = available_moves[move]
                if move in empty_cells:
                    board[move[0]][move[1]] = human
                    break
                else:
                    print("That move is not available\n")
            except:
                print("Not a valid number\n")
    else:
        ai_play(empty_cells)


#Generates best move by evauluating each potential move with minimax algorithm
def ai_play(empty_cells):
    best_val = inf
    move = []
    for cell in empty_cells:
        board[cell[0]][cell[1]] = computer
        result = minimax(board, 0, human)
        board[cell[0]][cell[1]] = 0

        if result < best_val:
            best_val = result
            move = cell

    board[move[0]][move[1]] = computer
    time.sleep(1)


# Recursively iterate through possible game states and return best score
# based on whether the score should be minimized or maximized
def minimax(state, depth, player):
    scores = []
    empty_cells = get_empty_cells(state)

    if has_won(state, -player) or len(empty_cells) == 0:
        return evaluate(state) * (10 - depth)

    for cell in empty_cells:
        state[cell[0]][cell[1]] = player
        scores.append(minimax(state, depth + 1, -player))
        state[cell[0]][cell[1]] = 0

    if player == human:
        best = -inf
        for score in scores:
            if score > best:
                best = score
    else:
        best = inf
        for score in scores:
            if score < best:
                best = score
    return best


# return score of end state
def evaluate(state):
    if has_won(state, human):
        return 10
    elif has_won(state, computer):
        return -10
    else:
        return 0


def get_empty_cells(board):
    cells = []
    for row in range(3):
        for col in range(3):
            if board[row][col] == 0:
                cells.append([row, col])
    return cells


#Draws board
def render():
    chars = {
        1: "X",
        -1: "O",
        0: " ",
    }

    line = "_______________"

    for row in board:
        print("\n" + line)
        for cell in row:
            print(f'| {chars[cell]} |', end='')
    print()


#Start menu
def choose_order():
    print()
    choice = input("Would you like to go first y or n or enter to quit: ")

    if choice == "y":
        render()
        return human
    elif choice == "n":
        render()
        return computer
    else:
        exit()

#Gameplay loop
def main():
    global board
    board = [[0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]]
    player = choose_order()

    while True:
        empty_cells = get_empty_cells(board)
        play(empty_cells, player)
        render()

        if has_won(board, player):
            if player == human:
                print("Player Wins")
            else:
                print("Computer Wins")
            break
        elif len(empty_cells) - 1 == 0:
            print("It's a draw")
            break
        player = -player
    main()


if __name__ == "__main__":
    main()
