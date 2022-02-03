from abc import ABC, abstractmethod
from random import choice


class Player(ABC):

    def __init__(self, sign):
        self.name = "Bot"
        self.sign = sign
        self.next_player_sign = "O" if self.sign == "X" else "X"
        super().__init__()



    @abstractmethod
    def make_move(self):
        pass


class EasyBot(Player):
    def __init__(self, sign):
        self.sign = sign
        self.name = "easy"
        self.next_player_sign = "O" if self.sign == "X" else "X"
        # super().__init__(sign)

    def make_move(self):
        steps_set = [(row + 1, cell + 1) for row in range(3) for cell in range(3) if self.grid.grid[row][cell] == " "]
        random_step = choice(steps_set)
        self.grid.grid[random_step[0] - 1][random_step[1] - 1] = self.sign
        self.grid.print_grid()
        print("Making move level \"%s\"" % self.name)


class MediumBot(EasyBot):
    def __init__(self, sign):
        self.name = "medium"
        self.sign = sign
        self.next_player_sign = "O" if self.sign == "X" else "X"

    def make_move(self):

        # print("current sign is:", self.sign)
        columns = tuple(zip(self.grid.grid[0], self.grid.grid[1], self.grid.grid[2]))
        # diagonals
        d1 = (self.grid.grid[0][0], self.grid.grid[1][1], self.grid.grid[2][2])
        d2 = (self.grid.grid[0][2], self.grid.grid[1][1], self.grid.grid[2][0])

        step = ""

        # win or block strategy

        for i in range(3) or step == "":
            # row win or block
            if any([self.grid.grid[i].count(self.sign) == 2,
                    self.grid.grid[i].count(self.next_player_sign) == 2]) and " " in self.grid.grid[i]:
                step = (i + 1, self.grid.grid[i].index(' ') + 1)

            # column win or block
            elif any([columns[i].count(self.sign) == 2,
                      columns[i].count(self.next_player_sign) == 2]) and " " in columns[i]:
                step = (columns[i].index(' ') + 1, i + 1)

            # diagonal win or block
            elif any([d1.count(self.sign) == 2, d1.count(self.next_player_sign) == 2]) and " " in d1:
                coordinates = {"0": (0 + 1, 0 + 1),
                               "1": (1 + 1, 1 + 1),
                               "2": (2 + 1, 2 + 1)}

                step = coordinates[str(d1.index(" "))]

            elif any([d2.count(self.sign) == 2, d2.count(self.next_player_sign) == 2]) and " " in d2:
                coordinates = {"0": (0 + 1, 2 + 1),
                               "1": (1 + 1, 1 + 1),
                               "2": (2 + 1, 0 + 1)}

                step = coordinates[str(d2.index(" "))]

        print("Step is:", step)


        if step:
            self.grid.grid[step[0] - 1][step[1] - 1] = self.sign
            self.grid.print_grid()
            print("Making move level \"%s\"" % self.name)
        else:
            # if algoritm don't find good solution - use the logic of EasyBot.
            super().make_move()



class HardBot:
    pass


class User:

    def __init__(self, sign):
        self.name = "User"
        self.sign = sign


    def make_move(self):

        try:
            row, column = [int(x) - 1 for x in input("Enter the coordinates: ").split()]

            # print(self.grid.grid)

            # grid.grid resolves the issue with subscription
            # exit()

            assert self.grid.grid[row][column] not in "XO"
            self.grid.grid[row][column] = self.sign
            self.grid.print_grid()

        except ValueError:
            print("You should enter numbers!")
            return self.self.make_move()

        except IndexError:
            print("Coordinates should be from 1 to 3!")
            return self.make_move()
        except AssertionError:
            print("This cell is occupied! Choose another one!")
            self.make_move()
