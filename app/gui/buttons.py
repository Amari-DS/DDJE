import json
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo
from typing import TYPE_CHECKING

from app.core.loader import Loader
from app.core.state import State
from app.misc.backup import Backup

if TYPE_CHECKING:
     from app.gui.gui import GUI


# noinspection PyTypeChecker
class Buttons(object):

    def __init__(self, gui: 'GUI'):
        self.__gui = gui
        self.__buttons_frame = ttk.Frame(self.__gui.get_main_frame())

    def setup(self):
        self.__buttons_frame.pack(fill=tk.Y, side=tk.LEFT, padx=5, pady=5)
        open_button = ttk.Button(self.__buttons_frame, text='Open JSON', command=self.__load_data)
        open_button.pack(side=tk.TOP)
        print_raw = ttk.Button(self.__buttons_frame, text='Print raw', command=self.__print_raw)
        print_raw.pack()
        save_local = ttk.Button(self.__buttons_frame, text='Save', command=self.__save)
        save_local.pack()

    def __load_data(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            Loader(filepath).load()
            self.__gui.get_table().load_data(State.get_state().current_data.data.all_nodes)
            State.get_state().current_file_path = filepath
            self.__gui.get_status_bar().update()

    def __print_raw(self):
        node = self.__gui.get_table().get_selection()
        if not node:
            return
        print(node.to_dict())

    def __save(self):
        Backup().backup()

        try:
            state = State.get_state()
            with open(state.current_file_path, 'w') as file:
                json.dump(state.current_data.to_dict(), file, separators=(',', ':'))
        except IOError as e:
            print(f'Error saving data to file: {e}')

        State.get_state().modified = False
        self.__gui.get_status_bar().update()
        showinfo(title='Info', message='Saved')
