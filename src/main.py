

# Python imports
import logging
#import sqlite3
import sys

# External imports
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Local imports
import at_state
import at_config


logger = logging.getLogger(__name__)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
main_state = at_state.ATMainState()

# Check that the user is authenticated:
@app.middleware("http")
async def check_session(request: Request, call_next):
    if main_state.check_session(request.cookies, request.client):
        response = await call_next(request)
        return response
    else:
        response = RedirectResponse(url="/login")
        return response

@app.get("/", response_class=HTMLResponse)
async def main_page():
    user_name = main_state.get_current_user()
    return templates.TemplateResponse(name="start.html", context={"user_name": user_name})

@app.get("/login", response_class=HTMLResponse)
async def login():
    return templates.TemplateResponse(name="login.html")

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
    else:
        logging.error(f"Got too many command line arguments: {all_args}")
        raise ValueError(f"Only expected one command line argument: filename of configuration file.")

    main_state.set_config(global_config)
    main_state.activate()

    uv_config = uvicorn.Config("main:app", port=5000, log_level="debug")
    server = uvicorn.Server(uv_config)
    server.run()

