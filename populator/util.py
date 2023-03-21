import subprocess
import os


def key_subset(d: dict, *keys: str) -> dict:
    return {k: d.get(k) for k in keys}


def get_local_ip() -> str:
    return subprocess.check_output(
        ["ipconfig", "getifaddr", "en0"]
    ).decode("utf-8").strip()


def get_pwd() -> str:
    return os.getcwd()


def pretty_cli(cli: dict) -> str:
    return ", ".join(f"{k}={v}" for (k, v) in cli.items())
