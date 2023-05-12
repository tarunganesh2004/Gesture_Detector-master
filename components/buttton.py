import pygame
import pygame_gui
from typing import Callable, Dict, Union
from pygame_gui.core.interfaces.container_interface import IContainerLikeInterface
from pygame_gui.core.interfaces.manager_interface import IUIManagerInterface
from pygame_gui.core.ui_element import ObjectID, UIElement

class CallbackButton(pygame_gui.elements.UIButton):
    def __init__(self, func: Union[Callable, None] =None, *args, **kwargs):
        self.func = func
        super().__init__(*args, **kwargs)

    def update(self, time_delta: float):
        if self.check_pressed() and self.func is not None:
            self.func()
        return super().update(time_delta)