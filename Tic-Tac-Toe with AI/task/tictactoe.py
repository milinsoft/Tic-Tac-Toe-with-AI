from game_board import TicTacToeGameBoard, TestBoard
from random import choice
from copy import copy


class User:

    def __init__(self, sign, game_board):
        self.name = "User"
        self.sign = sign
        self.game_board = game_board
        self.next_player_sign = "O" if self.sign == "X" else "X"

    def occupy_cell(self, row, column):
        self.game_board.grid[row][column] = self.sign

    def make_move(self):
        try:
            row, column = [int(x) - 1 for x in input("Enter the coordinates: ").split()]
            assert self.game_board.grid[row][column] == " "
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


class EasyBot(User):
    def __init__(self, sign, game_board):
        super().__init__(sign, game_board)
        self.sign = sign
        self.name = "easy"

    def occupy_cell(self, j, i):
        super().occupy_cell(j, i)

    def make_move(self):
        steps_set = [(i, j) for i in range(3) for j in range(3) if
                     self.game_board.grid[i][j] == " "]
        random_step = choice(steps_set)
        self.occupy_cell(*random_step)


class MediumBot(EasyBot):
    def __init__(self, sign, game_board):
        super().__init__(sign, game_board)
        self.name = "medium"
        self.sign = sign

    def make_move(self):
        columns = tuple(zip(self.game_board.grid[0], self.game_board.grid[1], self.game_board.grid[2]))
        # diagonals
        d1 = (self.game_board.grid[0][0], self.game_board.grid[1][1], self.game_board.grid[2][2])
        d2 = (self.game_board.grid[0][2], self.game_board.grid[1][1], self.game_board.grid[2][0])
        step = ""

        # win or block strategy
        for i in range(3) or step == "":
            """ i - column number
            self.game_board.grid[i].index(' ') - index of column in row i represented as 2D array."""
            # row win or block
            if any([self.game_board.grid[i].count(self.sign) == 2,
                    self.game_board.grid[i].count(self.next_player_sign) == 2]) and " " in self.game_board.grid[i]:
                step = (i, self.game_board.grid[i].index(' '))

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
        pass

    def create_sand_game(self):
        # creating copy of this game to give to find the best move behind the scean
        sand_board = copy(self.game_board)
        me = HardBot(self.sign, sand_board)
        opponent = HardBot(self.next_player_sign, sand_board)
        return TicTacToeGame(sand_board, me, opponent)

    def make_move(self):
        empty_cells_sum = sum((self.game_board.grid[0].count(" "),
                               self.game_board.grid[1].count(" "),
                               self.game_board.grid[2].count(" "))
                              )

        # if terminal state is not possible (more than 3 cells are empty) - play as MediumBot
        if empty_cells_sum > 500:  # 5 - means at least 4 signs placed
            super().make_move()

        else:
            move_scores = dict()
            # print("Not yet implemented")
            pseudo_game = self.create_sand_game()

            my_sign = self.sign

            empty_cells_coordinates = [(i, j) for i in range(3) for j in range(3) if pseudo_game.game_board.grid[i][j] == " "]

            print("The following cells are empty:", empty_cells_coordinates)
            depth = 0

            for move in empty_cells_coordinates:
                pseudo_game.curr_player.occupy_cell(*move)
                status = pseudo_game.get_game_state()

                # split it for two players?

                if status == "Finished":
                    score = 10 if pseudo_game.curr_player.sign == my_sign else -10
                    move_scores[move] = (score, depth)

                elif status == "Draw":
                    # need to use the most deepest step here (not yet implemented)
                    score = 0
                    move_scores[move] = (score, depth)
                    # return self.occupy_cell(*move)


                else:  # game is still in progress
                    depth += 1
                    pseudo_game.switch_player()
                    pseudo_game.curr_player.make_move()


                print("depth is:", depth)

            move_scores = sorted(move_scores.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)
            print("all steps calculated")
            print(move_scores)


            #move_scores = sorted(move_scores.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)
            best_move = move_scores[0][0]
            return self.occupy_cell(*best_move)
            # exit()


