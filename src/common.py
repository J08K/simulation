class Rotation:
    NORTH = 0
    WEST = 1
    SOUTH = 2
    EAST = 3
    
def calc_distance(x_1 : float, y_1 : float, x_2 : float, y_2 : float) -> float:
    return ((x_1 - x_2) ** 2 + (y_1 - y_2) ** 2) ** 0.5