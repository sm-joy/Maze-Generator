import random

class Cell:
    def __init__(self, pRow, pCol):
        """
        Initialize a cell with its row and column.

        Args:
            pRow (int): Row index of the cell.
            pCol (int): Column index of the cell.
        """
        self.walls = {
            "top": True,
            "bottom": True,
            "left": True,
            "right": True,
        }
        self.visited = False
        self.row, self.col = pRow, pCol

    def __str__(self):
        """
        Return a string representation of the cell.

        Returns:
            str: String representation of the cell.
        """
        return f"Cell(row={self.row}, col={self.col}, walls={self.walls}, visited={self.visited})"

    def checkNeighbors(self, pCells: list[list['Cell']], pRows: int, pCols: int) -> (int, int):
        """
        Check neighboring cells that have not been visited.

        Args:
            pCells (list): 2D list of Cell objects representing the grid of cells.
            pRows (int): Number of rows in the grid.
            pCols (int): Number of columns in the grid.

        Returns:
            tuple: Row and column indices of the neighboring cell (or (-1, -1) if no unvisited neighbors).
        """
        neighbors = []
        if self.row - 1 >= 0 and not pCells[self.row - 1][self.col].visited:  # Top
            neighbors.append((self.row - 1, self.col))

        if self.row + 1 < pRows and not pCells[self.row + 1][self.col].visited:  # Bottom
            neighbors.append((self.row + 1, self.col))

        if self.col - 1 >= 0 and not pCells[self.row][self.col - 1].visited:  # Left
            neighbors.append((self.row, self.col - 1))

        if self.col + 1 < pCols and not pCells[self.row][self.col + 1].visited:  # Right
            neighbors.append((self.row, self.col + 1))

        random.shuffle(neighbors)
        return neighbors[0] if neighbors else (-1, -1)

    def removeWall(self, pSide: str) -> None:
        """
        Remove a wall of the cell.

        Args:
            pSide (str): Side of the wall to be removed ('top', 'bottom', 'left', 'right').
        """
        self.walls[pSide] = False
