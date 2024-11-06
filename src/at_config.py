

import json
import logging


logger = logging.getLogger(__name__)


class ATConfiguration:
    def __init__(self):
        self.db_filename = "at_transport.db"
        self.port = 5000

    def from_file(self, filename: str):
        logger.debug(f"Load configuration from file: {filename}.")

        with open(filename, "r") as f:
            data = json.load(f)

        if "db_filename" in data:
            self.db_filename = data["db_filename"]

        if "port" in data:
            self.port = int(data["port"])
            assert (self.port >= 0 and self.port <= 65535), f"Port must be in range 0-65535: {self.port}"




