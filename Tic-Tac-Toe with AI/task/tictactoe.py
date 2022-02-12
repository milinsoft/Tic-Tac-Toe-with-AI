import re
from players import User, EasyBot, MediumBot, HardBot


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
        self.player1.print_grid()  # print 1st clear self.game_board/field
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
    game.gameplay()


if __name__ == '__main__':
    main()
