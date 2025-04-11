import pygame
import random
import time

# Initialize pygame
pygame.init()

# Screen dimensions and colors
WIDTH, HEIGHT = 600, 650
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (100, 149, 237)
RED = (255, 0, 0)
GREEN = (34, 139, 34)

# Fonts
FONT = pygame.font.Font(None, 40)
TITLE_FONT = pygame.font.Font(None, 60)


class Sudoku:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Sudoku Solver")
        self.board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.solution = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.selected_cell = None
        self.running = True
        self.difficulty = None  # To store difficulty level
        self.show_difficulty_menu()

    def show_difficulty_menu(self):
        """Display the difficulty level menu."""
        while True:
            self.screen.fill(WHITE)
            self.draw_text("Select Difficulty", WIDTH // 2, HEIGHT // 4, BLACK, TITLE_FONT)
            
            # Draw difficulty buttons
            pygame.draw.rect(self.screen, GREEN, (50, HEIGHT // 2, 200, 40))
            pygame.draw.rect(self.screen, BLUE, (350, HEIGHT // 2, 200, 40))
            pygame.draw.rect(self.screen, RED, (50, HEIGHT // 2 + 60, 200, 40))
            pygame.draw.rect(self.screen, BLACK, (350, HEIGHT // 2 + 60, 200, 40))

            self.draw_text("Easy", 150, HEIGHT // 2 + 20, WHITE)
            self.draw_text("Medium", 450, HEIGHT // 2 + 20, WHITE)
            self.draw_text("Hard", 150, HEIGHT // 2 + 80, WHITE)
            self.draw_text("Exit", 450, HEIGHT // 2 + 80, WHITE)

            pygame.display.flip()

            # Event handling for selecting difficulty
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if 50 <= pos[0] <= 250 and HEIGHT // 2 <= pos[1] <= HEIGHT // 2 + 40:
                        self.difficulty = "Easy"
                        self.generate_board()
                        return
                    elif 350 <= pos[0] <= 550 and HEIGHT // 2 <= pos[1] <= HEIGHT // 2 + 40:
                        self.difficulty = "Medium"
                        self.generate_board()
                        return
                    elif 50 <= pos[0] <= 250 and HEIGHT // 2 + 60 <= pos[1] <= HEIGHT // 2 + 100:
                        self.difficulty = "Hard"
                        self.generate_board()
                        return
                    elif 350 <= pos[0] <= 550 and HEIGHT // 2 + 60 <= pos[1] <= HEIGHT // 2 + 100:
                        pygame.quit()
                        exit()

    def generate_board(self):
        """Generate a random Sudoku puzzle based on selected difficulty."""
        self.board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.fill_board()  # Fill the board with a valid Sudoku solution
        self.solution = [row[:] for row in self.board]  # Save the solution
        
        # Set the number of blocks to remove based on difficulty
        if self.difficulty == "Easy":
            blocks_to_remove = 30
        elif self.difficulty == "Medium":
            blocks_to_remove = 40
        elif self.difficulty == "Hard":
            blocks_to_remove = 50

        self.remove_numbers(blocks_to_remove)  # Remove the appropriate number of blocks

    def fill_board(self):
        """Fill the board with a valid Sudoku solution using backtracking."""
        self.solve()

    def remove_numbers(self, count):
        """Remove numbers from the board to create a puzzle."""
        removed = 0
        while removed < count:
            row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                removed += 1

    def is_valid(self, row, col, num):
        """Check if a number can be placed in the given cell."""
        for i in range(GRID_SIZE):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num:
                    return False
        return True

    def solve(self):
        """Solve the board using backtracking."""
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.board[i][j] == 0:
                    nums = list(range(1, GRID_SIZE + 1))
                    random.shuffle(nums)  # Randomize numbers for uniqueness
                    for num in nums:
                        if self.is_valid(i, j, num):
                            self.board[i][j] = num
                            if self.solve():
                                return True
                            self.board[i][j] = 0
                    return False
        return True

    def auto_solve(self):
        """Auto-solve the Sudoku puzzle with animation."""
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.board[i][j] == 0:
                    for num in range(1, GRID_SIZE + 1):
                        if self.is_valid(i, j, num):
                            self.board[i][j] = num
                            self.draw_board()
                            pygame.display.flip()
                            time.sleep(0.05)
                            if self.auto_solve():
                                return True
                            self.board[i][j] = 0
                            self.draw_board()
                            pygame.display.flip()
                            time.sleep(0.05)
                    return False
        return True

    def draw_board(self):
        """Draw the Sudoku board."""
        self.screen.fill(WHITE)

        # Draw grid lines
        for i in range(GRID_SIZE + 1):
            line_width = 3 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH), line_width)
            pygame.draw.line(self.screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), line_width)

        # Draw numbers in the grid
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                num = self.board[row][col]
                if num != 0:
                    color = GRAY if self.solution[row][col] == num else BLUE
                    self.draw_text(str(num), col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2, color)

        # Highlight selected cell
        if self.selected_cell:
            row, col = self.selected_cell
            pygame.draw.rect(self.screen, RED,
                             (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

        # Draw buttons
        pygame.draw.rect(self.screen, GREEN, (50, HEIGHT - 50, 200, 40))
        pygame.draw.rect(self.screen, BLUE, (350, HEIGHT - 50, 200, 40))
        self.draw_text("Auto Solve", 150, HEIGHT - 30, WHITE)
        self.draw_text("New Puzzle", 450, HEIGHT - 30, WHITE)

    def draw_text(self, text, x, y, color, font=FONT):
        """Draw text on the screen."""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def handle_mouse_click(self, pos):
        """Handle clicks for selecting a cell or clicking buttons."""
        if pos[1] < WIDTH:  # Inside the grid
            col, row = pos[0] // CELL_SIZE, pos[1] // CELL_SIZE
            self.selected_cell = (row, col)
        else:  # Below the grid (buttons)
            if 50 <= pos[0] <= 250:  # Auto Solve button
                self.auto_solve()
            elif 350 <= pos[0] <= 550:  # New Puzzle button
                self.generate_board()

    def handle_key_press(self, key):
        """Handle number input for the selected cell."""
        if not self.selected_cell:
            return
        row, col = self.selected_cell
        if pygame.K_1 <= key <= pygame.K_9:
            num = key - pygame.K_0
            if self.is_valid(row, col, num):
                self.board[row][col] = num
        elif key == pygame.K_BACKSPACE:
            self.board[row][col] = 0

    def play(self):
        """Main game loop."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(pygame.mouse.get_pos())
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_press(event.key)

            self.draw_board()
            pygame.display.flip()

        pygame.quit()


# Run the Sudoku game
if __name__ == "__main__":
    Sudoku().play()
