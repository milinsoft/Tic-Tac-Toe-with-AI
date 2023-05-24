import re

from game_board import GameBoard
from players import EasyBot, HardBot, MediumBot, User


class TicTacToeGame:
    """Represents a Tic-Tac-Toe game."""

    def __init__(self, player1, player2):
        """
        Initializes a TicTacToeGame object.

        Args:
            player1 (Player): The first player.
            player2 (Player): The second player.
        """
        self.player1 = self.curr_player = player1
        self.player2 = player2

    def switch_player(self):
        """
        Switches the current player to the next player.
        """
        self.curr_player = self.player1 if self.curr_player == self.player2 else self.player2

    @classmethod
    def add_players(cls):
        """
        Prompts the user to add players and returns a TicTacToeGame object.

        Returns:
            TicTacToeGame: The created TicTacToeGame object.
        """
        template = re.compile('exit|start( (user|easy|medium|hard)){2}')

        if not template.match(game_parameters := input('Input command: ')):
            print('Bad parameters!')
            return cls.add_players()
        elif game_parameters == 'exit':
            exit()
        player1, player2 = (
            {'easy': EasyBot, 'medium': MediumBot, 'hard': HardBot, 'user': User}[player_type]
            for player_type in game_parameters.split()[1:]
        )
        game_board = GameBoard()
        return cls(player1('X', game_board), player2('O', game_board))

    def start_game(self):
        """
        Starts the Tic-Tac-Toe game.
        """
        print(self.curr_player.game_board)

        while True:
            self.curr_player.make_move()
            if self.curr_player.name:
                print(f"Making move level '{self.curr_player.name}'")
            print(self.curr_player.game_board)
            if winner := self.curr_player.game_board.get_winner():
                print('Draw' if winner == 'Draw' else f'{winner} wins')
                break
            else:
                self.switch_player()


if __name__ == '__main__':
    game = TicTacToeGame.add_players()
    game.start_game()
