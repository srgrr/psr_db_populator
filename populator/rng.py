import logging
import string
from numpy import random


def get_rng() -> random:
    return random


def set_random_seed(seed: int):
    logging.debug(f"Setting seed for RNG object {random} as {seed}")
    get_rng().seed(seed)


def random_integer(lo: int, hi: int) -> int:
    assert lo <= hi, f"lo must be <= hi, received {locals()}"
    return random.randint(lo, hi)


def choice(a: list):
    assert a, f"Array '{a}' must not be empty or None"
    return a[random_integer(0, len(a))]


def random_string(length: int = 5) -> str:
    assert length > 0, f"String length must be positive"
    return "".join(string.ascii_lowercase[random_integer(0, 25)] for _ in range(length))
