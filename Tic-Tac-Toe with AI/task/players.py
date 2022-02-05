from random import choice


class User:

    def __init__(self, sign, game_board):
        self.name = "User"
        self.sign = sign
        self.game_board = game_board
        self.next_player_sign = "O" if self.sign == "X" else "X"

    def occupy_cell(self, row, column):
        self.game_board.grid[row][column] = self.sign
        self.game_board.print_grid()

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
        print("Making move level \"%s\"" % self.name)

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
                print("L82")
                step = (i, self.game_board.grid[i].index(' '))

            # column win or block
            elif any([columns[i].count(self.sign) == 2,
                      columns[i].count(self.next_player_sign) == 2]) and " " in columns[i]:
                print("MAKING STEP: L 87", (columns[i].index(' '), i))
                step = (columns[i].index(' '), i)

            # diagonal win or block
            elif any([d1.count(self.sign) == 2, d1.count(self.next_player_sign) == 2]) and " " in d1:
                coordinates = {"0": (0, 0),
                               "1": (1, 1),
                               "2": (2, 2)}
                print("l96")
                step = coordinates[str(d1.index(" "))]

            elif any([d2.count(self.sign) == 2, d2.count(self.next_player_sign) == 2]) and " " in d2:
                coordinates = {"0": (0, 2),
                               "1": (1, 1),
                               "2": (2, 0)}
                print("L103")
                step = coordinates[str(d2.index(" "))]

        if step:
            self.occupy_cell(*step)
        else:
            # if algoritm don't find good solution - use the logic of EasyBot.
            super().make_move()


class HardBot:
    def __init__(self, sign, game_board):
        super().__init__(sign, game_board)
        self.name = "hard"
        self.sign = sign

    def minimax(self):
        pass

    def make_move(self):
        ...
