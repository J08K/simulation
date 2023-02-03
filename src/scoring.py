import math
import itertools
import Common


def food_score(rel_x: float, rel_y: float, target_nutritional_value: int) -> float:
    distance = math.sqrt(rel_x**2 + rel_y**2)
    return target_nutritional_value / distance


def best_food_target(targets: list[tuple[float, float, int]]) -> tuple[float, float]:
    highest_score = 0
    best_target = (0, 0)
    for x, y, nutritional_value in targets:
        score = food_score(x, y, nutritional_value)
        if score > highest_score:
            highest_score = score
            best_target = (x, y)
    return best_target


def avg_delta_distance(rel_target_locations: list[tuple[float, float]]) -> float:
    """Calculate the average change in distance of target entity from current entity."""
    distances = [Common.calc_distance(0.0, 0.0, *idx) for idx in rel_target_locations]
    deltas = [second - first for first, second in itertools.pairwise(distances)]
    return Common.avg(deltas)


def max_delta_distance(rel_target_locations: list[tuple[float, float]]) -> float:
    """Calculate the maximum distance a target entity can travel."""
    traveled_distances = [
        Common.calc_distance(*first, *second)
        for first, second in itertools.pairwise(rel_target_locations)
    ]
    return max(traveled_distances)


# TODO Add algorythm that calculates entities best option.
