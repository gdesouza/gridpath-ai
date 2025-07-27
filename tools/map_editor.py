# map_editor.py
import tkinter as tk
from tkinter import filedialog, messagebox
import os

class MapEditor:
    """A graphical tool to create and save game maps."""
    def __init__(self, root, rows=20, cols=30):
        self.root = root
        self.rows = rows
        self.cols = cols
        
        self.tile_types = ['.', 'X', 'P', 'E']
        self.colors = {'.': 'lightgray', 'X': '#34495e', 'P': '#3498db', 'E': '#2ecc71'}
        self.current_tile = 'X' # Start with painting walls

        self.root.title("GridPath Map Editor")

        # --- UI Elements ---
        controls_frame = tk.Frame(root, padx=10, pady=10)
        controls_frame.pack(side=tk.TOP, fill=tk.X)

        # Tile selection buttons
        for tile in self.tile_types:
            if tile == '.': continue # No button for floor, use right-click
            b = tk.Button(controls_frame, text=f"Paint '{tile}'", bg=self.colors[tile], fg='white',
                          command=lambda t=tile: self.set_current_tile(t))
            b.pack(side=tk.LEFT, padx=5)
        
        # Action buttons
        tk.Button(controls_frame, text="Save Map", command=self.save_map).pack(side=tk.RIGHT, padx=5)
        tk.Button(controls_frame, text="Clear Map", command=self.clear_map).pack(side=tk.RIGHT)

        # Canvas for the grid
        self.cell_size = 25
        canvas_width = cols * self.cell_size
        canvas_height = rows * self.cell_size
        self.canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
        self.canvas.pack(padx=10, pady=10)

        # --- Grid Data & Drawing ---
        self.grid_data = [['.' for _ in range(cols)] for _ in range(rows)]
        self.grid_rects = [[None for _ in range(cols)] for _ in range(rows)]
        self.draw_grid()

        # --- Bindings ---
        self.canvas.bind('<B1-Motion>', self.paint_tile) # Drag left-click
        self.canvas.bind('<Button-1>', self.paint_tile)   # Single left-click
        self.canvas.bind('<B3-Motion>', self.erase_tile) # Drag right-click
        self.canvas.bind('<Button-3>', self.erase_tile)   # Single right-click

    def set_current_tile(self, tile):
        self.current_tile = tile
        print(f"Selected tile type: {self.current_tile}")

    def draw_grid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                x1, y1 = c * self.cell_size, r * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                color = self.colors[self.grid_data[r][c]]
                self.grid_rects[r][c] = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')

    def paint_tile(self, event):
        self._update_tile(event, self.current_tile)

    def erase_tile(self, event):
        self._update_tile(event, '.')

    def _update_tile(self, event, tile_type):
        c = event.x // self.cell_size
        r = event.y // self.cell_size
        if 0 <= r < self.rows and 0 <= c < self.cols:
            # Prevent multiple 'P' or 'E'
            if tile_type in ['P', 'E']:
                self._clear_existing_tile(tile_type)
            
            self.grid_data[r][c] = tile_type
            self.canvas.itemconfig(self.grid_rects[r][c], fill=self.colors[tile_type])

    def _clear_existing_tile(self, tile_to_clear):
        """Finds and removes any existing instance of a unique tile (P or E)."""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid_data[r][c] == tile_to_clear:
                    self.grid_data[r][c] = '.'
                    self.canvas.itemconfig(self.grid_rects[r][c], fill=self.colors['.'])
                    return

    def clear_map(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid_data[r][c] = '.'
                self.canvas.itemconfig(self.grid_rects[r][c], fill=self.colors['.'])

    def save_map(self):
        # Validate map has one 'P' and one 'E'
        flat_list = [item for sublist in self.grid_data for item in sublist]
        if flat_list.count('P') != 1 or flat_list.count('E') != 1:
            messagebox.showerror("Invalid Map", "Map must contain exactly one Player ('P') and one Exit ('E').")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".map",
            filetypes=[("Map Files", "*.map"), ("All Files", "*.*")],
            title="Save Map As..."
        )
        if not filepath:
            return # User cancelled

        try:
            with open(filepath, 'w') as f:
                for r in range(self.rows):
                    f.write(" ".join(self.grid_data[r]) + "\n")
            messagebox.showinfo("Success", f"Map saved successfully to:\n{os.path.basename(filepath)}")
        except IOError as e:
            messagebox.showerror("Error", f"Failed to save map: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MapEditor(root)
    root.mainloop()