def solve(bo):
    """
    Solves the Sudoku board using backtracking.
    :param bo: 2D list representing the Sudoku board
    :return: bool (True if solved, False otherwise)
    """
    find = find_empty(bo)
    if not find:
        return True  # Board is solved
    else:
        row, col = find

    for i in range(1, 10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i  # Place the number

            if solve(bo):
                return True  # Recursive solve call

            bo[row][col] = 0  # Reset if solution fails

    return False


def valid(bo, num, pos):
    """
    Checks if placing a number at a position is valid.
    :param bo: 2D list representing the Sudoku board
    :param num: int (number to place)
    :param pos: tuple (row, col) - position to place the number
    :return: bool (True if valid, False otherwise)
    """
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check 3x3 box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True


def print_board(bo):
    """
    Prints the Sudoku board in a readable format.
    :param bo: 2D list representing the Sudoku board
    :return: None
    """
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - -")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(bo[i][j])  # End of row
            else:
                print(str(bo[i][j]) + " ", end="")


def find_empty(bo):
    """
    Finds an empty space (0) in the Sudoku board.
    :param bo: 2D list representing the Sudoku board
    :return: tuple (row, col) - position of the empty space, or None if full
    """
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return i, j  # Row, Column

    return None