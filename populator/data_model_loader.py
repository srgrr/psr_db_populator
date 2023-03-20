import logging
import re
from configparser import ConfigParser
from populator.org_archetype import OrgArchetype
from populator.org_pool import OrgPool


def _get_config_parser(filename: str) -> ConfigParser:
    ret = ConfigParser()
    ret.read_file(open(filename, "r"))
    return ret


def _get_org_keys(org_config):
    return [org for org in org_config if re.match(r"[a-z]+-org", org)]


def load_from_root(data_model_root, root: str) -> OrgPool:
    pool = OrgPool()
    org_config = _get_config_parser(f"{data_model_root}/data_model/{root}/org-config.ini")
    for org_archetype in _get_org_keys(org_config):
        logging.debug(f"Processing org archetype {org_archetype}")
        archetype_config = \
            _get_config_parser(f"{data_model_root}/data_model/{root}/{org_archetype}.ini")
        pool.add_org(
            int(org_config.get(org_archetype, "score")),
            OrgArchetype.from_archetype(
                org_archetype,
                archetype_config=archetype_config
            )
        )
    return pool
