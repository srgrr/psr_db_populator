import coloredlogs
import logging


coloredlogs.install(level="DEBUG")
args = {
    "level": logging.DEBUG,
    "format": "%(asctime)s %(levelname)-8s %(message)s",
    "datefmt": "%Y-%m-%d %H:%M:%S"
}
logging.basicConfig(**args)