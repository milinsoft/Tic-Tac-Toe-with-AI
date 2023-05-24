class GameBoard:
    def __init__(self):
        self.board = [[' ', ' ', ' '] for _ in range(3)]

    @property
    def empty_cells(self):
        """
        Returns a list of empty cells on the game board.

        Returns:
            list: A list of empty cells as tuples (row, column).
        """
        return [(row, col) for row in range(3) for col in range(3) if self.board[row][col] == ' ']

    def get_winner(self) -> str:
        """
        Checks if the player has won or if there is a draw.

        Returns:
            str: The winner sign ('X', 'O') or 'Draw' if it's a draw.
        """

        for sign in ('X', 'O'):
            if [sign] * 3 in self.lines_to_check():
                return sign

        if not any(' ' in line for line in self.lines_to_check()):
            return 'Draw'
        return ''

    def lines_to_check(self):
        """
        Returns the lines (rows, columns, and diagonals) to check for a win.

        Returns:
            tuple: A tuple containing the lines to check.
        """
        rows = (row for row in self.board)
        columns = ((self.board[i][j] for i in range(3)) for j in range(3))
        diagonals = ((self.board[i][i] for i in range(3)), (self.board[i][2 - i] for i in range(3)))

        return (*rows, *columns, *diagonals)

    def __str__(self):
        """
        Returns the string representation of the current game board.
        """
        hr = '-' * 9  # horizontal_line (shortcut like in HTML)
        rows = (f"| {' '.join(row)} |" for row in self.board)
        board_str = '\n'.join(rows)
        return f'{hr}\n{board_str}\n{hr}'

    def is_clear(self):
        """
        Checks if any moves were already made.

        Returns:
            bool: True if the game board is clear, False otherwise.
        """
        return self.board == [[' ', ' ', ' '] for _ in range(3)]

    def occupy_cell(self, row, column, sign):
        """
        Occupies a cell on the game board with the player's sign.

        Args:
            row (int): The row index of the cell.
            column (int): The column index of the cell.
            sign (str): The player's sign ('X' or 'O').
        """
        assert sign in ('X', 'O'), "Acceptable values 'X', 'O'"
        self.board[row][column] = sign
