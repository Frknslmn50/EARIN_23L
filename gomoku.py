# Gomoku (Five in a Row) Game
import random

import numpy as np

# Initialize the board
board_size = 15
board = [[' ' for _ in range(board_size)] for _ in range(board_size)]


# Define a function to print the board
def print_board():
    print("   ", end="")
    for i in range(board_size):
        print(chr(ord('a') + i), end=" ")
    print()
    for i in range(board_size):
        print("{:2d}".format(i + 1), end=" ")
        for j in range(board_size):
            print(board[i][j], end=" ")
        print()


def check_win(player):
    # Check horizontal, vertical, and diagonal wins
    for i in range(board_size):
        for j in range(board_size):
            if j + 4 < board_size and all(board[i][j + k] == player for k in range(5)):  # Check horizontal
                return True
            if i + 4 < board_size and all(board[i + k][j] == player for k in range(5)):  # Check vertical
                return True
            if i + 4 < board_size and j + 4 < board_size and all(
                    board[i + k][j + k] == player for k in range(5)):  # Check diagonal (top-left to bottom-right)
                return True
            if i >= 4 and j + 4 < board_size and all(
                    board[i - k][j + k] == player for k in range(5)):  # Check diagonal (bottom-left to top-right)
                return True
    # If no win condition is met, return False
    return False


def evaluate_board(player):
    """
    A heuristic evaluation function that calculates the value of a Gomoku game board for a given player.
    """
    rows = board_size
    cols = board_size
    score = 0

    # Keep track of evaluated pieces to avoid double counting
    evaluated_pieces = np.zeros((board_size, board_size))

    # Count the number of consecutive pieces in all directions
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == player and evaluated_pieces[r, c] == 0:
                # Horizontal
                if c <= cols - 5:
                    row_score = 1
                    for i in range(1, 5):
                        if evaluated_pieces[r, c+i]:
                            break
                        if board[r][c + i] == player:
                            row_score += 1
                            evaluated_pieces[r, c + i] += 1
                        else:
                            break
                    if row_score == 5:
                        return 1000
                    score += row_score
                # Vertical
                if r <= rows - 5:
                    col_score = 1
                    for i in range(1, 5):
                        if evaluated_pieces[r+i, c]:
                            break
                        if board[r + i][c] == player:
                            col_score += 1
                            evaluated_pieces[r + i, c] += 1
                        else:
                            break
                    if col_score == 5:
                        return 1000
                    score += col_score
                # Diagonal down-right
                if c <= cols - 5 and r <= rows - 5:
                    diag_score = 1
                    for i in range(1, 5):
                        if evaluated_pieces[r+i, c+i]:
                            break
                        if board[r + i][c + i] == player:
                            diag_score += 1
                            evaluated_pieces[r + i, c + i] += 1
                        else:
                            break
                    if diag_score == 5:
                        return 1000
                    score += diag_score
                # Diagonal up-right
                if c <= cols - 5 and r >= 4:
                    diag_score = 1
                    for i in range(1, 5):
                        if evaluated_pieces[r-i, c-i]:
                            break
                        if board[r - i][c + i] == player:
                            diag_score += 1
                            evaluated_pieces[r - i, c + i] += 1
                        else:
                            break
                    if diag_score == 5:
                        return 1000
                    score += diag_score

    evaluated_pieces = np.zeros((board_size, board_size))

    # Subtract the number of consecutive pieces of the opponent
    opponent = 'X' if player == 'O' else 'O'
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == opponent:
                # Horizontal
                if c <= cols - 5:
                    row_score = 1
                    for i in range(1, 5):
                        if evaluated_pieces[r, c+i]:
                            break
                        if board[r][c + i] == opponent:
                            row_score += 1
                            evaluated_pieces[r, c + i] += 1
                        else:
                            break
                    if row_score == 5:
                        return -1000
                    score -= row_score
                # Vertical
                if r <= rows - 5:
                    col_score = 1
                    for i in range(1, 5):
                        if evaluated_pieces[r+i, c]:
                            break
                        if board[r + i][c] == opponent:
                            col_score += 1
                        else:
                            break
                    if col_score == 5:
                        return -1000
                    score -= col_score
                # Diagonal down-right
                if c <= cols - 5 and r <= rows - 5:
                    diag_score = 1
                    for i in range(1, 5):
                        if evaluated_pieces[r+i, c+i]:
                            break
                        if board[r + i][c + i] == opponent:
                            diag_score += 1
                        else:
                            break
                    if diag_score == 5:
                        return -1000
                    score -= diag_score
                # Diagonal up-right
                if c <= cols - 5 and r >= 4:
                    diag_score = 1
                    for i in range(1, 5):
                        if evaluated_pieces[r-i, c-i]:
                            break
                        if board[r - i][c + i] == opponent:
                            diag_score += 1
                        else:
                            break
                    if diag_score == 5:
                        return -1000
                    score -= diag_score
    return score


