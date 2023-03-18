import logging
import tqdm
from populator.cli import parse_args
from populator.util import set_random_seed


def _pretty_cli(cli: dict):
    return ", ".join(f"{k}={v}" for (k, v) in cli.items())


def main(**cli):
    logging.debug(f"Invoked PSR Populator with CLI args {_pretty_cli(cli)}")
    set_random_seed(cli.get("random_seed"))


if __name__ == "__main__":
    args = parse_args()
    main(**vars(args))
