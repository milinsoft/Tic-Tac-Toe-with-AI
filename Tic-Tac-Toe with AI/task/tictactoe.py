from random import choice


# terminology:
# i -- row
# j -- column

class TicTacToe:

    def __init__(self, player1, player2, mode):
        self.curr_player_sign = "X"  # default value as "X" makes the 1st move
        self.next_player_sign = "O"

        self.grid = [[' ', ' ', ' '] for _ in range(3)]
        self.top, self.mid, self.bot = \
            self.grid[0], self.grid[1], self.grid[2]
        self.mode = mode
        self.state = "in process"
        self.player1 = player1
        self.player2 = player2

    @classmethod
    def from_string(cls):
        game_parameters = input("Input command: ")
        if game_parameters not in ("exit",
                                   "start easy user", "start medium user", "start hard user",
                                   "start user easy", "start user medium", "start user hard",
                                   "start user user",
                                   "start easy easy", "start medium medium", "start hard hard"):

            print("Bad parameters!")
            return TicTacToe.from_string()
        elif game_parameters == "exit":
            exit()
        else:
            player_1, player_2 = \
                game_parameters.split()[1], game_parameters.split()[2]

            if player_1 in "easy medium hard":
                mode = player_1
            elif player_2 in "easy medium hard":
                mode = player_2
            else:
                mode = "easy"

            return cls(player_1, player_2, mode)

    def current_state_analyzer(self):
        x_counter = 0
        o_counter = 0

        for i in range(3):
            for n in range(3):
                if self.grid[i][n] == "X":
                    x_counter += 1
                elif self.grid[i][n] == "O":
                    o_counter += 1

        if x_counter > o_counter:
            self.switch_player()
        self.game_rules_validation()

    def print_grid(self):
        print(
            f"{9 * '-'}\n| {' '.join(self.top)} |\n| {' '.join(self.mid)} |\n| {' '.join(self.bot)} |\n{9 * '-'}")  # printing symbols separately so it's possible to have a blankspace between each of three sybmols

    def switch_player(self):
        self.curr_player_sign, self.next_player_sign = self.next_player_sign, self.curr_player_sign

    def user_move(self):

        try:
            row, column = [int(x) - 1 for x in input("Enter the coordinates: ").split()]
            assert self.grid[row][column] not in "XO"
            self.grid[row][column] = self.curr_player_sign
            self.print_grid()

        except ValueError:
            print("You should enter numbers!")
            return self.user_move()

        except IndexError:
            print("Coordinates should be from 1 to 3!")
            return self.user_move()
        except AssertionError:
            print("This cell is occupied! Choose another one!")
            self.user_move()

    def mini_max(self):
        ...


    def computer_move(self):
        def easy():
            steps_set = [(row + 1, cell + 1) for row in range(3) for cell in range(3) if self.grid[row][cell] == " "]
            random_step = choice(steps_set)
            self.grid[random_step[0] - 1][random_step[1] - 1] = self.curr_player_sign
            self.print_grid()
            print("Making move level \"%s\"" % self.mode)

        def medium():
            print("current sign is:", self.curr_player_sign)
            columns = tuple(zip(self.grid[0], self.grid[1], self.grid[2]))
            # diagonals
            d1 = (self.grid[0][2], self.grid[1][1], self.grid[2][0])
            d2 = (self.grid[0][0], self.grid[1][1], self.grid[2][2])
            step = ""

            # win or block strategy

            for i in range(3) or step == "":
                # row win or block
                if any([self.grid[i].count(self.curr_player_sign) == 2, self.grid[i].count(self.next_player_sign) == 2]) and " " in self.grid[i]:
                    step = (i + 1, self.grid[i].index(' ') + 1)

                # column win or block
                elif any([columns[i].count(self.curr_player_sign) == 2, columns[i].count(self.next_player_sign) == 2]) and " " in columns[i]:
                    step = (columns[i].index(' ') + 1, i + 1)

                # diagonal win or block
                elif any([d2.count(self.curr_player_sign) == 2, d2.count(self.next_player_sign) == 2]) and " " in d2:
                    coordinates = {"0": (0+1, 0+1),
                                   "1": (1+1, 1+1),
                                   "2": (2+1, 2+1)}

                    step = coordinates[str(d2.index(" "))]

                elif any([d1.count(self.curr_player_sign) == 2, d1.count(self.next_player_sign) == 2]) and " " in d1:
                    coordinates = {"0": (0+1, 2+1),
                                   "1": (1+1, 1+1),
                                   "2": (2+1, 0+1)}

                    step = coordinates[str(d1.index(" "))]

            if step:
                self.grid[step[0] - 1][step[1] - 1] = self.curr_player_sign
                self.print_grid()
                print("Making move level \"%s\"" % self.mode)
            else:
                easy()

        def hard():
            best_step = ""
            print("current sign is:", self.curr_player_sign)
            columns = tuple(zip(self.grid[0], self.grid[1], self.grid[2]))
            # diagonals
            d1 = (self.grid[0][2], self.grid[1][1], self.grid[2][0])
            d2 = (self.grid[0][0], self.grid[1][1], self.grid[2][2])
            step = ""

            # win or block strategy

            for i in range(3) or step == "":
                # row win or block
                if self.grid[i].count(self.curr_player_sign) == 2 and " " in self.grid[i]:
                    step = (i + 1, self.grid[i].index(' ') + 1)

                # column win or block
                elif columns[i].count(self.curr_player_sign) == 2 and " " in columns[i]:
                    step = (columns[i].index(' ') + 1, i + 1)

                # diagonal win or block
                elif d2.count(self.curr_player_sign) == 2 and " " in d2:
                    coordinates = {"0": (0+1, 0+1),
                                   "1": (1+1, 1+1),
                                   "2": (2+1, 2+1)}

                    step = coordinates[str(d2.index(" "))]

                elif d1.count(self.curr_player_sign) == 2 and " " in d1:
                    coordinates = {"0": (0+1, 2+1),
                                   "1": (1+1, 1+1),
                                   "2": (2+1, 0+1)}

                    step = coordinates[str(d1.index(" "))]

                elif self.grid[i].count(self.next_player_sign) == 2 and " " in self.grid[i]:
                    step = (i + 1, self.grid[i].index(' ') + 1)

                # column win or block
                elif columns[i].count(self.next_player_sign) == 2 and " " in columns[i]:
                    step = (columns[i].index(' ') + 1, i + 1)

                # diagonal win or block
                elif d2.count(self.next_player_sign) == 2 and " " in d2:
                    coordinates = {"0": (0+1, 0+1),
                                   "1": (1+1, 1+1),
                                   "2": (2+1, 2+1)}

                    step = coordinates[str(d2.index(" "))]

                elif d1.count(self.next_player_sign) == 2 and " " in d1:
                    coordinates = {"0": (0+1, 2+1),
                                   "1": (1+1, 1+1),
                                   "2": (2+1, 0+1)}

                    step = coordinates[str(d1.index(" "))]

            if step:
                self.grid[step[0] - 1][step[1] - 1] = self.curr_player_sign
                self.print_grid()
                print("Making move level \"%s\"" % self.mode)
            else:
                easy()



        if self.mode == 'easy':
            easy()
        elif self.mode == 'medium':
            medium()
        else:
            hard()

    def game_rules_validation(self):
        """ Tic-Tac-Toe game for 2 players. X moves 1st then O.
            The fist who will put own sign 3 time in row, column or horizontally - wins.
            In all cells are occupied and there is no winner - it's a "Draw", game will be over with no winner.
        """
        empty_cells = sum((self.top.count(" "), self.mid.count(" "), self.bot.count(" ")))

        if any([self.top[0] == self.top[1] == self.top[2] != " ",  # top row
                self.mid[0] == self.mid[1] == self.mid[2] != " ",  # middle row
                self.bot[0] == self.bot[1] == self.bot[2] != " ",  # bottom row
                self.top[0] == self.mid[0] == self.bot[0] != " ",  # left column
                self.top[1] == self.mid[1] == self.bot[1] != " ",  # middle column
                self.top[2] == self.mid[2] == self.bot[2] != " ",  # right column
                self.top[2] == self.mid[1] == self.bot[0] != " ",  # main diagonal
                self.top[0] == self.mid[1] == self.bot[2] != " ",  # second diagonal
                ]):
            print(f"{self.curr_player_sign} wins")  # winner
            self.state = "Finished"
            return main()

        elif empty_cells < 1:  # at least 1 move left  # issue is here, DRAW function is not working
            print("Draw")
            self.state = "Draw"
            return main()

    def gameplay(self):
        self.user_move() if self.player1 == "user" else self.computer_move()
        self.game_rules_validation()
        self.switch_player()
        self.user_move() if self.player2 == "user" else self.computer_move()
        self.game_rules_validation()
        self.switch_player()
        # play with "current player to save 2 lines"?


# make it @classmethod ?
def main():
    while True:
        game = TicTacToe.from_string()
        game.print_grid()  # print 1st clear grid/field
        while game.state not in frozenset({"Finished", "Draw"}):
            game.gameplay()


if __name__ == '__main__':
    main()
