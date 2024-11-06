

# Python imports
import logging
#import sqlite3
import sys
from typing import Annotated

# External imports
import uvicorn
from fastapi import FastAPI, Cookie

# Local imports
import at_state
import at_config
from at_cookie import ATCookies


logger = logging.getLogger(__name__)

app = FastAPI()
main_state = at_state.ATMainState()

@app.get("/")
async def main_page(cookies: Annotated[ATCookies, Cookie()]):
    return ""

@app.get("/login")
async def login():
    return ""

if __name__ == "__main__":
    log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    log_file_name = "server.log"
    logging.basicConfig(filename=log_file_name, level=logging.DEBUG, format=log_format)
    logging.getLogger("asyncio").setLevel(logging.WARNING)

    global_config = at_config.ATConfiguration()

    all_args = sys.argv
    num_of_args = len(all_args)

    if num_of_args == 1:
        logging.info("Using defualt configuration.")
    elif num_of_args == 2:
        config_filename = all_args[1]
        global_config.from_file(config_filename)
        #logging.info(f"Reading configuration from file: {config_filename}")
    else:
        logging.error(f"Got too many command line arguments: {all_args}")
        raise ValueError(f"Only expected one command line argument: filename of configuration file.")

    main_state.set_config(global_config)
    main_state.activate()

    uv_config = uvicorn.Config("main:app", port=5000, log_level="debug")
    server = uvicorn.Server(uv_config)
    server.run()

