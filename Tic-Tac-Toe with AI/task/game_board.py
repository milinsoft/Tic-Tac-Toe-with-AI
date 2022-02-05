class TicTacToeGameBoard:

    def __init__(self):
        self.grid = [[' ', ' ', ' '] for _ in range(3)]


    def print_grid(self):
        line = 9 * '-'
        print(f"{line}\n"
              f"| {' '.join(self.grid[0])} |\n"
              f"| {' '.join(self.grid[1])} |\n"
              f"| {' '.join(self.grid[2])} |\n"
              f"{line}"
              )  # printing symbols separately so it's possible to have a blankspace between each of three sybmols
