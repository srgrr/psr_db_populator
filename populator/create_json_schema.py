import logging
import json
from populator.cli import create_json_parse_args
from populator.org_pool import OrgPool
from populator.rng import set_random_seed
from populator.data_model_loader import load_from_root


def _pretty_cli(cli: dict):
    return ", ".join(f"{k}={v}" for (k, v) in cli.items())


def _get_org_pool_from_data_model(data_model_root: str, use_sample_schema: bool) -> OrgPool:
    root = "example" if use_sample_schema else "schema"
    return load_from_root(data_model_root, root)


def main(random_seed, data_model_root, num_orgs, use_sample_schema):
    logging.debug(f"Invoked PSR Create JSON Schema tool with CLI args {_pretty_cli(locals())}")
    set_random_seed(random_seed)
    org_pool = _get_org_pool_from_data_model(data_model_root, use_sample_schema)

    summary_json = []

    for _ in range(num_orgs):
        chosen_archetype = org_pool.pick_org()
        logging.debug(f"Choosing org archetype {chosen_archetype.archetype_name}")
        summary_json.append(
            chosen_archetype.get_specific_instance()
        )


if __name__ == "__main__":
    args = create_json_parse_args()
    main(**vars(args))