class TicTacToeGame:

    def __init__(self, game_board, player1, player2):
        self.game_board = game_board
        self.player1 = player1
        self.player2 = player2
        self.curr_player = player1
        self.game_state = "In progress"

    @staticmethod
    def add_players(game_board):
        # ideally this function must initilise the game with 3 objects (2 players and 1 self.game_board)

        game_parameters = input("Input command: ")
        if game_parameters not in ("exit",
                                   "start easy user", "start medium user", "start hard user",
                                   "start user easy", "start user medium", "start user hard",
                                   "start user user",
                                   "start easy easy", "start medium medium", "start hard hard"):

            print("Bad parameters!")

            return TicTacToeGame.add_players(game_board)
        elif game_parameters == "exit":
            exit()
        else:
            def assigner(player, sign):
                return {"easy": EasyBot(sign, game_board), "medium": MediumBot(sign, game_board),
                        "hard": HardBot(sign, game_board),
                        "user": User(sign, game_board)}[player]

            player_1 = assigner(game_parameters.split()[1], "X")

            player_2 = assigner(game_parameters.split()[2], "O")  # because this is the second player

            return player_1, player_2

    def get_game_state(self):
        """ Tic-Tac-Toe game for 2 players. X moves 1st then O.
            The fist who will put own sign 3 time in row, column or horizontally - wins.
            In all cells are occupied and there is no winner - it's a "Draw", game will be over with no winner.
        """

        if [self.curr_player.sign] * 3 in (
                self.game_board.grid,  # all three rows
                [self.game_board.grid[0][0], self.game_board.grid[1][0], self.game_board.grid[2][0]],  # left column
                [self.game_board.grid[0][1], self.game_board.grid[1][1], self.game_board.grid[2][1]],  # middle column
                [self.game_board.grid[0][2], self.game_board.grid[1][2], self.game_board.grid[2][2]],  # right column
                [self.game_board.grid[0][2], self.game_board.grid[1][1], self.game_board.grid[2][0]],  # main diagonal
                [self.game_board.grid[0][0], self.game_board.grid[1][1], self.game_board.grid[2][2]],  # second diagonal
        ):
            return "Finished"

        elif not bool(sum((self.game_board.grid[0].count(" "), self.game_board.grid[1].count(" "),
                           self.game_board.grid[2].count(" ")))):
            return "Draw"
        return "In progress"

    def gameplay(self):
        while self.game_state == "In progress":
            self.curr_player.make_move()
            # think how to move it into "players" file and User class
            print("Making move level \"%s\"" % self.curr_player.name) if self.curr_player.name != "User" else ""

            self.game_board.print_grid()
            self.game_state = self.get_game_state()

            if self.game_state == "Finished":
                print(f"{self.curr_player.sign} wins")  # winner
            elif self.game_state == "Draw":
                print("Draw")
            self.switch_player()

    def current_state_analyzer(self):
        x_counter, o_counter = 0, 0
        for j in range(3):
            for i in range(3):
                if self.game_board[j][i] == "X":
                    x_counter += 1
                elif self.game_board[j][i] == "O":
                    o_counter += 1

        if x_counter > o_counter:
            self.switch_player()
        self.get_game_state()

    def switch_player(self):
        self.curr_player = self.player1 if self.curr_player == self.player2 else self.player2


def main():
    game_board = TicTacToeGameBoard()

    # game_board = TestBoard()

    player1, player2 = TicTacToeGame.add_players(game_board)
    game = TicTacToeGame(game_board, player1, player2)

    # game = TicTacToeGame(game_board, HardBot("X", game_board), HardBot("O", game_board))

    # game = TicTacToeGame(game_board, User("X", game_board), User("O", game_board))
    game.game_board.print_grid()  # print 1st clear self.game_board/field
    game.gameplay()


if __name__ == '__main__':
    main()


# can remove board as an object of TicTacToeGame class and access through players
