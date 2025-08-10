import tkinter as tk
from tkinter.messagebox import showerror
from typing import TYPE_CHECKING

from app.core.models import Node, NoteType
from app.core.state import State

if TYPE_CHECKING:
     from app.gui.gui import GUI


# noinspection PyTypeChecker
class EditWindow(object):
    __width = 150
    __height = 75
    __max_value = 10

    def __init__(self, gui: 'GUI', content: Node):
        self.__node = content
        self.__gui = gui
        self.__counter_value = tk.IntVar()
        self.__window = self.__setup()
        self.__min_value = -1 if self.__node.noteType == NoteType.ROAD_BLOCK else 0

    def __setup(self) -> tk.Toplevel:
        root = self.__gui.get_root()
        edit_window = tk.Toplevel(root)
        edit_window.title('Edit node')
        edit_window.transient(root)
        edit_window.grab_set()
        edit_window.resizable(False, False)

        label = tk.Label(edit_window, text='Vertical position')
        label.place(y=8, x=8)
        entry = tk.Entry(edit_window, textvariable=self.__counter_value, width=5, justify=tk.CENTER)
        entry.place(y=10, x=102)

        self.__add_buttons(edit_window)

        return edit_window

    def __add_buttons(self, edit_window):
        start_x = 39
        y_pos = 37
        increment_button = tk.Button(edit_window, text='↑', height=1, command=self.increment)
        increment_button.place(y=y_pos, x=start_x)
        decrement_button = tk.Button(edit_window, text='↓', height=1, command=self.decrement)
        decrement_button.place(y=y_pos, x=start_x + 20)
        save_button = tk.Button(edit_window, text='Save', command=self.__save_changes)
        save_button.place(y=y_pos, x=start_x + 40)

    def __center(self):
        root = self.__gui.get_root()

        root.update_idletasks()
        main_x = root.winfo_x()
        main_y = root.winfo_y()
        main_width = root.winfo_width()
        main_height = root.winfo_height()

        center_x_offset = (main_width - self.__width) // 2
        center_y_offset = (main_height - self.__height) // 2
        new_x = main_x + center_x_offset
        new_y = main_y + center_y_offset

        self.__window.geometry(f'{self.__width}x{self.__height}+{new_x}+{new_y}')

    def open(self):
        self.__counter_value.set(self.__node.position.y)
        self.__center()
        self.__window.focus_force()
        self.__gui.get_root().wait_window(self.__window)

    def increment(self):
        current_value = self.__counter_value.get()
        new_value = current_value + 1
        if new_value > self.__max_value:
            showerror(title='Error', message=f'Max value is {self.__max_value}')
            return
        self.__counter_value.set(new_value)

    def decrement(self):
        current_value = self.__counter_value.get()
        new_value = current_value - 1
        if new_value < self.__min_value:
            showerror(title='Error', message=f'Min value is {self.__min_value}')
            return
        self.__counter_value.set(new_value)

    def __save_changes(self):
        current_value = self.__counter_value.get()
        if not self.__min_value <= current_value <= self.__max_value:
            showerror(title='Error', message=f'Value must be between {self.__min_value} and {self.__max_value}')
            return
        self.__node.position.v_pos = current_value
        self.__gui.get_table().update_row(self.__node)
        self.__window.destroy()
        State.get_state().modified = True
        self.__gui.get_status_bar().update()
