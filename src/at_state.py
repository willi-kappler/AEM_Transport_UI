
# Python imports
import logging
import sqlite3
from typing import Optional
from hashlib import blake2b


# Local imports
import at_config


logger = logging.getLogger(__name__)

class ATMainState:
    def __init__(self):
        self.configuration: at_config.ATConfiguration = at_config.ATConfiguration()
        logger.info("ATMainState init")

    def set_config(self, configuration: at_config.ATConfiguration):
        self.configuration: at_config.ATConfiguration = configuration
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

        user_id: str = db_row[0]

        db_res = cursor.execute(f"SELECT login FROM users WHERE id = '{user_id}'")
        db_row = db_res.fetchone()
        if db_row is None:
            logger.debug(f"User id not found: {user_id}")
            return None

        username: str = db_row[0]

        logger.debug(f"Found user: {username} for session: {browser_id}")
        cursor.close()

        return username

    def check_login(self, username: str, password: str, browser_id: str) -> bool:
        logger.debug(f"Check user: {username}, browser_id: {browser_id}")

        cursor = self.db.cursor()
        db_res = cursor.execute(f"SELECT id, password FROM users WHERE login = '{username}'")
        db_row = db_res.fetchone()
        if db_row is None:
            logger.debug(f"User not found: {username}")
            return False

        user_id: str = db_row[0]
        stored_password: str = db_row[1]

        # Check password
        # TODO: use better method with salting!!!!
        hashed_password = blake2b(password.encode()).hexdigest()
        if hashed_password != stored_password:
            logger.debug("Password does not match!")
            return False

        # Remove all old sessions from the user:
        db_res = cursor.execute(f"DELETE FROM sessions WHERE user_id = '{user_id}'")
        logger.debug(f"Removed {db_res.rowcount} old sessions for user {username}.")

        # Create a new random session id:
        cursor.execute(f"INSERT INTO sessions (uuid, ip_hash, user_id) VALUES ('{browser_id}', 'IP_TEST', {user_id})")

        self.db.commit()
        cursor.close()

        return True

    def logout_user(self, username: str):
        cursor = self.db.cursor()

        # Remove session from the user:
        db_res = cursor.execute(f"SELECT id FROM users WHERE login = '{username}'")
        db_row = db_res.fetchone()
        if db_row is None:
            logger.debug(f"User not found: {username}")
            return

        user_id: str = db_row[0]
        db_res = cursor.execute(f"DELETE FROM sessions WHERE user_id = '{user_id}'")
        logger.debug(f"Removed {db_res.rowcount} session(s) for user {username}.")

        self.db.commit()
        cursor.close()

