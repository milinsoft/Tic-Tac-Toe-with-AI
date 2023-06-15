from random import choice


class User:
    """Represents a user player in the Tic-Tac-Toe game."""

    def __init__(self, sign, game_board):
        """
        Initializes a User object.

        Args:
            sign (str): The sign ('X' or 'O') of the player.
            game_board (list): The game board as a 2D list.
        """
        self.name = None
        self.sign = sign
        self.game_board = game_board
        self.opponent_sign = 'O' if self.sign == 'X' else 'X'

    def make_move(self):
        """
        Prompts the user to enter the coordinates and makes a move on the game board.
        """
        try:
            row, column = [int(x) - 1 for x in input('Enter the coordinates: ').split()]
            assert self.game_board.board[row][column] == ' '
            if any([row < 0, row > 2, column < 0, column > 2]):
                raise IndexError

        except ValueError:
            print('You should enter numbers from 1 to 3!')
            return self.make_move()

        except IndexError:
            print('Coordinates should be from 1 to 3!')
            return self.make_move()

        except AssertionError:
            print('This cell is occupied! Choose another one!')
            self.make_move()
        else:
            self.game_board.occupy_cell(row, column, self.sign)


class EasyBot(User):
    """Represents an easy-level bot player in the Tic-Tac-Toe game."""

    def __init__(self, sign, game_board):
        """
        Initializes an EasyBot object.

        Args:
            sign (str): The sign ('X' or 'O') of the player.
            game_board (list): The game board as a 2D list.
        """
        super().__init__(sign, game_board)
        self.name = 'easy'
        self.sign = sign

    def make_move(self):
        """
        Makes a random move on an empty cell.
        """
        return self.game_board.occupy_cell(*choice(self.game_board.empty_cells), self.sign)


class MediumBot(EasyBot):
    """Represents a medium-level bot player in the Tic-Tac-Toe game."""

    def __init__(self, sign, game_board):
        """
        Initializes a MediumBot object.

        Args:
            sign (str): The sign ('X' or 'O') of the player.
            game_board (list): The game board as a 2D list.
        """
        super().__init__(sign, game_board)
        self.name = 'medium'
        self.sign = sign

    def scan_lines(self) -> tuple:
        """
        Scans the lines to check for an opportunity to win or block the opponent.

        Returns:
            tuple: The row and column indices of the move if an opportunity is found, False otherwise.
        """
        for line in self.game_board.lines_to_check():
            # this check makes sense only in when one of the players put 2 signs in a line or diagonal
            line_symbols = set(line)
            if len(line_symbols) == 2 and ' ' in line_symbols:
                empty_cell_index = line.index(' ')
                if line in self.game_board.board:  # row
                    return self.game_board.board.index(line), empty_cell_index
                elif line in [self.game_board.board[i][empty_cell_index] for i in range(3)]:  # column
                    return empty_cell_index, [self.game_board.board[i][empty_cell_index] for i in range(3)].index(line)
        return ()

    def make_move(self):
        """
        Makes a move based on opportunities to win or block the opponent.
        If no opportunity is found, makes a random move on an empty cell.
        """
        # todo potential refactor
        position = self.scan_lines()
        if position:
            self.game_board.occupy_cell(*position, self.sign)
        else:
            super().make_move()


class HardBot(MediumBot):
    """Represents a hard-level bot player in the Tic-Tac-Toe game."""

    def __init__(self, sign, game_board):
        """
        Initializes a HardBot object.

        Args:
            sign (str): The sign ('X' or 'O') of the player.
            game_board (list): The game board as a 2D list.
        """
        super().__init__(sign, game_board)
        self.name = 'hard'
        self.sign = sign

    def minimax(self, depth, is_maximizing, max_player_sign, min_player_sign) -> int:
        """
        Minimax algorithm with depth.

        Args:
            depth (int): The current depth of the algorithm.
            is_maximizing (bool): Whether it's a maximizing or minimizing step.
            max_player_sign (str): The sign of the maximizing player.
            min_player_sign (str): The sign of the minimizing player.

        Returns:
            int: The score of the best move.
        """

        # check winner
        if winner := self.game_board.get_winner():
            return {max_player_sign: 10 - depth, min_player_sign: depth - 10, 'Draw': 0}[winner]

        best_score = float('-inf') if is_maximizing else float('inf')

        for row, col in self.game_board.empty_cells:
            # Make a move
            self.game_board.board[row][col] = max_player_sign if is_maximizing else min_player_sign

            # Recursively call minimax for the next level
            score = self.minimax(depth + 1, not is_maximizing, max_player_sign, min_player_sign)

            # Undo the move
            self.game_board.board[row][col] = ' '

            # Update the best score and depth
            best_score = max(score, best_score) if is_maximizing else min(score, best_score)

        return best_score

    def make_move(self):
        """
        Makes a move based on the minimax algorithm with depth.
        """

        # skip minimax algorithm at the very beginning for performance reasons
        if self.game_board.is_clear():
            return super().make_move()

        min_player_sign = 'X' if self.sign == 'O' else 'O'
        best_score = float('-inf')
        best_move = None

        for move in self.game_board.empty_cells:
            self.game_board.board[move[0]][move[1]] = self.sign
            score = self.minimax(0, False, self.sign, min_player_sign)
            self.game_board.board[move[0]][move[1]] = ' '

            if score > best_score:
                best_score = score
                best_move = move
        return self.game_board.occupy_cell(*best_move, self.sign)
