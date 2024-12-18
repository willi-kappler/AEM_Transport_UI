

# External imports
from nicegui import app, ui

# Local imports
import at_state



class ATLoginUI:
    def __init__(self, main_state: at_state.ATMainState):
        self.main_state: at_state.ATMainState = main_state

        with ui.dialog() as error_dialog:
            with ui.card():
                ui.label("Login failed!").classes("text-2xl text-red-500 font-bold")

        self.error_dialog = error_dialog

    def check_login(self):
        browser_id: str = app.storage.browser["id"]
        if self.main_state.check_login(self.username.value, self.password.value, browser_id):
            ui.navigate.to("/main")
        else:
            self.error_dialog.open()

    def show(self):
        with ui.card().classes("absolute-center items-center"):
            ui.label("AEM Transport").classes("text-2xl font-bold")
            ui.label("Please log in first:").classes("text-xl")
            self.username = ui.input(label="Username")
            self.password = ui.input(label="Password", password=True)
            ui.button("Login", icon="login", on_click=self.check_login).classes("rounded-lg")


