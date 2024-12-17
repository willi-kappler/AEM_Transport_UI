
# Python imports
import logging
import sqlite3
import uuid
from typing import Optional
from hashlib import blake2b

# External imports
from fastapi import Request


# Local imports
import at_config


logger = logging.getLogger(__name__)

AT_SESSION_ID = "AT_f294098d4ca564e6b0c8ccf460e06d80_ID"
AT_SESSION_MAX_AGE = 60 * 60 * 4 # In seconds, thus 4 hours

def get_session_id(request: Request) -> Optional[str]:
    cookies: dict[str, str] = request.cookies

    if AT_SESSION_ID not in cookies:
        logger.debug("No session_id found in cookies.")
        return None

    session_id: str = cookies[AT_SESSION_ID]

    try:
        uuid_object = uuid.UUID(session_id, version=4)
        del uuid_object
    except Exception:
        logging.debug(f"Invalid session id (uuid version 4): {session_id}")
        return None

    return session_id

class ATMainState:
    def __init__(self):
        self.configuration = at_config.ATConfiguration()
        print("ATMainState init")

    def set_config(self, configuration: at_config.ATConfiguration):
        self.configuration = configuration
        print("Configuration was set")

    def activate(self):
        self.db = sqlite3.connect(self.configuration.db_filename)
        print("Database was loaded")

    def get_current_user(self, request: Request) -> Optional[str]:
        session_id = get_session_id(request)

        if session_id is None:
            return None

        cursor = self.db.cursor()
        db_res = cursor.execute(f"SELECT user_id FROM sessions WHERE uuid = '{session_id}'")
        db_row = db_res.fetchone()
        if db_row is None:
            logger.debug(f"Session not found: {session_id}")
            return None

        user_id = db_row[0]

        db_res = cursor.execute(f"SELECT login FROM users WHERE id = '{user_id}'")
        db_row = db_res.fetchone()
        if db_row is None:
            logger.debug(f"User id not found: {user_id}")
            return None

        username = db_row[0]

        logger.debug(f"Found user: {username} for session: {session_id}")

        # TODO: check for ip or sth. else...

        cursor.close()

        return username

    def create_new_session(self, username: str, password: str) -> Optional[str]:
        logging.debug(f"Create a new session for user: {username}")

        cursor = self.db.cursor()
        db_res = cursor.execute(f"SELECT id, password FROM users WHERE login = '{username}'")
        db_row = db_res.fetchone()
        if db_row is None:
            logger.debug(f"User not found: {username}")
            return None

        user_id: str = db_row[0]
        stored_password: str = db_row[1]

        # Check password
        # TODO: use better method with salting!!!!
        hashed_password = blake2b(password.encode()).hexdigest()
        if hashed_password != stored_password:
            logger.debug("Password does not match!")
            return None

        # Remove all old sessions from the user:
        db_res = cursor.execute(f"DELETE FROM sessions WHERE user_id = '{user_id}'")
        logger.debug(f"Removed {db_res.rowcount} old sessions for user {username}.")

        # Create a new random session id:
        new_session_id: str = uuid.uuid4().hex
        cursor.execute(f"INSERT INTO sessions (uuid, ip_hash, user_id) VALUES ('{new_session_id}', 'IP_TEST', {user_id})")

        self.db.commit()
        cursor.close()

        return new_session_id

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

