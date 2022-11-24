from typing import overload

def calc_best_flee_vector(rel_predator_pos : list[tuple[int, int]]) -> tuple[int, int]:
    
    total_predators = len(rel_predator_pos)
    
    x_predators, y_predators = zip(*rel_predator_pos)
    x_avg_predators = sum(x_predators) / total_predators
    y_avg_predators = sum(y_predators) / total_predators
    
    return -x_avg_predators, -y_avg_predators

@overload 
def normalize_vector(vec_x : int, vec_y : int) -> tuple[int, int]:
    divisor = abs(1 / vec_x)
    return vec_x * divisor, vec_y * divisor

@overload
def normalize_vector(vec : tuple[int, int]) -> tuple[int, int]:
    x, y = 
    divisor = abs(1 / )