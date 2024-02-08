import random

class PuzzleGame:
    def __init__(self, board_size=8):
        self.board_size = board_size
        self.board = [[0 for _ in range(board_size)] for _ in range(board_size)]

    def display_board(self):
        # Print column indices
        print("  " + " ".join(map(str, range(self.board_size))))
        
        for i, row in enumerate(self.board):
            # Print row index
            print(f"{i} ", end="")
            
            # Print board cells
            for cell in row:
                print("X" if cell == 1 else " ", end=" ")
            print()

    def clear_full_rows(self, full_rows):
        for row_index in full_rows:
            # Clear the entire row
            self.board[row_index] = [0] * self.board_size

    def clear_full_cols(self, full_cols):
        for col_index in full_cols:
            # Check if the column is already empty
            if all(row[col_index] == 0 for row in self.board):
                continue
            
            # Clear the column
            for i in range(self.board_size):
                self.board[i][col_index] = 0

    def check_full_rows(self):
        full_rows = []
        for i in range(self.board_size):
            if all(cell == 1 for cell in self.board[i]):
                full_rows.append(i)
        return full_rows
    
    def check_full_cols(self):
        full_cols = []
        for j in range(self.board_size):
            if all(row[j] == 1 for row in self.board):
                full_cols.append(j)
        return full_cols


class Puzzle:
    def __init__(self, shape):
        self.shape = shape


class PuzzleSolver:
    def __init__(self, game_board):
        self.game_board = game_board

    def place_puzzle(self, puzzle, row, col):
        if row + len(puzzle.shape) > len(self.game_board) or col + len(puzzle.shape[0]) > len(self.game_board[0]):
            return False  # Puzzle would be placed out of bounds
        for r in range(len(puzzle.shape)):
            for c in range(len(puzzle.shape[0])):
                if puzzle.shape[r][c] == 1:
                    if self.game_board[row + r][col + c] == 1:
                        return False  # Puzzle overlaps with existing filled cells
                    self.game_board[row + r][col + c] = 1
        return True  # Puzzle successfully placed

# Main game logic
def play_game():
    puzzle_game = PuzzleGame()
    puzzle_solver = PuzzleSolver(puzzle_game.board)
    puzzle_options_set = set()
    
    while True:
        print("\nCurrent board state:")
        puzzle_game.display_board()
        
        # Define puzzle options
        puzzle_options = [
            Puzzle([[1], [1]]),
            Puzzle([[1,1], [1,1]]),
            Puzzle([[1,1,1], [0,0,1], [0,0,1]]),
            Puzzle([[1,1,1], [1,0,0], [1,0,0]]),
            Puzzle([[0,1], [1,1], [0,1]]),
            Puzzle([[1,0], [1,1], [1,0]]),
            Puzzle([[1,1,1,1,1]]),
            Puzzle([[1], [1], [1], [1]]),
            Puzzle([[1,1], [1,0]]),
            Puzzle([[1,0,0], [1,1,1]]),
            Puzzle([[0,1,0], [1,1,1]]),
            Puzzle([[1,1,1]]),
            Puzzle([[1,1]]),
            Puzzle([[1,1,1,1]]),
            Puzzle([[1,1,1],[1,1,1], [1,1,1]]),
            Puzzle([[1,0,0],[0,1,0], [0,0,1]]),
            Puzzle([[0,0,1],[0,1,0], [1,0,0]])
        ]
        
        # Generate new puzzle options if set is empty
        if not puzzle_options_set:
            puzzle_options_set = set(random.sample(puzzle_options, 3))
        
        # Select three random puzzle options from the set
        selected_puzzles = random.sample(list(puzzle_options_set), min(3, len(puzzle_options_set)))


        print("\nChoose a puzzle to place:")
        for i, puzzle in enumerate(selected_puzzles):
            print(f"{i}:")
            for row in puzzle.shape:
                print(" ".join(map(str, row)))
        
        # Get user input for puzzle selection and position
        while True:
            try:
                puzzle_index = int(input("Enter the index of the puzzle (0-2): "))
                if puzzle_index not in range(3):
                    raise ValueError("Invalid input. Please enter a valid index.")
                
                row = int(input("Enter the row index to place the puzzle (0-7): "))
                col = int(input("Enter the column index to place the puzzle (0-7): "))
                
                if row not in range(8) or col not in range(8):
                    raise ValueError("Invalid input. Please enter valid indices.")
                
                if not puzzle_solver.place_puzzle(selected_puzzles[puzzle_index], row, col):
                    print("Selected puzzle overlaps with existing filled cells or would be placed out of bounds. Please select again.")
                    continue
                
                # Remove placed puzzle from set
                puzzle_options_set.remove(selected_puzzles[puzzle_index])
                
                # Check for and clear full rows and columns
                full_rows = puzzle_game.check_full_rows()
                full_cols = puzzle_game.check_full_cols()
                puzzle_game.clear_full_rows(full_rows)
                puzzle_game.clear_full_cols(full_cols)
                
                break  # Exit the loop if puzzle successfully placed and full rows/cols cleared
                
            except ValueError as e:
                print(e)
        
        # If all puzzles are placed, generate new options
        if not puzzle_options_set:
            print("All puzzles placed. Generating new options.")

# Run the game
play_game()
