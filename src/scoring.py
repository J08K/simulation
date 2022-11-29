import math

def food_score(rel_x : float, rel_y : float, target_nutritional_value : int) -> float:
    distance = math.sqrt( rel_x ** 2 + rel_y ** 2 )
    return target_nutritional_value / distance

def best_food_target(targets : list[tuple[float, float, int]]) -> tuple[float, float]:
    highest_score = 0
    best_target = (0, 0)
    for candidate in targets:
        x, y, nutritional_value = candidate
        score = food_score(x, y, nutritional_value)
        if score > highest_score:
            highest_score = score
            best_target = (x, y)
    return best_target