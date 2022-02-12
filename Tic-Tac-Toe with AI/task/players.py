from copy import copy
from random import choice


class User:

    def __init__(self, sign, game_board):
        self.name = "User"  # need this field for print the message Making move level
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

    # or better "get winner?" replace game_state with - winner , default None
    def get_winner(self):
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
        line = 9 * '-'
        print(f"{line}\n"
              f"| {' '.join(self.game_board[0])} |\n"
              f"| {' '.join(self.game_board[1])} |\n"
              f"| {' '.join(self.game_board[2])} |\n"
              f"{line}"
              )  # printing symbols separately so it's possible to have a blankspace between each of three sybmols


class EasyBot(User):
    def __init__(self, sign, game_board):
        super().__init__(sign, game_board)
        self.name = "easy"
        self.sign = sign

    def make_move(self):
        steps_set = [(i, j) for i in range(3) for j in range(3) if
                     self.game_board[i][j] == " "]
        random_step = choice(steps_set)
        self.occupy_cell(*random_step)


class MediumBot(EasyBot):
    def __init__(self, sign, game_board):
        super().__init__(sign, game_board)
        self.name = "medium"
        self.sign = sign

    def make_move(self):
        if self.game_board == [[' ', ' ', ' '] for _ in range(3)]:  # all cells empty
            return super().make_move()

        columns = tuple(zip(self.game_board[0], self.game_board[1], self.game_board[2]))
        # diagonals
        d1 = (self.game_board[0][0], self.game_board[1][1], self.game_board[2][2])
        d2 = (self.game_board[0][2], self.game_board[1][1], self.game_board[2][0])
        step = ""

        # win or block strategy
        for i in range(3) or step == "":
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

            # diagonal win or block
            elif any([d1.count(self.sign) == 2, d1.count(self.opponent_sign) == 2]) and " " in d1:
                coordinates = {"0": (0, 0),
                               "1": (1, 1),
                               "2": (2, 2)}
                step = coordinates[str(d1.index(" "))]

            elif any([d2.count(self.sign) == 2, d2.count(self.opponent_sign) == 2]) and " " in d2:
                coordinates = {"0": (0, 2),
                               "1": (1, 1),
                               "2": (2, 0)}
                step = coordinates[str(d2.index(" "))]

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

    def minimax(self) -> tuple:
        original_board = self.game_board
        fake_board = copy(original_board)

        fake_player1 = HardBot(self.sign, fake_board)
        fake_player2 = HardBot(self.opponent_sign, fake_board)

        current_player = fake_player1

        move_scores = dict()
        scores = {self.sign: 10, self.opponent_sign: -10, "Draw": 0}
        # pseudo_game = self.create_sand_game()

        empty_cells_coordinates = [(i, j) for i in range(3) for j in range(3) if self.game_board[i][j] == " "]
        depth = 0

        for move in empty_cells_coordinates:
            current_player.occupy_cell(*move)
            winner = self.get_winner()
            # split it for two players?

            if winner:
                move_scores[move] = (scores[winner], depth)

            else:  # game is still in progress
                depth += 1
                current_player = fake_player2 if current_player == fake_player1 else fake_player1
                # important step, as otherwise next player will not seek for the best move
                # but will start from the next availiable which will destroy the algorithm
                current_player.make_move()

        move_scores = dict(sorted(move_scores.items(), key=lambda x: (x[1][0], -x[1][1]), reverse=True))  # sorting putting highest score and lowest depth first
        return list(move_scores)[0]

    def make_move(self):
        if self.game_board == [[' ', ' ', ' '] for _ in range(3)]:  # all cells empty
            return super().make_move()
        best_move = self.minimax()
        return self.occupy_cell(*best_move)  # picking best move
