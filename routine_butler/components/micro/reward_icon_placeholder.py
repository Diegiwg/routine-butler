from nicegui import ui

from routine_butler.components.primitives import SVG
from routine_butler.constants import ABS_REWARD_SVG_PATH


def reward_icon_placeholder() -> ui.element:
    with ui.row().classes("container flex justify-center items-center w-40"):
        placeholder = ui.element("q-item").props("dense")
        cls = "items-center justify-center border-secondary"
        cls += " rounded w-full border-dotted border-2"
        placeholder.classes(cls).style("height: 2.5rem;")
        with placeholder:
            SVG(
                ABS_REWARD_SVG_PATH,
                size=17,
                color="#e5e5e5",
            )
    return placeholder
