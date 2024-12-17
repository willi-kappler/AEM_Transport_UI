from nicegui import ui


@ui.page("/main")
def main_page():
    ui.page_title('AEM Transport - Main')

    with ui.header():
        with ui.button("File").props("no-caps"):
            with ui.menu():
                ui.menu_item("Load CSV...")
                ui.menu_item("Load JSON...")
                ui.separator()
                ui.menu_item("Save CSV...")
                ui.menu_item("Save JSON...")
                ui.separator()
                ui.menu_item("Log out")

        with ui.button("Edit").props("no-caps"):
            with ui.menu():
                ui.menu_item("Undo")
                ui.menu_item("Redo")
                ui.separator()
                ui.menu_item("Cut")
                ui.menu_item("Copy")
                ui.menu_item("Paste")
                ui.separator()
                ui.menu_item("Clear all")

        with ui.button("Tool").props("no-caps"):
            with ui.menu():
                ui.menu_item("Add point")
                ui.menu_item("Add line")
                ui.menu_item("Add circle")
                ui.separator()
                ui.menu_item("Move element")
                ui.menu_item("Edit element")
                ui.menu_item("Delete element")

        with ui.button("View").props("no-caps"):
            with ui.menu():
                ui.menu_item("Zoom 100%")
                ui.menu_item("Zoom in")
                ui.menu_item("Zoom out")
                ui.separator()
                ui.menu_item("Move / Pan")

        with ui.button("Model").props("no-caps"):
            with ui.menu():
                ui.menu_item("AEM flow")
                ui.menu_item("AEM transport...")
                ui.menu_item("Run model")

        with ui.button("Data").props("no-caps"):
            with ui.menu():
                ui.menu_item("Domain extent...")
                ui.menu_item("Aquifier properties...")
                ui.menu_item("Chemical parameters...")

        with ui.button("Solver").props("no-caps"):
            with ui.menu():
                ui.menu_item("Least squares")
                ui.menu_item("Gauss-Seidel...")
                ui.menu_item("Order of functions (N)...")
                ui.menu_item("Num. of controll points (M)...")

        with ui.button("Post processing").props("no-caps"):
            with ui.menu():
                ui.menu_item("Download result...")
                ui.menu_item("Plots...")
                ui.menu_item("Statistical parameters...")

        with ui.button("Help").props("no-caps"):
            with ui.menu():
                ui.menu_item("Navigation...")
                ui.menu_item("Model manual...")
                ui.menu_item("About...")

    ui.interactive_image(size=(1000, 1000), cross=True).classes("size-[800px] bg-blue-100")

    with ui.footer():
        ui.label("AEM Transport")


@ui.page("/")
def login_page():
    ui.page_title('AEM Transport - Login')

    def check_login() -> None:
        ui.navigate.to("/main")

    with ui.card().classes("absolute-center items-center"):
        ui.label("AEM Transport").classes("text-2xl font-bold")
        ui.label("Please log in first:").classes("text-xl")
        ui.input(label="Login ID")
        ui.input(label="Password")
        ui.button("Login", icon="login", on_click=check_login).classes("rounded-lg")


if __name__ in {"__main__", "__mp_main__"}:
    ui.run()

