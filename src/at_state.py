
# Python imports
import logging
import sqlite3
import uuid
from typing import Optional
from hashlib import blake2b


# Local imports
import at_config


logger = logging.getLogger(__name__)

class ATMainState:
    def __init__(self):
        self.configuration = at_config.ATConfiguration()
        logger.info("ATMainState init")

    def set_config(self, configuration: at_config.ATConfiguration):
        self.configuration = configuration
        logger.debug("Configuration was set")

    def activate(self):
        self.db = sqlite3.connect(self.configuration.db_filename)
        logger.debug("Database was loaded")

    def get_current_user(self, browser_id: str) -> Optional[str]:
        cursor = self.db.cursor()
        db_res = cursor.execute(f"SELECT user_id FROM sessions WHERE uuid = '{browser_id}'")
        db_row = db_res.fetchone()
        if db_row is None:
            logger.debug(f"Session not found: {browser_id}")
            return None

        user_id = db_row[0]

        db_res = cursor.execute(f"SELECT login FROM users WHERE id = '{user_id}'")
        db_row = db_res.fetchone()
        if db_row is None:
            logger.debug(f"User id not found: {user_id}")
            return None

        username = db_row[0]

        logger.debug(f"Found user: {username} for session: {browser_id}")
        cursor.close()

        return username

    def check_login(self, login_id: str, password: str) -> bool:
        return False

