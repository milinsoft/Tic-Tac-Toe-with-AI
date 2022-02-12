# what about creating one file that just run the methods ?

#add players make static
#so players can import game_rule class or something
"""
    def make_move(self):
        if self.game_board == [[' ', ' ', ' '] for _ in range(3)]:  # all cells empty
            return super().make_move()

        move_scores = dict()
        pseudo_game = self.create_sand_game()

        empty_cells_coordinates = [(i, j) for i in range(3) for j in range(3) if self.game_board[i][j] == " "]
        depth = 0

        for move in empty_cells_coordinates:
            pseudo_game.curr_player.occupy_cell(*move)
            status = self.get_game_state()

            # split it for two players?

            if status == "Finished":
                score = 10 if pseudo_game.curr_player.sign == self.sign else -10
                move_scores[move] = (score, depth)

            elif status == "Draw":
                # need to use the most deepest step here (not yet implemented)
                score = 0
                move_scores[move] = (score, depth)

            else:  # game is still in progress
                depth += 1
                pseudo_game.switch_player()
                pseudo_game.curr_player.make_move()

        # re-write sorting!!!
        print(move_scores)
        move_scores = dict(sorted(move_scores.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True))

        return self.occupy_cell(*list(move_scores)[0])  # picking best move

"""



# BUG


"""

Wrong answer in test #2

You should print 'X wins' if X win the game!

Please find below the output of your program during this failed test.
Note that the '>' character indicates the beginning of the input line.

---

Input command: > start user easy
---------
|       |
|       |
|       |
---------
Enter the coordinates: > 2 2
---------
|       |
|   X   |
|       |
---------
Making move level "easy"
---------
|       |
|   X O |
|       |
---------
Enter the coordinates: > 1 1
---------
| X     |
|   X O |
|       |
---------
Making move level "easy"
---------
| X     |
|   X O |
|     O |
---------
Enter the coordinates: > 1 3
---------
| X   X |
|   X O |
|     O |
---------
Making move level "easy"
---------
| X   X |
|   X O |
|   O O |
---------
Enter the coordinates: > 1 2
---------
| X X X |
|   X O |
|   O O |
---------
Making move level "easy"
---------
| X X X |
|   X O |
| O O O |
---------

"""
