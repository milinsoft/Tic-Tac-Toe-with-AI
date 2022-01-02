# write your code here
class TicTacToe:

    def __init__(self, grid):
        self.curr_player_sign = "X"  # default value as "X" makes the 1st move
        # self.grid = [['_', '_', '_'] for _ in range(3)]
        self.grid = [grid[0:3], grid[3:6], grid[6:9]]
        self.top, self.mid, self.bot = \
            self.grid[0], self.grid[1], self.grid[2]

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
            row, column = [int(x) - 1 for x in input("Enter the coordinates:").split()]
            if self.grid[row][column] in "XO":
                print("This cell is occupied! Choose another one!")
                self.user_move()
            else:
                self.grid[row][column] = self.curr_player_sign
                self.print_grid()
        except ValueError:
            print("You should enter numbers!")
            return self.user_move()
        except IndexError:
            print("Coordinates should be from 1 to 3!")
            return self.user_move()

    def game_rules_validation(self):
        """ Tic-Tac-Toe game for 2 players. X moves 1st then O.
            The fist who will put own sign 3 time in row, column or horizontally - wins.
            In all cells are occupied and there is no winner - it's a "Draw", game will be over with no winner.
        """
        empty_cells = sum((self.top.count("_"), self.mid.count("_"), self.bot.count("_")))

        if any([self.top[0] == self.top[1] == self.top[2] != "_",  # top row
                self.mid[0] == self.mid[1] == self.mid[2] != "_",  # middle row
                self.bot[0] == self.bot[1] == self.bot[2] != "_",  # bottom row
                self.top[0] == self.mid[0] == self.bot[0] != "_",  # left column
                self.top[1] == self.mid[1] == self.bot[1] != "_",  # middle column
                self.top[2] == self.mid[2] == self.bot[2] != "_",  # right column
                self.top[2] == self.mid[1] == self.bot[0] != "_",  # main diagonal
                self.top[0] == self.mid[1] == self.bot[2] != "_",  # second diagonal
                ]):
            print(f"{self.curr_player_sign} wins")
            exit()

        elif empty_cells < 1:  # at least 1 move left  # issue is here, DRAW function is not working
            print("Draw")
            exit()
        else:
            print("Game not finished")


if __name__ == '__main__':
    game_grid = [x for x in input("Enter the cells: ")]
    game = TicTacToe(game_grid)
    game.print_grid()  # print 1st clear grid/field
    game.current_state_analyzer()

    while True:
        game.user_move()
        game.game_rules_validation()
        game.switch_player()
