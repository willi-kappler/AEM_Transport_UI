

# Python imports
import logging
import sys
from typing import Optional
from contextlib import asynccontextmanager

# External imports
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Local imports
import at_state
import at_config


logger = logging.getLogger(__name__)

@asynccontextmanager
async def init_data(app: FastAPI):
    global main_state

    print("Lifespan: init_data()")
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
        raise ValueError("Only expected one command line argument: filename of configuration file.")

    main_state = at_state.ATMainState()
    main_state.set_config(global_config)
    main_state.activate()

    yield


app = FastAPI(lifespan=init_data)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
@app.post("/")
async def main_page(request: Request):
    maybe_user: Optional[str] = main_state.get_current_user(request)

    match maybe_user:
        case None:
            return RedirectResponse(url="/login")
        case username:
            return templates.TemplateResponse(name="start.html",
                context={"request": request, "username": username})


@app.get("/login")
async def login_get(request: Request):
    maybe_user: Optional[str] = main_state.get_current_user(request)

    match maybe_user:
        case None:
            return templates.TemplateResponse(name="login.html",
                context={"request": request, "message": "Please log in first."})
        case _:
            return RedirectResponse(url="/")


@app.post("/login")
async def login_post(request: Request, login: str = Form(), passwd: str = Form()):
    maybe_session = main_state.create_new_session(login, passwd)

    match maybe_session:
        case None:
            return templates.TemplateResponse(name="login.html",
                context={"request": request, "message": "Failed login, please retry!"})
        case new_session:
            response = RedirectResponse(url="/")
            response.set_cookie(key=at_state.AT_SESSION_ID, value=new_session, max_age=at_state.AT_SESSION_MAX_AGE)
            return response


@app.get("/logout")
@app.post("/logout")
async def logout_get(request: Request):
    maybe_user: Optional[str] = main_state.get_current_user(request)

    match maybe_user:
        case None:
            return RedirectResponse(url="/login")
        case user:
            main_state.logout_user(user)
            response = RedirectResponse(url="/login")
            response.delete_cookie(key=at_state.AT_SESSION_ID)
            return response


if __name__ == "__main__":
    log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    log_file_name = "server.log"
    logging.basicConfig(filename=log_file_name, level=logging.DEBUG, format=log_format)

    # Silence loggers from other modules:
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("multipart").setLevel(logging.WARNING)

    uv_config = uvicorn.Config("main:app", port=5000, log_level="debug")
    server = uvicorn.Server(uv_config)
    server.run()

