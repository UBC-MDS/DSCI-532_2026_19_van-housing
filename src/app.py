from shiny import App

from .ui import app_ui
from .server import server


# For App Rendering, this line must be at the last
app = App(app_ui, server=server)