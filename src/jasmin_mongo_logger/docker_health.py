import logging
import os
import sys
from enum import Enum
from pathlib import Path

DOCKER_HEATH_FILE = Path("/tmp/docker_health")

print(f"DOCKER_HEATH_FILE: {DOCKER_HEATH_FILE.absolute()}")


class HeathStates(str, Enum):
    STARTING = "starting"
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"

    @classmethod
    def all_states(cls) -> list["HeathStates"]:
        return [HeathStates.STARTING, HeathStates.HEALTHY, HeathStates.UNHEALTHY]

    @classmethod
    def good_states(cls) -> list["HeathStates"]:
        return [HeathStates.HEALTHY]

    @classmethod
    def bad_states(cls) -> list["HeathStates"]:
        return [HeathStates.STARTING, HeathStates.UNHEALTHY]


def set_health(health: HeathStates):
    logging.info(f"Setting Docker health to {health}")
    with open(DOCKER_HEATH_FILE, "w") as f:
        f.write(health.value)
    logging.debug(f"Written {health.value} to {DOCKER_HEATH_FILE.absolute()}")


def get_health() -> HeathStates:
    logging.info("Getting Docker health")
    try:
        with open(DOCKER_HEATH_FILE, "r") as f:
            health = f.read()
        logging.debug(f"Read {health} from {DOCKER_HEATH_FILE.absolute()}")
        return HeathStates(health)
    except FileNotFoundError:
        logging.debug(f"File {DOCKER_HEATH_FILE.absolute()} not found")
        return HeathStates.STARTING


def unset_health():
    logging.info("Unsetting Docker health")
    try:
        os.remove(DOCKER_HEATH_FILE)
        logging.debug(f"Removed {DOCKER_HEATH_FILE.absolute()}")
    except FileNotFoundError:
        logging.debug(f"File {DOCKER_HEATH_FILE.absolute()} not found")


if __name__ == '__main__':
    current_health = get_health()
    print(current_health)
    if current_health in HeathStates.good_states():
        sys.exit(0)
    sys.exit(1)
