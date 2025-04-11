import pygame
import time
import random
pygame.font.init()

class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
        self.strike = False  # This will indicate if the cube is invalid

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))
        elif self.value != 0:
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

        # If the cube has a strike, we highlight it in red
        if self.strike:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val

    def set_strike(self, strike):
        self.strike = strike  # Set whether the cube has a strike

    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)
        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

class Grid:
    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.win = win
        self.cubes = [[Cube(0, i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.model = None
        self.selected = None
        self.generate_board()  # Generate a random board upon initialization

    def generate_board(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.fill_board(self.board)
        self.update_cubes()
        self.remove_numbers()  # Remove some numbers to create a puzzle

    def update_cubes(self):
        """Update the cube values based on the generated board."""
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].set(self.board[i][j])

    def fill_board(self, board):
        """Fill the board using a backtracking algorithm."""
        empty_pos = self.find_empty(board)
        if not empty_pos:
            return True  # Board is complete
        row, col = empty_pos

        random.shuffle(list(range(1, 10)))  # Shuffle to introduce randomness
        for num in range(1, 10):
            if self.valid(board, num, (row, col)):
                board[row][col] = num
                if self.fill_board(board):
                    return True
                board[row][col] = 0  # Backtrack

        return False

    def find_empty(self, board):
        """Find an empty space on the board (denoted by 0)."""
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def valid(self, board, num, pos):
        """Check if a number can be placed in the given position."""
        row, col = pos

        # Check row
        for i in range(len(board[0])):
            if board[row][i] == num and col != i:
                return False

        # Check column
        for i in range(len(board)):
            if board[i][col] == num and row != i:
                return False

        # Check the 3x3 grid
        box_x = col // 3
        box_y = row // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if board[i][j] == num and (i, j) != pos:
                    return False

        return True

    def remove_numbers(self):
        """Remove random numbers from the filled board to create a puzzle."""
        num_remove = random.randint(40, 50)  # Remove a random number of cells
        for _ in range(num_remove):
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            while self.board[row][col] == 0:
                row = random.randint(0, 8)
                col = random.randint(0, 8)
            self.board[row][col] = 0  # Remove the number (set to 0)
        self.update_cubes()

    def draw(self):
        """Draw the Sudoku grid and cubes."""
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    def select(self, row, col):
        """Select a cell in the grid."""
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False
        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def click(self, pos):
        """Handle mouse click events."""
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def clear(self):
        """Clear the selected cell."""
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def is_finished(self):
        """Check if the board is complete."""
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def solve_gui(self):
        """Solve the board automatically with visual updates."""
        find = self.find_empty(self.board)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.valid(self.board, i, (row, col)):
                self.board[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_cubes()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_gui():
                    return True

                self.board[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_cubes()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False

    def manual_input(self, num):
        """Allow the user to input a number manually."""
        if self.selected:
            row, col = self.selected
            if self.board[row][col] == 0:
                if self.valid(self.board, num, (row, col)):
                    self.board[row][col] = num
                    self.cubes[row][col].set(num)
                    self.cubes[row][col].set_strike(False)  # Clear strike if the input is valid
                else:
                    self.cubes[row][col].set_strike(True)  # Strike the cell if the input is invalid
                self.update_cubes()

# Initialize pygame
pygame.init()

# Game window dimensions
width, height = 540, 540
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sudoku Solver")

# Create a grid instance
grid = Grid(9, 9, width, height, win)

# Main game loop
running = True
while running:
    win.fill((255, 255, 255))  # Fill the screen with white

    grid.draw()  # Draw the grid and cubes
    pygame.display.update()  # Update the display

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Spacebar to start solving
                grid.solve_gui()

            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                num = event.key - pygame.K_1 + 1  # Get the number based on the key press
                grid.manual_input(num)

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            clicked = grid.click(pos)
            if clicked:
                row, col = clicked
                grid.select(row, col)

    pygame.time.Clock().tick(60)  # Frame rate

pygame.quit()
