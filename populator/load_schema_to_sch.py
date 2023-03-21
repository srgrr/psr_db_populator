import logging
import tqdm
from populator.load_schema_cli import parse_args
from populator.util import pretty_cli
from streamsets import sdk


def main(
    json_file: str,
    sch_url: str,
    sch_username: str,
    sch_password: str,
    sch_authoring_sdc: str
):
    logging.debug(f"Using StreamSets SDK Version {sdk.__version__}")
    logging.debug(f"Invoked PSR Load Schema to SCH tool with CLI args {pretty_cli(locals())}")
    pass


if __name__ == "__main__":
    args = parse_args()
    main(**vars(args))
