import random

def generate_sudoku():
    """
    Generates a random Sudoku puzzle with a unique solution.
    """
    board = [[0 for _ in range(9)] for _ in range(9)]

    def fill_diagonal():
        # Fill the diagonal 3x3 boxes
        for i in range(0, 9, 3):
            fill_box(i, i)

    def fill_box(row, col):
        nums = random.sample(range(1, 10), 9)
        for i in range(3):
            for j in range(3):
                board[row + i][col + j] = nums.pop()

    def remove_numbers():
        # Randomly remove numbers to create a puzzle
        attempts = 30
        while attempts > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            while board[row][col] == 0:
                row = random.randint(0, 8)
                col = random.randint(0, 8)
            # Backup the current number
            backup = board[row][col]
            board[row][col] = 0

            # Check if the board still has a unique solution
            temp_board = [row[:] for row in board]
            if not solve(temp_board) or not is_unique(temp_board):
                board[row][col] = backup
            else:
                attempts -= 1

    def is_unique(temp_board):
        """
        Checks if a Sudoku board has a unique solution.
        """
        solutions = []

        def find_solution(temp_board):
            if len(solutions) > 1:
                return
            find = find_empty(temp_board)
            if not find:
                solutions.append([row[:] for row in temp_board])
                return
            else:
                row, col = find

            for i in range(1, 10):
                if valid(temp_board, i, (row, col)):
                    temp_board[row][col] = i
                    find_solution(temp_board)
                    temp_board[row][col] = 0

        find_solution(temp_board)
        return len(solutions) == 1

    fill_diagonal()
    solve(board)  # Fill the remaining cells
    remove_numbers()
    return board