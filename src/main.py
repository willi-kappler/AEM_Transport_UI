

# Python imports
import logging
import sys
from typing import Optional

# External imports
from nicegui import app, ui

# Local imports
import at_config
import at_state
import at_login
import at_main


logger = logging.getLogger(__name__)

@ui.page("/main", title="AEM - Main")
def main_page():
    browser_id: str = app.storage.browser["id"]
    maybe_user: Optional[str]  = main_state.get_current_user(browser_id)

    match maybe_user:
        case None:
            # Not logged in, redirect to /login:
            ui.navigate.to("/login")
        case username:
            # Already logged in, show main ui:
            main_ui = at_main.ATMainUI(username, main_state)
            main_ui.show()

@ui.page("/login", title="AEM - Login")
def login_page():
    browser_id: str = app.storage.browser["id"]
    maybe_user: Optional[str]  = main_state.get_current_user(browser_id)

    match maybe_user:
        case None:
            # Not logged in, show login ui:
            login_ui = at_login.ATLoginUI(main_state)
            login_ui.show()
        case _:
            # Already logged in, redirect to main:
            ui.navigate.to("/main")

@ui.page("/", title="AEM")
def root_page():
    browser_id: str = app.storage.browser["id"]
    maybe_user: Optional[str]  = main_state.get_current_user(browser_id)

    match maybe_user:
        case None:
            # Not logged in, redirect to /login:
            ui.navigate.to("/login")
        case _:
            # Already logged in, redirect to /main:
            ui.navigate.to("/main")

if __name__ in {"__main__", "__mp_main__"}:
    global main_state

    log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    log_file_name = "server.log"
    logging.basicConfig(filename=log_file_name, level=logging.DEBUG, format=log_format)

    # Silence loggers from other modules:
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("multipart").setLevel(logging.WARNING)

    all_args = sys.argv
    num_of_args = len(all_args)

    global_config = at_config.ATConfiguration()

    if num_of_args == 1:
        logging.info("Using defualt configuration.")
    elif num_of_args == 2:
        config_filename = all_args[1]
        global_config.from_file(config_filename)
    else:
        logging.error(f"Got too many command line arguments: {all_args}")
        raise ValueError("Only expected one command line argument: filename of configuration file.")

    main_state = at_state.ATMainState()
    main_state.set_config(global_config)
    main_state.activate()

    ui.run(storage_secret=global_config.secret, show=False, reload=False)

