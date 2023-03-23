import logging
import json
from populator.load_schema_cli import parse_args
from populator.util import pretty_cli
from streamsets.sdk import ControlHub
from streamsets.sdk.sch_models import Organization


def _get_sdk_version():
    from streamsets import sdk
    return sdk.__version__


def _get_sch(sch_url: str, sch_username: str, sch_password: str) -> ControlHub:
    # TODO: ADAPT IT SO WE ALSO SUPPORT 4X
    return ControlHub(sch_url, sch_username, sch_password)


def _get_org_object_from_repr(sch, org_repr: dict) -> Organization:
    org_name = org_repr.get("org_name")
    return sch.get_organization_builder().build(id=org_name,
                                                name=org_name,
                                                admin_user_id=f'admin@{org_name}',
                                                admin_user_display_name=f'{org_name} Admin',
                                                admin_user_email_address='fake@example.com')


def main(
    json_file: str,
    sch_url: str,
    sch_username: str,
    sch_password: str,
    sch_authoring_sdc: str
):
    logging.debug(f"Using StreamSets SDK Version {_get_sdk_version()}")
    logging.debug(f"Invoked PSR Load Schema to SCH tool with CLI args {pretty_cli(locals())}")
    admin_sch = _get_sch(sch_url, sch_username, sch_password)
    for org_repr in json.load(open(json_file, "r")):
        org_name = org_repr.get('org_name')
        logging.debug(f"Processing org {org_repr.get('org_name')}")
        org = _get_org_object_from_repr(admin_sch, org_repr)
        logging.debug(f"Adding org obtained from repr: {org}")
        admin_sch.add_organization(org)
        logging.debug(f"Added Org {org_name} to SCH")
        org_sch = _get_sch(sch_url, f"admin@{org_name}", f"admin@{org_name}")
        logging.debug(f"Obtained org SCH accessor {org_sch}")
        logging.debug(f"Available SDCs for current org are {org_sch.data_collectors}")


if __name__ == "__main__":
    args = parse_args()
    main(**vars(args))
