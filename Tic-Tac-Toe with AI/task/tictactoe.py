from game_board import TicTacToeGameBoard
from players import EasyBot, MediumBot, User


class TicTacToeGame:

    def __init__(self, game_board, player1, player2):
        self.game_board = game_board
        self.player1 = player1
        self.player2 = player2
        self.curr_player = player1
        self.game_state = "In progress"

    @staticmethod
    def add_players(game_game_board):
        # ideally this function must initilise the game with 3 objects (2 players and 1 self.game_board)

        game_parameters = input("Input command: ")
        if game_parameters not in ("exit",
                                   "start easy user", "start medium user", "start hard user",
                                   "start user easy", "start user medium", "start user hard",
                                   "start user user",
                                   "start easy easy", "start medium medium", "start hard hard"):

            print("Bad parameters!")

            return TicTacToeGame.add_players(game_game_board)
        elif game_parameters == "exit":
            exit()
        else:
            def assigner(player, sign):
                return {"easy": EasyBot(sign, game_game_board), "medium": MediumBot(sign, game_game_board),
                        "user": User(sign, game_game_board)}[player]

            player_1 = assigner(game_parameters.split()[1], "X")

            player_2 = assigner(game_parameters.split()[2], "O")  # because this is the second player

            return player_1, player_2

    def game_rules_validation(self):
        """ Tic-Tac-Toe game for 2 players. X moves 1st then O.
            The fist who will put own sign 3 time in row, column or horizontally - wins.
            In all cells are occupied and there is no winner - it's a "Draw", game will be over with no winner.
        """

        # try self.curr_player.sign * 3 in [ list of combinations] -> bool

        """ format [row][column], where column is a cell number in row"""

        if any([self.game_board.top[0] == self.game_board.top[1] == self.game_board.top[2] != " ",  # top row
                self.game_board.mid[0] == self.game_board.mid[1] == self.game_board.mid[2] != " ",  # middle row
                self.game_board.bot[0] == self.game_board.bot[1] == self.game_board.bot[2] != " ",  # bottom row
                self.game_board.top[0] == self.game_board.mid[0] == self.game_board.bot[0] != " ",  # left column
                self.game_board.top[1] == self.game_board.mid[1] == self.game_board.bot[1] != " ",  # middle column
                self.game_board.top[2] == self.game_board.mid[2] == self.game_board.bot[2] != " ",  # right column
                self.game_board.top[2] == self.game_board.mid[1] == self.game_board.bot[0] != " ",  # main diagonal
                self.game_board.top[0] == self.game_board.mid[1] == self.game_board.bot[2] != " ",  # second diagonal
                ]):
            print(f"{self.curr_player.sign} wins")  # winner
            self.game_state = "Finished"

            return main()

        elif not bool(sum((self.game_board.top.count(" "), self.game_board.mid.count(" "), self.game_board.bot.count(" ")))):
            print("Draw")
            self.game_state = "Draw"
            return main()

    def gameplay(self):

        self.player1.make_move()
        self.game_rules_validation()
        self.switch_player()
        self.player2.make_move()
        self.game_rules_validation()
        self.switch_player()

    def current_state_analyzer(self):

        # terminology: i -- row, j -- column

        x_counter, o_counter = 0, 0

        for j in range(3):
            for i in range(3):
                if self.game_board[j][i] == "X":
                    x_counter += 1
                elif self.game_board[j][i] == "O":
                    o_counter += 1

        if x_counter > o_counter:
            self.switch_player()
        self.game_rules_validation()

    def switch_player(self):
        self.curr_player = self.player1 if self.curr_player == self.player2 else self.player2


def main():
    game_board = TicTacToeGameBoard()

    player1, player2 = TicTacToeGame.add_players(game_board)

    game = TicTacToeGame(game_board, player1, player2)

    while True:

        game.game_board.print_grid()  # print 1st clear self.game_board/field
        while game.game_state not in frozenset({"Finished", "Draw"}):
            game.gameplay()


if __name__ == '__main__':
    main()
