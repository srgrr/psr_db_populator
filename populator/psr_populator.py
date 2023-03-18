import logging
import coloredlogs
import tqdm
# change the random lib name in case you wanna use something else
# (might break stuff tho)
from numpy import random as random
from populator.cli import parse_args


def _configure_logger():
    coloredlogs.install(level="DEBUG")
    args = {
        "level": logging.DEBUG,
        "format": "%(asctime)s %(levelname)-8s %(message)s",
        "datefmt": "%Y-%m-%d %H:%M:%S"
    }
    logging.basicConfig(**args)


def _pretty_cli(cli: dict):
    return ", ".join(f"{k}={v}" for (k, v) in cli.items())


def _get_rng():
    return random


def _set_random_seed(seed):
    logging.debug(f"Setting seed for RNG library {random} to {seed}")
    _get_rng().seed(seed)


def main(**cli):
    logging.debug(f"Invoked PSR Populator with CLI args {_pretty_cli(cli)}")
    _set_random_seed(cli.get("random_seed"))


if __name__ == "__main__":
    _configure_logger()
    args = parse_args()
    main(**vars(args))
