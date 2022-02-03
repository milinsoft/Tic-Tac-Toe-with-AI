from players import EasyBot, MediumBot, HardBot, User
from grid import TicTacToeGrid




# terminology:
# i -- row
# j -- column

class TicTacToeGame:
    def __init__(self, player1, player2, grid):
        self.player1 = player1
        self.player2 = player2
        self.grid = grid

        player1.grid = self.grid
        player2.grid = self.grid

        self.curr_player = player1
        self.next_player = player2

        self.state = "In progress"


    @classmethod
    def from_string(cls):
        game_parameters = input("Input command: ")
        if game_parameters not in ("exit",
                                   "start easy user", "start medium user", "start hard user",
                                   "start user easy", "start user medium", "start user hard",
                                   "start user user",
                                   "start easy easy", "start medium medium", "start hard hard"):

            print("Bad parameters!")

            return TicTacToeGame.from_string()
        elif game_parameters == "exit":
            exit()
        else:
            def assigner(player, sign):
                return {"easy": EasyBot(sign), "medium": MediumBot(sign), "user": User(sign)}[player]


            player_1 = assigner(game_parameters.split()[1], "X")

            player_2 = assigner(game_parameters.split()[2], "O")  # because this is the second player

            grid = TicTacToeGrid()



            return cls(player_1, player_2, grid)

    def game_rules_validation(self):
        """ Tic-Tac-Toe game for 2 players. X moves 1st then O.
            The fist who will put own sign 3 time in row, column or horizontally - wins.
            In all cells are occupied and there is no winner - it's a "Draw", game will be over with no winner.
        """
        empty_cells = sum((self.grid.top.count(" "), self.grid.mid.count(" "), self.grid.bot.count(" ")))

        if any([self.grid.top[0] == self.grid.top[1] == self.grid.top[2] != " ",  # top row
                self.grid.mid[0] == self.grid.mid[1] == self.grid.mid[2] != " ",  # middle row
                self.grid.bot[0] == self.grid.bot[1] == self.grid.bot[2] != " ",  # bottom row
                self.grid.top[0] == self.grid.mid[0] == self.grid.bot[0] != " ",  # left column
                self.grid.top[1] == self.grid.mid[1] == self.grid.bot[1] != " ",  # middle column
                self.grid.top[2] == self.grid.mid[2] == self.grid.bot[2] != " ",  # right column
                self.grid.top[2] == self.grid.mid[1] == self.grid.bot[0] != " ",  # main diagonal
                self.grid.top[0] == self.grid.mid[1] == self.grid.bot[2] != " ",  # second diagonal
                ]):
            print(f"{self.curr_player.sign} wins")  # winner
            self.state = "Finished"
            return main()

        elif empty_cells < 1:  # at least 1 move left  # issue is here, DRAW function is not working
            print("Draw")
            self.state = "Draw"
            return main()


    def gameplay(self):
        self.player1.make_move()
        self.game_rules_validation()
        self.switch_player()

        self.player2.make_move()
        self.game_rules_validation()
        self.switch_player()
        # play with "current player to save 2 lines"?


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


    def switch_player(self):
        self.curr_player, self.next_player = self.next_player, self.curr_player

        # try something like if self.curr_player = player1 if self.curr_player == player2 else player 2





def main():

    while True:
        game = TicTacToeGame.from_string()

        game.grid.print_grid()  # print 1st clear grid/field
        while game.state not in frozenset({"Finished", "Draw"}):
            game.gameplay()




def test():
    game = TicTacToeGame.from_string()
    print("Player1 name:", game.player1.name,
          "\nPlayer 1 sign:", game.player1.sign)

    print()

    print("Player2 name:", game.player2.name,
          "\nPlayer 2 sign:", game.player2.sign)

    print("\nInitial Grid:\n")
    game.grid.print_grid()



if __name__ == '__main__':
    main()






