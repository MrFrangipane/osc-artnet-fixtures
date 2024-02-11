import math


def map_to_int(input_: float, min_: int = 0, max_: int = 255) -> int:
    return int(min_ + (max_ - min_) * min(1., (max(0., input_))))


def p_cos(value):
    return math.cos(value) * .5 + .5
