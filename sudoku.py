import tkinter as tk
from tkinter import messagebox
import random

# Function to check if placing num at (row, col) is valid
def is_valid(board, row, col, num):
    # Check the row
    if num in board[row]:
        return False
    
    # Check the column
    for r in range(9):
        if board[r][col] == num:
            return False

    # Check the 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r][c] == num:
                return False

    return True

# Backtracking algorithm to solve the board
def solve(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:  # Empty cell
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve(board):
                            return True
                        board[row][col] = 0  # Reset if no solution
                return False
    return True

# Function to generate a valid Sudoku puzzle
def generate_sudoku():
    board = [[0 for _ in range(9)] for _ in range(9)]

    # Start with a solved puzzle
    solve(board)

    # Remove some numbers to create the puzzle
    for _ in range(random.randint(40, 60)):  # Randomly remove numbers
        row, col = random.randint(0, 8), random.randint(0, 8)
        board[row][col] = 0

    return board

# Function to check if the puzzle is solved
def check_solved(board):
    return all(board[row][col] != 0 for row in range(9) for col in range(9))

# Function to update the GUI based on the board state
def update_board_gui(board, buttons):
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                buttons[i][j].config(text=str(board[i][j]), state=tk.DISABLED, relief=tk.SUNKEN)
            else:
                buttons[i][j].config(text='', state=tk.NORMAL)

# Function to handle user input in the GUI
def on_click(row, col, board, buttons, entry_box, entry_text):
    if board[row][col] == 0:  # Only allow input if the cell is empty
        current_value = entry_text.get()
        if current_value.isdigit() and 1 <= int(current_value) <= 9:
            num = int(current_value)
            if is_valid(board, row, col, num):
                board[row][col] = num
                entry_text.set('')  # Clear input box
                update_board_gui(board, buttons)
                if check_solved(board):
                    messagebox.showinfo("Sudoku", "Congratulations! You solved the puzzle!")
        else:
            messagebox.showwarning("Invalid input", "Please enter a number between 1 and 9.")

# Function to create and show the GUI
def create_gui():
    root = tk.Tk()
    root.title("Sudoku")

    board = generate_sudoku()

    # Create entry widget for user input
    entry_text = tk.StringVar()
    entry_box = tk.Entry(root, textvariable=entry_text, font=("Arial", 18), width=5, justify="center")
    entry_box.grid(row=0, column=9, rowspan=9, padx=10)

    buttons = []
    for i in range(9):
        row_buttons = []
        for j in range(9):
            button = tk.Button(root, text='', font=("Arial", 18), width=5, height=2, command=lambda row=i, col=j: on_click(row, col, board, buttons, entry_box, entry_text))
            button.grid(row=i+1, column=j, padx=5, pady=5)
            row_buttons.append(button)
        buttons.append(row_buttons)

    # Update the board for the first time
    update_board_gui(board, buttons)

    root.mainloop()

# Run the GUI application
if __name__ == "__main__":
    create_gui()
