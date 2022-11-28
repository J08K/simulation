import math

class StandardRotations:
    EAST = 0
    NORTH = math.pi / 2
    WEST = math.pi
    SOUTH = (3 * math.pi) / 2
    BEGIN = EAST

def degrees_to_radians(degrees : float) -> float:
    """Converts degrees to radians

    Args:
        degrees (float): Amount of degrees

    Returns:
        float: Radian angle
    """
    return degrees * ( math.pi / 180 )

def radians_to_slope(radians : float) -> float:
    """Converts radians to a slope

    Args:
        radians (float): Radian angle

    Returns:
        float: Slope
    """
    return math.tan(radians)

def degrees_to_slope(degrees : float) -> float:
    """Converts degrees to a slope

    Args:
        degrees (float): Amount of degrees

    Returns:
        float: Slope
    """
    return radians_to_slope(degrees_to_radians(degrees))

def radians_to_direction_vector(radians : float) -> tuple[float, float]:
    """Converts a radian angle to a direction vector

    Args:
        radians (float): Radian angle

    Returns:
        tuple[float, float]: Direction vector
    """
    match radians:
        case StandardRotations.NORTH:
            return 0.0, 1.0
        case StandardRotations.SOUTH:
            return 0.0, -1.0
        case StandardRotations.EAST:
            return 1.0, 0.0
        case StandardRotations.WEST:
            return -1.0, 0.0
        case _:
            x_vec = -1.0 if StandardRotations.NORTH > radians < StandardRotations.SOUTH else 1.0
            y_vec = radians_to_slope(radians) * x_vec
            return (x_vec, round(y_vec, 3))