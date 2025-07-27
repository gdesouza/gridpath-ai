import os

class Area:
    """
    Represents an M x N grid-based area.

    This class provides the foundational data structure for the game map,
    handling the creation of the grid, and any modifications or queries
    related to its cells.

    Attributes:
        _rows (int): The number of rows (M) in the area.
        _cols (int): The number of columns (N) in the area.
        _grid (list[list]): The 2D list representing the grid.
    """
    def __init__(self, M: int, N: int, default_value: any = 0):
        """
        Initializes an Area object of size M x N.

        Args:
            M (int): The number of rows for the grid.
            N (int): The number of columns for the grid.
            default_value (any): The initial value for all cells in the grid.
        
        Raises:
            ValueError: If M or N are not positive integers.
        """
        if not (isinstance(M, int) and M > 0 and isinstance(N, int) and N > 0):
            raise ValueError("Area dimensions M and N must be positive integers.")
        self._rows = M
        self._cols = N
        self._grid = [[default_value for _ in range(N)] for _ in range(M)]

    @property
    def rows(self) -> int:
        """Returns the number of rows in the area."""
        return self._rows

    @property
    def cols(self) -> int:
        """Returns the number of columns in the area."""
        return self._cols

    def set_cell(self, row: int, col: int, value: any):
        """
        Sets the value of a specific cell in the grid.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.
            value (any): The new value to set for the cell.

        Raises:
            IndexError: If the row or col coordinates are out of bounds.
        """
        if not (0 <= row < self._rows and 0 <= col < self._cols):
            raise IndexError("Cell coordinates are out of bounds.")
        self._grid[row][col] = value

    def get_cell(self, row: int, col: int) -> any:
        """
        Retrieves the value of a specific cell from the grid.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.

        Returns:
            The value of the specified cell.

        Raises:
            IndexError: If the row or col coordinates are out of bounds.
        """
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise IndexError("Cell coordinates are out of bounds.")
        return self._grid[row][col]

    @classmethod
    def from_list(cls, grid_list: list[list]):
        """
        Creates an Area object from a pre-existing list of lists.

        This is useful for loading maps from files or using predefined layouts.

        Args:
            grid_list (list[list]): The list of lists to use as the grid.

        Returns:
            An Area object initialized with the provided grid.
        """
        M = len(grid_list)
        N = len(grid_list[0]) if M > 0 else 0
        area = cls(M, N)
        area._grid = grid_list
        return area
