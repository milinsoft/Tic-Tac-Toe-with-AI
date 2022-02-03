
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
        print(
            f"{9 * '-'}\n| {' '.join(self.top)} |\n| {' '.join(self.mid)} |\n| {' '.join(self.bot)} |\n{9 * '-'}")  # printing symbols separately so it's possible to have a blankspace between each of three sybmols



