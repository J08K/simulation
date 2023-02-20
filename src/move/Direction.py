import Common
import random

def calc_direction(x_1 : float, y_1 : float, x_2 : float, y_2 : float) -> tuple[float, float]:
    """ Returns a vector of the difference between two points. """
    return x_2 - x_1, y_2 - y_1

def max_delta_location(max_distance : float, x : float, y : float, maximize : bool = False) -> tuple[float, float]:
    """ Returns a vector of the maximum difference in location, keeping the direction. Does not change the value if the distance of the vector is lower or equal to max distance. """
    direction_vec_distance = Common.calc_distance(0, 0, x, y)
    if direction_vec_distance > max_distance or maximize:
        multiplier = direction_vec_distance / max_distance
        return x * multiplier, y * multiplier
    return x, y

def random_direction() -> tuple[float, float]:
    x = random.random() * (1 if random.random() > 0.5 else -1)
    y = random.random() * (1 if random.random() > 0.5 else -1)
    return x, y