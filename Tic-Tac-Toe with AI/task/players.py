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

    def get_game_state(self):
        """ Tic-Tac-Toe game for 2 players. X moves 1st then O.
            The fist who will put own sign 3 time in row, column or horizontally - wins.
            In all cells are occupied and there is no winner - it's a "Draw", game will be over with no winner.
        """

        if [self.sign] * 3 in (
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
