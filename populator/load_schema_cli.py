import argparse
from argparse import ArgumentParser
from populator.util import get_local_ip

DEFAULT_STR = "Default: %(default)s"


def _add_sch_3x_options(parser: ArgumentParser):
    ver = "(3x only)"
    parser.add_argument(
        "--sch-url",
        type=str,
        default=f"http://{get_local_ip()}:18631",
        help=f"{ver} SCH URL {DEFAULT_STR}"
    )
    parser.add_argument(
        "--sch-username",
        type=str,
        default="admin@admin",
        help=f"{ver} SCH Admin Username {DEFAULT_STR}"
    )
    parser.add_argument(
        "--sch-password",
        type=str,
        default="admin@admin",
        help=f"{ver} SCH Admin Password {DEFAULT_STR}"
    )
    parser.add_argument(
        "--sch-authoring-sdc",
        type=str,
        default=f"http://{get_local_ip()}:18630",
        help=f"{ver} SCH Authoring SDC {DEFAULT_STR}"
    )


def _add_sch_4x_options(parser: ArgumentParser):
    # TODO: ADD IT FOR DATAOPS
    pass


def get_parser() -> ArgumentParser:
    parser = ArgumentParser(
        "Populate SCH from JSON specification"
    )
    parser.add_argument(
        "json_file",
        type=str,
        help="JSON File"
    )
    _add_sch_3x_options(parser)
    _add_sch_4x_options(parser)
    return parser


def parse_args() -> argparse.Namespace:
    return get_parser().parse_args()
