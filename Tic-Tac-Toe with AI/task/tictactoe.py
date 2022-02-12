import re
from copy import copy
from random import choice


class User:

    def __init__(self, sign, game_board):
        self.name = "User"  # need this field for print the message Making move level
        self.sign = sign
        self.game_board = game_board
        self.next_player_sign = "O" if self.sign == "X" else "X"

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
        return None

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
                    self.game_board[i].count(self.next_player_sign) == 2]) and " " in self.game_board[i]:
                step = (i, self.game_board[i].index(' '))

            # column win or block
            elif any([columns[i].count(self.sign) == 2,
                      columns[i].count(self.next_player_sign) == 2]) and " " in columns[i]:
                step = (columns[i].index(' '), i)

            # diagonal win or block
            elif any([d1.count(self.sign) == 2, d1.count(self.next_player_sign) == 2]) and " " in d1:
                coordinates = {"0": (0, 0),
                               "1": (1, 1),
                               "2": (2, 2)}
                step = coordinates[str(d1.index(" "))]

            elif any([d2.count(self.sign) == 2, d2.count(self.next_player_sign) == 2]) and " " in d2:
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

    def minimax(self):
        move_scores = dict()
        scores = {self.sign: 10, self.next_player_sign: -10, "Draw": 0}
        pseudo_game = self.create_sand_game()

        empty_cells_coordinates = [(i, j) for i in range(3) for j in range(3) if self.game_board[i][j] == " "]
        depth = 0

        for move in empty_cells_coordinates:
            pseudo_game.curr_player.occupy_cell(*move)
            winner = self.get_winner()

            # split it for two players?
            if winner:
                move_scores[move] = (scores[winner], depth)

            else:  # game is still in progress
                depth += 1
                pseudo_game.switch_player()
                pseudo_game.curr_player.make_move()

            # re-write sorting!!!
        move_scores = dict(sorted(move_scores.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True))

        return list(move_scores)[0]



    def create_sand_game(self):
        # creating copy of this game to give to find the best move behind the scean
        sand_board = copy(self.game_board)
        me = HardBot(self.sign, sand_board)

        me.game_board = sand_board
        opponent = HardBot(self.next_player_sign, sand_board)

        opponent.game_board = sand_board
        return TicTacToeGame(me, opponent)

    def make_move(self):
        if self.game_board == [[' ', ' ', ' '] for _ in range(3)]:  # all cells empty
            return super().make_move()

        best_move = self.minimax()
        return self.occupy_cell(*best_move)  # picking best move


class TicTacToeGame:

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.curr_player = player1
        self.winner = None

    def switch_player(self):
        self.curr_player = self.player1 if self.curr_player == self.player2 else self.player2

    @classmethod
    def add_players(cls):
        game_board = [[' ', ' ', ' '] for _ in range(3)]
        
        template = re.compile("exit|start( (user|easy|medium|hard)){2}")
        game_parameters = input("Input command: ")

        if not re.match(template, game_parameters):
            print("Bad parameters!")
            return TicTacToeGame.add_players()

        elif game_parameters == "exit":
            exit()
        else:
            game_parameters = game_parameters.split()
            modes = {"easy": EasyBot, "medium": MediumBot, "hard": HardBot, "user": User}
            return cls(modes[game_parameters[1]]("X", game_board),
                       modes[game_parameters[2]]("O", game_board))

    def gameplay(self):
        while not self.winner:
            self.curr_player.make_move()
            # think how to move it into "players" file and User class
            print("Making move level \"%s\"" % self.curr_player.name) if self.curr_player.name != "User" else ""
            self.curr_player.print_grid()
            self.winner = self.curr_player.get_winner()

            if self.winner:
                print("Draw" if self.winner == "Draw" else f"{self.curr_player.sign} wins")
            else:
                self.switch_player()


def main():
    game = TicTacToeGame.add_players()
    game.player1.print_grid()  # print 1st clear self.game_board/field
    game.gameplay()

if __name__ == '__main__':
    main()

