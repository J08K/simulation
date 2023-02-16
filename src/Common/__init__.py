from Common import Rotation, Species, Genomes
import math

__all__ = [
    "Rotation",
    "Species",
    "Genomes",
]

__version__ = "0.0.1"


def calc_distance(x_1: float, y_1: float, x_2: float, y_2: float) -> float:
    return math.sqrt((x_1 - x_2) ** 2 + (y_1 - y_2) ** 2)


def fixed_size_string(input_text: str, str_length: int) -> str:
    if len(input_text) > str_length:
        return input_text[:str_length]
    elif len(input_text) < str_length:
        return input_text + " " * (str_length - len(input_text))
    else:
        return input_text


def clamp(min_n: int, max_n: int, n: int) -> int:
    n = max(n, min_n)
    n = min(n, max_n)
    return n


def avg(values: list[float]) -> float:
    return sum(values) / len(values)


def cycle_names(start_name : str, spacer : str, clean_start : bool, start_num : int = 2) -> str:
    if clean_start:
        yield start_name
    idx = start_num
    while True:
        yield start_name + spacer + str(idx)
        idx += 1