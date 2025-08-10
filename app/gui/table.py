import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk
from tkinter.messagebox import showerror
from typing import TYPE_CHECKING, Any, Dict, List

from app.core.models import Node, NoteType
from app.gui.edit_window import EditWindow

if TYPE_CHECKING:
     from app.gui.gui import GUI


@dataclass
class ColumnParam(object):
    heading_params: dict[str, Any]
    column_params: dict[str, Any]


# noinspection PyTypeChecker
class Table(object):
    __columns = {
        'time': ColumnParam({'text': 'Time'}, {'width': 110, 'stretch': False, 'anchor': tk.CENTER}),
        'v_pos': ColumnParam({'text': 'V pos'}, {'width': 50, 'stretch': False, 'anchor': tk.CENTER}),
        'h_pos': ColumnParam({'text': 'H pos'}, {'width': 50, 'stretch': False, 'anchor': tk.CENTER})
    }

    def __init__(self, gui: 'GUI'):
        self.__gui = gui
        self.__table_frame = ttk.Frame(self.__gui.get_main_frame())
        self.__table = ttk.Treeview(self.__table_frame, columns=list(self.__columns.keys()), show=('headings', 'tree'))
        self.__content: Dict[str, Any] = None

    def setup(self):
        self.__table_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        self.__set_columns()
        self.__add_scrollbar()
        self.__table.bind('<Double-1>', self.__on_double_click)
        style = ttk.Style(self.__gui.get_root())
        style.configure('Treeview', rowheight=32, font=('Helvetica', 16))

    def __set_columns(self):
        self.__table.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        self.__table.heading('#0', text='Type')
        self.__table.column('#0', anchor=tk.W, width=120, stretch=False)
        for c_id, c_param in self.__columns.items():
            self.__table.heading(c_id, **c_param.heading_params)
            self.__table.column(c_id, **c_param.column_params)

    def __add_scrollbar(self):
        v_scrollbar = ttk.Scrollbar(self.__table_frame, orient='vertical', command=self.__table.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.__table.configure(yscrollcommand=v_scrollbar.set)

    def load_data(self, nodes_list: List[Node]):
        self.__reset()
        self.__content = {n.id: n for n in nodes_list}
        for node in sorted(nodes_list, key=lambda n: n.noteOrder):
            note_image = node.noteType.binded_value
            self.__table.insert('', tk.END, iid=node.id, values=node.to_repr(),
                                text=' ' + note_image.label, image=note_image.image)

    def __reset(self):
        self.__table.delete(*self.__table.get_children())
        self.__table.yview_moveto(0.0)

    def update_row(self, node: Node):
        self.__table.item(item=node.id, values=node.to_repr())

    def __on_double_click(self, _):
        node = self.get_selection()
        if node.noteType in (NoteType.WALL_START, NoteType.WALL_END):
            showerror(title='Error', message=f'Unsupported')
            return
        edit_window = EditWindow(self.__gui, node)
        edit_window.open()

    def get_selection(self) -> Node:
        selected_item_id = self.__table.focus()
        if not selected_item_id:
            return None
        return self.__content[selected_item_id]
