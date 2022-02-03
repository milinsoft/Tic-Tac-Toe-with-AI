class TicTacToeGrid:

    def __init__(self):
        self.grid = [[' ', ' ', ' '] for _ in range(3)]
        self.state = "in process"

    @property
    def top(self):
        return self.grid[0]

    @property
    def mid(self):
        return self.grid[1]

    @property
    def bot(self):
        return self.grid[2]

    def print_grid(self):
        line = 9 * '-'
        print(f"{line}\n"
              f"| {' '.join(self.top)} |\n"
              f"| {' '.join(self.mid)} |\n"
              f"| {' '.join(self.bot)} |\n"
              f"{line}"
              )  # printing symbols separately so it's possible to have a blankspace between each of three sybmols
