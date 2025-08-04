import tkinter as tk
from typing import TYPE_CHECKING

from app.core.state import State

if TYPE_CHECKING:
    from app.gui.gui import GUI


# noinspection PyTypeChecker
class StatusBar(object):

    def __init__(self, gui: 'GUI'):
        self.__gui = gui
        self.__status_bar = tk.Label(self.__gui.get_footer(), anchor=tk.W)

    def setup(self):
        self.__status_bar.pack(side=tk.BOTTOM, fill=tk.X, expand=True)

    def update(self):
        state = State.get_state()
        modified_token = '*' if state.modified else ''
        new_status = f'{modified_token}{state.current_file_path}'
        self.__status_bar.configure(text=new_status)
