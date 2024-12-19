
# Python imports
import logging

# External imports
from nicegui import app, ui


logger = logging.getLogger(__name__)


class ATCanvas:
    def __init__(self):
        self.elements = []

        # TODO: get state and gfx elements from browser via app.storage

    def show(self):
        self.image = ui.interactive_image(size=(1000, 1000), cross=True).classes("size-[800px] bg-blue-100")



