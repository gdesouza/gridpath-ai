# GridPath AI

GridPath AI is a Python application for visualizing and simulating various AI pathfinding and area coverage algorithms on a grid-based map.

## Project Structure

```
gridpath-ai/
├── src/
│   ├── core/
│   │   └── area.py             # Defines the Area class (fundamental data structure)
│   ├── game/
│   │   └── game.py             # Defines the Game class (main game logic, all AI modes, rendering)
│   ├── utils/
│   │   └── map_utils.py        # Contains functions for map generation and loading
│   └── main.py                 # The main application entry point and menu logic
├── maps/                       # Directory for custom map files
├── requirements.txt            # Project dependencies
└── README.md                   # Project description and setup instructions
```

## Setup

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone <repository_url>
    cd gridpath-ai
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

    *Note: If you encounter issues with `tkinter` (e.g., `_tkinter.TclError: no display name and no $DISPLAY environment variable`), you might need to install the `python3-tk` package on Linux:
    ```bash
    sudo apt-get install python3-tk
    ```

## How to Run

To start the GridPath AI application, use the following command from the project root directory (`gridpath-ai/`):

```bash
python -m src.main
```

This will launch the main menu, where you can choose different AI simulations or load custom maps.

## Usage

Follow the on-screen menu prompts to interact with the application:

*   **Manual Control:** Use arrow keys to move the player.
*   **Greedy AI:** An AI that moves towards the exit by choosing the locally optimal path.
*   **A* AI:** An AI that finds the optimal (shortest) path to the exit.
*   **Wall Follower AI:** An AI that explores the map using the left-hand rule.
*   **Frontier Exploration AI:** An AI that explores the map by moving towards the closest unvisited area.
*   **(l)oad map:** Load a custom map from a file in the `maps/` directory.
*   **(n)ew random map:** Generate a new random solvable map.
*   **(e)xit:** Exit the program.

## Custom Maps

You can create your own custom maps. Place them in the `maps/` directory. Map files should be plain text files where:

*   Each character represents a cell.
*   Rows are separated by newlines.
*   Columns can be separated by spaces (e.g., `P . X` or `P.X`).

Example `my_map.txt`:
```
P . X
. X .
X . E
```

Then, you can load it by entering `l` and providing the path `maps/my_map.txt` when prompted.
