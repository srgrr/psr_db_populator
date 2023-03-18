import subprocess
import logging
from numpy import random


def get_rng():
    return random


def set_random_seed(seed: int):
    logging.debug(f"Setting seed for RNG object {random} as {seed}")
    get_rng().seed(seed)


def get_local_ip():
    return subprocess.check_output(
        ["ipconfig", "getifaddr", "en0"]
    ).decode("utf-8").strip()