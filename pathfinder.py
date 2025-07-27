import sys

class Area:
    """
    Represents an M x N area using a list of lists.

    Attributes:
        rows (int): The number of rows (M) in the area.
        cols (int): The number of columns (N) in the area.
    """

    def __init__(self, M: int, N: int, default_value: any = 0):
        """
        Initializes an M x N area.

        Args:
            M (int): The number of rows.
            N (int): The number of columns.
            default_value (any, optional): The initial value for each cell. Defaults to 0.
        """
        if not (isinstance(M, int) and M > 0 and isinstance(N, int) and N > 0):
            raise ValueError("Area dimensions M and N must be positive integers.")

        self._rows = M
        self._cols = N
        # Create the M x N grid using a list comprehension
        self._grid = [[default_value for _ in range(N)] for _ in range(M)]

    @property
    def rows(self) -> int:
        """Returns the number of rows (M)."""
        return self._rows

    @property
    def cols(self) -> int:
        """Returns the number of columns (N)."""
        return self._cols

    def set_cell(self, row: int, col: int, value: any):
        """
        Sets the value of a specific cell.

        Args:
            row (int): The row index.
            col (int): The column index.
            value (any): The new value for the cell.
        
        Raises:
            IndexError: If the row or col is out of the area's bounds.
        """
        if not (0 <= row < self._rows and 0 <= col < self._cols):
            raise IndexError("Cell coordinates are out of bounds.")
        self._grid[row][col] = value

    def get_cell(self, row: int, col: int) -> any:
        """
        Retrieves the value of a specific cell.

        Args:
            row (int): The row index.
            col (int): The column index.

        Returns:
            The value of the cell at the specified coordinates.
            
        Raises:
            IndexError: If the row or col is out of the area's bounds.
        """
        if not (0 <= row < self._rows and 0 <= col < self._cols):
            raise IndexError("Cell coordinates are out of bounds.")
        return self._grid[row][col]

    def __str__(self) -> str:
        """
        Returns a string representation of the area for printing.
        """
        # Build a string where each cell is separated by a space
        return "\n".join(" ".join(map(str, row)) for row in self._grid)

# --- Main execution block to demonstrate usage ---
if __name__ == "__main__":
    try:
        # 1. Create a 5x10 area, initializing all cells with a '.' character
        print("## Creating a 5x10 Area ##")
        game_map = Area(M=5, N=10, default_value='.')
        print(f"Successfully created a {game_map.rows}x{game_map.cols} area.\n")
        print(game_map)
        print("-" * 20)

        # 2. Modify the area by placing objects
        print("## Modifying the Area ##")
        print("Placing Player 'P', Exit 'E', and Obstacle 'X'...")
        game_map.set_cell(row=2, col=1, value='P')
        game_map.set_cell(row=4, col=8, value='E')
        game_map.set_cell(row=2, col=5, value='X')
        game_map.set_cell(row=2, col=6, value='X')
        print("\nUpdated area:")
        print(game_map)
        print("-" * 20)

        # 3. Retrieve the value from a specific cell
        print("## Accessing a Cell ##")
        player_pos_value = game_map.get_cell(row=2, col=1)
        print(f"Value at cell (2, 1) is: '{player_pos_value}'")

    except (ValueError, IndexError) as e:
        print(f"\nAn error occurred: {e}", file=sys.stderr)