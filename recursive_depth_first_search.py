"""
Tic Tac Toe implementation adopted from pygames
"""

import copy
from typing import List, Optional, Set, Tuple


X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board: List[List[str]]) -> str:
    """
    Returns player who has the next turn on a board.
    """
    players = ["X", "O"]

    # Count the moves made by each player
    flat_board = [item for _ in board for item in _]
    move_count_dict = {player: flat_board.count(player) for player in players}

    if move_count_dict["O"] < move_count_dict["X"]:
        return "O"
    else:
        return "X"


def actions(board: List[List[str]]) -> Set[Tuple[int, int]]:
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    available_actions = set()
    for i, row in enumerate(board):
        for j, column in enumerate(row):
            if not column:
                available_actions.add((i, j))

    return available_actions


def result(board: List[List[str]], action: Tuple) -> List[List[int]]:
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception
    else:
        # If an objects contains objects that are themselves mutable (lists) - use deepcopy
        board_copy = copy.deepcopy(board)
        board_copy[action[0]][action[1]] = player(board)
        return board_copy


def winner(board: List[List[str]]) -> Optional[str]:
    """
    Returns the winner of the game, if there is one.
    """
    n = len(board)

    # Check horizontally
    for row in board:
        if row[0] is not None and all(x == row[0] for x in row):
            return row[0]

    # Check vertically
    for col in range(n):
        if board[0][col] is not None and all(
            row[col] == board[0][col] for row in board
        ):
            return board[0][col]

    # Check for Diagonal
    middel_value = board[n // 2][n // 2]
    if middel_value is not None and (
        all(board[i][i] == middel_value for i in range(n))
        or all(board[i][n - 1 - i] == middel_value for i in range(n))
    ):
        return middel_value

    return None


def terminal(board: List[List[str]]) -> bool:
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    elif any(None in row for row in board):
        return False  # Game in progress
    else:
        return True


def utility(board: List[List[str]]) -> int:
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    Assumption: Called only if terminal(board) == True
    """
    if winner(board) == None:
        return 0
    elif winner(board) == "X":
        return 1
    elif winner(board) == "O":
        return -1


def minimax(board: List[List[str]]) -> Optional[Tuple[int, int]]:
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    else:
        return recursive_depth_search(board)[0]


def recursive_depth_search(
    board: List[List[str]],
) -> Tuple[Tuple[int, int], int]:
    """
    Recursively conducts depth search for optimal Action-Value Tuple
    """
    action_value_dict = {}
    for action in actions(board):
        next_board = result(board, action)
        if terminal(next_board):
            action_value_dict[action] = utility(next_board)
        else:
            action_value_dict[action] = recursive_depth_search(next_board)[1]

    if player(board) == "X":
        best_value = max(action_value_dict.values())
    else:
        best_value = min(action_value_dict.values())

    for action, value in action_value_dict.items():
        if value == best_value:
            return action, value
