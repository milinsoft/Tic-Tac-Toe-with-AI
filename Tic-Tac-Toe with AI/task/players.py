from copy import copy
from random import choice

EMPTYBOARD = [[' ', ' ', ' '] for _ in range(3)]


class User:

    def __init__(self, sign, game_board):
        self.name = None  # need this field for print the message Making move level
        self.sign = sign
        self.game_board = game_board
        self.opponent_sign = "O" if self.sign == "X" else "X"

    def occupy_cell(self, row, column):
        self.game_board[row][column] = self.sign

    def make_move(self):
        try:
            row, column = [int(x) - 1 for x in input("Enter the coordinates: ").split()]
            assert self.game_board[row][column] == " "
            if any([row < 0, row > 2, column < 0, column > 2]):
                raise IndexError

        except ValueError:
            print("You should enter numbers from 1 to 3!")
            return self.make_move()

        except IndexError:
            print("Coordinates should be from 1 to 3!")
            return self.make_move()

        except AssertionError:
            print("This cell is occupied! Choose another one!")
            self.make_move()

        else:
            self.occupy_cell(row, column)

    def get_winner(self) -> str:
        """ Tic-Tac-Toe game for 2 players. X moves 1st then O.
            The fist who will put own sign 3 time in row, column or horizontally - wins.
            In all cells are occupied and there is no winner - it's a "Draw", game will be over with no winner.
        """

        if [self.sign] * 3 in (
                self.game_board[0], self.game_board[1], self.game_board[2],  # all three rows
                [self.game_board[0][0], self.game_board[1][0], self.game_board[2][0]],  # left column
                [self.game_board[0][1], self.game_board[1][1], self.game_board[2][1]],  # middle column
                [self.game_board[0][2], self.game_board[1][2], self.game_board[2][2]],  # right column
                [self.game_board[0][2], self.game_board[1][1], self.game_board[2][0]],  # main diagonal
                [self.game_board[0][0], self.game_board[1][1], self.game_board[2][2]],  # second diagonal
        ):
            return self.sign

        elif not bool(sum((self.game_board[0].count(" "), self.game_board[1].count(" "),
                           self.game_board[2].count(" ")))):
            return "Draw"

    def print_grid(self):
        print(f"{9 * '-'}\n"
              f"| {' '.join(self.game_board[0])} |\n"
              f"| {' '.join(self.game_board[1])} |\n"
              f"| {' '.join(self.game_board[2])} |\n"
              f"{9 * '-'}"
              )  # printing symbols separately so it's possible to have a blankspace between each of three sybmols


class EasyBot(User):
    def __init__(self, sign, game_board):
        super().__init__(sign, game_board)
        self.name = "easy"
        self.sign = sign

    def make_move(self):
        steps_set = [(i, j) for i in range(3) for j in range(3) if self.game_board[i][j] == " "]
        random_step = choice(steps_set)
        self.occupy_cell(*random_step)


class MediumBot(EasyBot):
    def __init__(self, sign, game_board):
        super().__init__(sign, game_board)
        self.name = "medium"
        self.sign = sign

    def scan_diagonals(self) -> tuple:
        diagonals = (
            ((0, 0), (1, 1), (2, 2)),
            ((0, 2), (1, 1), (2, 0)),
        )

        for diagonal in diagonals:
            diagonal_symbols = [self.game_board[c[0]][c[1]] for c in diagonal]
            if any([diagonal_symbols.count(self.sign) == 2, diagonal_symbols.count(self.opponent_sign) == 2]) and " " in diagonal_symbols:
                empty_cell = diagonal_symbols.index(' ')
                return diagonal[empty_cell]
        return tuple()

    def make_move(self):
        if self.game_board == EMPTYBOARD:  # all cells empty
            return super().make_move()

        # diagonal win or block
        step = self.scan_diagonals()  # trying to scan diagonals first to avoid the loop

        if step == tuple():
            columns = tuple(zip(self.game_board[0], self.game_board[1], self.game_board[2]))
        # win or block strategy
            for i in range(3):
                """ i - column number
                self.game_board[i].index(' ') - index of column in row i represented as 2D array."""
                # row win or block
                if any([self.game_board[i].count(self.sign) == 2,
                        self.game_board[i].count(self.opponent_sign) == 2]) and " " in self.game_board[i]:
                    step = (i, self.game_board[i].index(' '))

                # column win or block
                elif any([columns[i].count(self.sign) == 2,
                          columns[i].count(self.opponent_sign) == 2]) and " " in columns[i]:
                    step = (columns[i].index(' '), i)
                if step:
                    break

        if step:
            self.occupy_cell(*step)
        else:
            # if algoritm don't find good solution - use the logic of EasyBot.
            super().make_move()


class HardBot(MediumBot):
    def __init__(self, sign, game_board):
        super().__init__(sign, game_board)
        self.name = "hard"
        self.sign = sign

    def minimax(self, depth) -> tuple:
        move_scores = dict()

        fake_board = copy(self.game_board)
        simulated_player1, simulated_player2 =\
            HardBot(self.sign, fake_board), HardBot(self.opponent_sign, fake_board)

        scores = {self.sign: 10, "Draw": 0}  # -10 removed as it makes no sense in this realisation

        current_player = simulated_player1
        empty_cells_coordinates = [(i, j) for i in range(3) for j in range(3) if self.game_board[i][j] == " "]

        for move in empty_cells_coordinates:
            current_player.occupy_cell(*move)
            winner = self.get_winner()
            if winner:
                move_scores[move] = (scores[winner], depth)
            else:
                current_player = simulated_player2 if current_player == simulated_player1 else simulated_player1
                depth += 1
                current_player.make_move(depth)

        # sorting putting highest score and lowest depth first
        move_scores = dict(sorted(move_scores.items(), key=lambda x: (x[1][0], -x[1][1]), reverse=True))
        return list(move_scores)[0]

    def make_move(self, depth=0):
        if self.game_board == EMPTYBOARD:  # all cells empty
            return super().make_move()

        best_move = self.minimax(depth)
        return self.occupy_cell(*best_move)  # picking best move
