
# Python imports
import sqlite3

# External imports


# Local imports
import at_config


class ATMainState:
    def __init__(self):
        self.configuration = at_config.ATConfiguration()

    def set_config(self, configuration: at_config.ATConfiguration):
        self.configuration = configuration

    def activate(self):
        self.db = sqlite3.connect(self.configuration.db_filename)

    def check_session(self, cookies: dict[str, str]) -> bool:
        return False


