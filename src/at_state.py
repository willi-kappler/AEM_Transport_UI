
# Python imports
import logging
import sqlite3
import uuid

# External imports


# Local imports
import at_config


logger = logging.getLogger(__name__)


class ATMainState:
    def __init__(self):
        self.configuration = at_config.ATConfiguration()

    def set_config(self, configuration: at_config.ATConfiguration):
        self.configuration = configuration

    def activate(self):
        self.db = sqlite3.connect(self.configuration.db_filename)

    def check_session(self, cookies: dict[str, str], client_host) -> bool:
        if "session_id" in cookies:
            session_id = cookies["session_id"]

            try:
                uuid_object = uuid.UUID(session_id, version=4)
            except Exception:
                logging.debug(f"Invalid session id (uuid version 4): {session_id}")
                return False

            cursor = self.db.cursor()
            db_res = cursor.execute(f"SELECT ip_hash FROM sessions WHERE uuid = '{session_id}'")
            db_row = db_res.fetchone()
            if db_row is None:
                return False

            # TODO: check for ip or sth. else...

            return True
        else:
            return False

    def get_current_user(self) -> str:
        return "dummy_user"



