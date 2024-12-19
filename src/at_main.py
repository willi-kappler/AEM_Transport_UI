
# Python imports
import logging
import enum

# External imports
from nicegui import app, ui

# Local imports
import at_state
import at_canvas

logger = logging.getLogger(__name__)

class ATModelType(enum.Enum):
    AEM_Flow = 0
    AEM_Transport_horizontal = 1
    AEM_Transport_vertical = 2


class ATMainUI:
    def __init__(self, username: str, main_state: at_state.ATMainState):
        self.username: str = username
        self.main_state = main_state
        self.canvas = at_canvas.ATCanvas()
        self.aem_model_type = ATModelType.AEM_Flow
        self.domain_extend = (0.0, 0.0, 100.0, 100.0)

        # TODO: get state and settings from browser via app.storage

        # File menu:
        with ui.dialog() as self.logout_dialog:
            with ui.card():
                ui.label("Logged out sucessfully!").classes("text-2xl")

        # Model menu:
        with ui.dialog() as self.aem_transport_dialog:
            with ui.card():
                def set_variant(element):
                    self.aem_transport_dialog.close()
                    v = element.value
                    match v:
                        case "horizontal":
                            self.aem_model_type = ATModelType.AEM_Transport_horizontal
                            self.status_bar.set_text("AEM model is now of type transport horizontal")
                        case "vertical":
                            self.aem_model_type = ATModelType.AEM_Transport_vertical
                            self.status_bar.set_text("AEM model is now of type transport vertical")

                ui.label("Select AEM transport variant:").classes("text-1xl")
                ui.select(["horizontal", "vertical"], on_change=set_variant, value="horizontal")

        # Data menu:
        with ui.dialog() as self.domain_extend_dialog:
            with ui.card():
                def set_values():
                    self.domain_extend_dialog.close()
                    self.domain_extend = (x_min.value, y_min.value, x_max.value, y_max.value)
                    self.status_bar.set_text(f"New domain extend: {self.domain_extend}")

                ui.label("Set domain extend:").classes("text-1xl")
                x_min = ui.number("x min", value=self.domain_extend[0], step=10.0)
                y_min = ui.number("y min", value=self.domain_extend[1], step=10.0)
                x_max = ui.number("x max", value=self.domain_extend[2], step=10.0)
                y_max = ui.number("y max", value=self.domain_extend[3], step=10.0)
                ui.button("OK", on_click=set_values)

        # Help menu:
        with ui.dialog() as self.about_dialog:
            with ui.card():
                ui.label("Supervisor: Prabhas Yadav").classes("text-1xl")
                ui.label("Simulation: Anton Köhler").classes("text-1xl")
                ui.label("GUI: Willi Kappler").classes("text-1xl")


    def show(self):
        with ui.header():
            with ui.button("File").props("no-caps"):
                with ui.menu():
                    ui.menu_item("Load CSV...", self.file_load_csv)
                    ui.menu_item("Load JSON...", self.file_load_json)
                    ui.separator()
                    ui.menu_item("Save CSV...", self.file_save_csv)
                    ui.menu_item("Save JSON...", self.file_save_json)
                    ui.separator()
                    ui.menu_item("Log out", self.file_logout)

            with ui.button("Edit").props("no-caps"):
                with ui.menu():
                    ui.menu_item("Undo", self.edit_undo)
                    ui.menu_item("Redo", self.edit_redo)
                    ui.separator()
                    ui.menu_item("Cut", self.edit_cut)
                    ui.menu_item("Copy", self.edit_copy)
                    ui.menu_item("Paste", self.edit_paste)
                    ui.separator()
                    ui.menu_item("Clear all", self.edit_clear_all)

            with ui.button("Tool").props("no-caps"):
                with ui.menu():
                    ui.menu_item("Add point", self.tool_add_point)
                    ui.menu_item("Add line", self.tool_add_line)
                    ui.menu_item("Add circle", self.tool_add_circle)
                    ui.separator()
                    ui.menu_item("Move element", self.tool_move_element)
                    ui.menu_item("Edit element", self.tool_edit_element)
                    ui.menu_item("Delete element", self.tool_delete_element)

            with ui.button("View").props("no-caps"):
                with ui.menu():
                    ui.menu_item("Zoom 100%", self.view_zoom_100)
                    ui.menu_item("Zoom in", self.view_zoom_in)
                    ui.menu_item("Zoom out", self.view_zoom_out)
                    ui.separator()
                    ui.menu_item("Move / Pan", self.view_move)

            with ui.button("Model").props("no-caps"):
                with ui.menu():
                    ui.menu_item("AEM flow", self.model_aem_flow)
                    ui.menu_item("AEM transport...", self.model_aem_transport)
                    with ui.menu_item("Run model", self.model_run):
                        with ui.item_section().props("side"):
                            ui.icon("play_arrow")

            with ui.button("Data").props("no-caps"):
                with ui.menu():
                    ui.menu_item("Domain extent...", self.data_domain_extent)
                    ui.menu_item("Aquifier properties...", self.data_aquifier)
                    ui.menu_item("Chemical parameters...", self.data_chemical)

            with ui.button("Solver").props("no-caps"):
                with ui.menu():
                    ui.menu_item("Least squares", self.solver_least_squares)
                    ui.menu_item("Gauss-Seidel...", self.solver_gauss_seidel)
                    ui.menu_item("Order of functions (N)...", self.solver_function_order)
                    ui.menu_item("Num. of controll points (M)...", self.solver_controll_points)

            with ui.button("Post processing").props("no-caps"):
                with ui.menu():
                    ui.menu_item("Download result...", self.postp_download_result)
                    ui.menu_item("Plots...", self.postp_plots)
                    ui.menu_item("Statistical parameters...", self.postp_statistics)

            with ui.button("Help").props("no-caps"):
                with ui.menu():
                    ui.menu_item("Navigation...", self.help_navigation)
                    ui.menu_item("Model manual...", self.help_manual)
                    ui.menu_item("About...", self.help_about)

            ui.space()
            ui.label(f"{self.username}")

        self.canvas.show()

        with ui.footer():
            self.status_bar = ui.label("Welcome to AEM Transport")

    # File menu:
    def file_load_csv(self):
        pass

    def file_load_json(self):
        pass

    def file_save_csv(self):
        pass

    def file_save_json(self):
        pass

    async def file_logout(self):
        self.main_state.logout_user(self.username)
        await self.logout_dialog
        ui.navigate.to("/login")

    # Edit menu:
    def edit_undo(self):
        pass

    def edit_redo(self):
        pass

    def edit_cut(self):
        pass

    def edit_copy(self):
        pass

    def edit_paste(self):
        pass

    def edit_clear_all(self):
        pass

    # Tool menu:
    def tool_add_point(self):
        pass

    def tool_add_line(self):
        pass

    def tool_add_circle(self):
        pass

    def tool_move_element(self):
        pass

    def tool_edit_element(self):
        pass

    def tool_delete_element(self):
        pass

    # View menu:
    def view_zoom_100(self):
        pass

    def view_zoom_in(self):
        pass

    def view_zoom_out(self):
        pass

    def view_move(self):
        pass

    # Model menu:
    def model_aem_flow(self):
        self.aem_model_type = ATModelType.AEM_Flow
        self.status_bar.set_text("AEM model is now of type flow")

    def model_aem_transport(self):
        self.aem_transport_dialog.open()

    def model_run(self):
        pass

    # Data menu:
    def data_domain_extent(self):
        self.domain_extend_dialog.open()

    def data_aquifier(self):
        pass

    def data_chemical(self):
        pass

    # Solver menu:
    def solver_least_squares(self):
        pass

    def solver_gauss_seidel(self):
        pass

    def solver_function_order(self):
        pass

    def solver_controll_points(self):
        pass

    # Post processing menu:
    def postp_download_result(self):
        pass

    def postp_plots(self):
        pass

    def postp_statistics(self):
        pass

    # Help menu:
    def help_navigation(self):
        pass

    def help_manual(self):
        pass

    def help_about(self):
        self.about_dialog.open()

