

# External imports
from nicegui import ui

# Local imports
import at_state



class ATLoginUI:
    def __init__(self, main_state: at_state.ATMainState):
        self.main_state = main_state

        with ui.dialog() as error_dialog:
            ui.label("Login failed!").classes("text-2xl text-red-500 font-bold")

        self.error_dialog = error_dialog

    def check_login(self):
        if self.main_state.check_login(self.login_id.value, self.password.value):
            ui.navigate.to("/main")
        else:
            self.error_dialog.open()

    def show(self):
        with ui.card().classes("absolute-center items-center"):
            ui.label("AEM Transport").classes("text-2xl font-bold")
            ui.label("Please log in first:").classes("text-xl")
            self.login_id = ui.input(label="Login ID").bind_value_to(self, "login_id")
            self.password = ui.input(label="Password", password=True).bind_value_to(self, "password")
            ui.button("Login", icon="login", on_click=self.check_login).classes("rounded-lg")


