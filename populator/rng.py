import logging
import string
from numpy import random


def get_rng():
    return random


def set_random_seed(seed: int):
    logging.debug(f"Setting seed for RNG object {random} as {seed}")
    get_rng().seed(seed)


def random_integer(lo: int, hi: int) -> int:
    assert lo <= hi, f"lo must be <= hi, received {locals()}"
    return random.randint(lo, hi)


def random_string(length=5):
    assert length > 0, f"String length must be positive"
    return "".join(string.ascii_lowercase[random_integer(0, 25)] for _ in range(length))
