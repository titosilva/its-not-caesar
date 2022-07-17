class Position:
    row: int
    col: int
    depth: int

    def __init__(self, row: int, col: int, depth: int = 0) -> None:
        self.row = row
        self.col = col
        self.depth = depth
