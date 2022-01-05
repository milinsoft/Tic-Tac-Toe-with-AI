from random import choice


# terminology:
# i -- row
# j -- column

class TicTacToe:

    def __init__(self, player1, player2):
        self.curr_player_sign = "X"  # default value as "X" makes the 1st move
        self.grid = [[' ', ' ', ' '] for _ in range(3)]
        self.top, self.mid, self.bot = \
            self.grid[0], self.grid[1], self.grid[2]
        self.mode = "easy"
        self.state = "in process"
        self.player1 = player1
        self.player2 = player2

    @classmethod
    def from_string(cls):
        game_parameters = input("Input command: ")
        if game_parameters not in ("exit", "start easy user", "start user easy", "start user user", "start easy easy"):
            print("Bad parameters!")
            return TicTacToe.from_string()
        elif game_parameters == "exit":
            exit()
        else:
            player_1, player_2 = \
                game_parameters.split()[1], game_parameters.split()[2]
            return cls(player_1, player_2)

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
        self.curr_player_sign = "O" if self.curr_player_sign == "X" else "X"

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

    def computer_move(self):
        steps_set = [(row + 1, cell + 1) for row in range(3) for cell in range(3) if self.grid[row][cell] == " "]
        random_step = choice(steps_set)
        self.grid[random_step[0] - 1][random_step[1] - 1] = self.curr_player_sign
        self.print_grid()
        print("Making move level \"%s\"" % self.mode)

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
            print(f"{self.curr_player_sign} wins")
            self.state = "Finished"
            return main()

        elif empty_cells < 1:  # at least 1 move left  # issue is here, DRAW function is not working
            print("Draw")
            self.state = "Finished"
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
        while game.state != "Finished":
            game.gameplay()


if __name__ == '__main__':
    main()