# Define the Minimax algorithm with Alpha-Beta pruning
def minimax_alpha_beta_pruning(player, depth, alpha, beta, maximizing_player):
    # Check for a terminal state (win or tie)
    if check_win(player):
        return (10000 - depth) if maximizing_player else (-10000 + depth), None
    if check_win('X' if player == 'O' else 'O'):
        return (-10000 + depth) if maximizing_player else (10000 - depth), None
    if depth == 0:
        score = evaluate_board(player)
        return score if maximizing_player else -1 * score, None
    # Initialize variables
    best_score = float('-inf') if maximizing_player else float('inf')
    best_move = None
    # Generate all possible moves
    moves = []
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == ' ':
                moves.append((i, j))
    # Shuffle the moves to avoid always choosing the same move
    random.shuffle(moves)
    # Iterate over all possible moves
    for move in moves:
        # Apply the move
        row, col = move
        board[row][col] = player
        # Calculate the score for the move
        score, _ = minimax_alpha_beta_pruning('O' if player == 'X' else 'X', depth - 1, alpha, beta,
                                              not maximizing_player)
        # Undo the move
        board[row][col] = ' '
        # Update the best score and best move
        if maximizing_player:
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
        else:
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, best_score)
            if beta <= alpha:
                break
    # Return the best score and best move
    return best_score, best_move


# Define the main game loop
def main():
    # Initialize variables
    human_player = input("Do you want to play as X or O? ").upper()
    while human_player not in ['X', 'O']:
        human_player = input("Invalid input. Do you want to play as X or O? ").upper()
    current_player = 'X'
    turn = 1
    # Loop until a player wins or the board is full
    while turn <= board_size * board_size:
        # Print the current board
        print("Turn {}: Player {}".format(turn, current_player))
        print_board()
        # Get the player's move
        if current_player == human_player:
            while True:
                move = input("Enter your move (e.g. 'a1'): ")
                if (len(move) == 2 or len(move) == 3) and move[0] in 'abcdefghijklmno' and move[1] in '123456789101112131415':
                    row = int(move[1:]) - 1
                    col = ord(move[0]) - ord('a')
                    if board[row][col] == ' ':
                        break
            # Update the board
            board[row][col] = current_player
        else:
            # Get the AI's move using Minimax with Alpha-Beta pruning
            _, (row, col) = minimax_alpha_beta_pruning(current_player, 3, float('-inf'), float('inf'), True)
            # Update the board
            board[row][col] = current_player
            print("AI chooses", chr(ord('a') + col), row + 1)
        # Check if the player has won
        if check_win(current_player):
            print_board()
            if current_player == human_player:
                print("You win!")
            else:
                print("AI wins!")
            return
        # Switch to the other player
        current_player = 'O' if current_player == 'X' else 'X'
        turn += 1
    # If no player has won and the board is full, it's a tie
    print_board()
    print("It's a tie!")


# Start the game
main()
