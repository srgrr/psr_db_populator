import subprocess


def get_local_ip():
    return subprocess.check_output(
        ["ipconfig", "getifaddr", "en0"]
    ).decode("utf-8").strip()