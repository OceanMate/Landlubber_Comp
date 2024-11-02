class GridManager:
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        
        # Initialize the grid to be 0 and size grid_width x grid_height
        self.grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

    # Check if a rectangle of rect_width x rect_height can be placed at x, y
    def can_place_rectangle(self, x, y, rect_width, rect_height):
        if x + rect_width > self.grid_width or y + rect_height > self.grid_height:
            return False
        for i in range(y, y + rect_height):
            for j in range(x, x + rect_width):
                if self.grid[i][j] != 0:
                    return False
        return True

    # "Place" a rectangle of rect_width x rect_height at x, y (set all values in the rectangle to 1 not actually place anything)
    def place_rectangle(self, x, y, rect_width, rect_height):
        for i in range(y, y + rect_height):
            for j in range(x, x + rect_width):
                self.grid[i][j] = 1

    # Find the next available space to place a rectangle of rect_width x rect_height
    def find_next_available_space(self, rect_width, rect_height):
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.can_place_rectangle(x, y, rect_width, rect_height):
                    return (x, y)
        return (-1, -1)