import argparse
from populator.util import get_pwd


DEFAULT_STR = "Default: %(default)s"


def get_parser():
    parser = argparse.ArgumentParser(
        "PSR DB populator"
    )
    parser.add_argument(
        "--random-seed",
        type=int,
        default=19071990,
        help=f"Random seed {DEFAULT_STR}"
    )
    parser.add_argument(
        "--num-orgs",
        type=int,
        default=10,
        help=f"Num orgs {DEFAULT_STR}"
    )
    parser.add_argument(
        "--use-sample-schema",
        action="store_true",
        help=f"Use a smaller schema instead of the real one for testing purposes {DEFAULT_STR}"
    )
    parser.add_argument(
        "--data-model-root",
        type=str,
        default=get_pwd(),
        help=f"Root for data model files {DEFAULT_STR}"
    )

    return parser


def parse_args() -> argparse.Namespace:
    return get_parser().parse_args()