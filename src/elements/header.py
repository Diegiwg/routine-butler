import os
from datetime import datetime

from nicegui import ui

from elements.svg import SVG
from utils.constants import clrs

BUTTON_STYLE = "height: 45px; width: 45px; background-color: {clr} !important;"
APP_NAME = "RoutineButler"
APP_NAME_SIZE = "1.9rem"
ROUTINES_SVG_SIZE: int = 30
PROGRAMS_SVG_SIZE: int = 26
LOGO_SIZE = "2.6rem"
TIME_SIZE = "1.1rem"
DATE_SIZE = ".7rem"

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROUTINE_SVG_FPATH = os.path.join(CURRENT_DIR, "../assets/routine-icon.svg")
PROGRAM_SVG_FPATH = os.path.join(CURRENT_DIR, "../assets/program-icon.svg")


class Clock(ui.column):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.classes("-space-y-1 gap-0")
        self.style("align-items: center;")

        with self:
            # time
            time = ui.label().style(f"font-size: {TIME_SIZE}")
            time.classes("items-center")
            set_time = lambda: time.set_text(
                datetime.now().strftime("%H:%M:%S")
            )
            ui.timer(0.1, set_time)

            # date
            date = ui.label().style(f"font-size: {DATE_SIZE}")
            date.classes("items-center;")
            set_date = lambda: date.set_text(
                datetime.now().strftime("%b %d, %Y")
            )
            ui.timer(1.0, set_date)


class Header(ui.header):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.classes("justify-between items-center")
        self.style(
            f"background-color: {clrs.dark_green};"
            f"box-shadow: 0 2px 15px rgba(0, 0, 0, 0.5);"
        )

        with self:
            left_content = ui.row().style("align-items: center")
            right_content = ui.row().style("align-items: center")
            with left_content:
                # routines button
                self.routines_button = ui.button()
                style = BUTTON_STYLE.format(clr=clrs.dark_gray)
                self.routines_button.style(style)
                with self.routines_button:
                    SVG(ROUTINE_SVG_FPATH, ROUTINES_SVG_SIZE)
                # app name
                ui.label(APP_NAME).style(f"font-size: {APP_NAME_SIZE}")
            with right_content:
                # clock
                Clock()
                # programs button
                self.programs_button = ui.button()
                style = BUTTON_STYLE.format(clr=clrs.dark_gray)
                self.programs_button.style(style)
                with self.programs_button:
                    SVG(PROGRAM_SVG_FPATH, PROGRAMS_SVG_SIZE)
