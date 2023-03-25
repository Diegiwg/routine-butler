from loguru import logger

from components.primitives.button import Button
from components.primitives.collapsible_vbox import CollapsibleVBox
from components.routine_configurer import RoutineConfigurer
from database import Routine, User


class RoutineComponent(CollapsibleVBox):
    """
    Class for "RoutineComponents" objects

    A "Routine" is a self-managing chronology of "Programs" that can be scheduled
    to a time of day. For example, the user's morning "routine" might be comprised
    of a ReadText "Program" to read a motivational quote and a PromptContinue
    "Program" to prompt the user to drink a glass of water."
    """

    routine: Routine

    def __init__(self, routine: Routine, user: User):
        self.routine = routine
        self.user = user
        CollapsibleVBox.__init__(self, title=self.routine.title)

        self.title_text_input.onchange.connect(self.on_title_change)

        self.css_margin = "12px"
        self.css_width = "78%"
        self.css_border_color = "yellow"
        self.css_border_width = "2px"
        self.css_border_style = "solid"

        self.routine_configurer = RoutineConfigurer(routine, self.user)
        self.append(self.routine_configurer)

        # initiate routine button
        self.initiate_routine_button = Button("Initiate Routine")
        self.initiate_routine_button.onclick.connect(self.on_initiate_routine)
        self.initiate_routine_button.css_background_color = "green"
        self.initiate_routine_button.css_width = "33%"
        self.initiate_routine_button.css_float = "right"
        self.append(self.initiate_routine_button, "initiate_routine_button")

    def on_initiate_routine(self, widget):
        """Initiates the routine"""
        logger.debug("Routine initiation not yet implemented")

    def should_be_on_screen(self):
        """Returns True if the Routine should be on screen, False otherwise"""
        # TODO: Implement this
        return True

    def idle(self):
        """Gets called every update_interval seconds"""
        self.routine_configurer.idle()

    def on_title_change(self, _, new_value: str):
        """Called when the title text input changes"""
        self.routine.title = new_value
