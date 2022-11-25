from typing import overload
import math

def calc_best_flee_vector(rel_predator_pos : list[tuple[float, float]]) -> tuple[float, float]:
    
    total_predators = len(rel_predator_pos)
    
    x_predators, y_predators = zip(*rel_predator_pos)
    x_avg_predators = sum(x_predators) / total_predators
    y_avg_predators = sum(y_predators) / total_predators
    
    return -x_avg_predators, -y_avg_predators


def normalize_vector(vec : tuple[float, float]) -> tuple[float, float]:
    
    # Keeps the shape of the vector, but makes it so that x will be 1 or -1.
    
    x, y = vec
    divisor = abs(1 / x)
    return x * divisor, y * divisor

def maximize_vector(vec : tuple[float, float], max_range : float) -> tuple[float, float]:
    x_val, y_val = vec
    # TODO Test if the fast inverse square root algorithm can work here.
    xy_modifier = ((x_val ** 2 + y_val ** 2) / max_range ** 2) ** -0.5
    return (x_val * xy_modifier, y_val * xy_modifier)