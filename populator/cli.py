import argparse
from populator.util import get_local_ip


DEFAULT_STR = "Default: %(default)s"


def _add_sch_3x_options(parser):
    parser.add_argument(
        "--sch-url",
        type=str,
        default=f"http://{get_local_ip()}:18631",
        help=f"SCH URL {DEFAULT_STR}"
    )
    parser.add_argument(
        "--sch-username",
        type=str,
        default="admin@admin",
        help=f"SCH Admin Username {DEFAULT_STR}"
    )
    parser.add_argument(
        "--sch-password",
        type=str,
        default="admin@admin",
        help=f"SCH Admin Password {DEFAULT_STR}"
    )
    parser.add_argument(
        "--sch-authoring-sdc",
        type=str,
        default=f"http://{get_local_ip()}:18630",
        help=f"SCH Authoring SDC {DEFAULT_STR}"
    )
    parser.add_argument(
        "--use-sample-schema",
        action="store_true",
        help=f"Use a smaller schema instead of the real one for testing purposes {DEFAULT_STR}"
    )


def _add_sch_4x_options(parser):
    # TODO: ADD IT FOR DATAOPS
    pass


def get_basic_parser():
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

    _add_sch_3x_options(parser)
    _add_sch_4x_options(parser)

    return parser


def parse_args():
    return get_basic_parser().parse_args()