import tkinter as tk

from app.gui.buttons import Buttons
from app.gui.status_bar import StatusBar
from app.gui.table import Table


# noinspection PyTypeChecker
class GUI(object):
    __width = 600
    __height = 800

    def __init__(self):
        self.__root = tk.Tk()
        self.__main_frame = tk.Frame(self.__root)
        self.__footer = tk.Frame(self.__root)
        self.__buttons = Buttons(self)
        self.__table = Table(self)
        self.__status_bar = StatusBar(self)
        self.__setup()

    def start(self):
        self.__root.mainloop()

    def __setup(self):
        self.__main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.__footer.pack(side=tk.BOTTOM, fill=tk.X, expand=False)
        self.__root.title('DDJE')
        self.__center()
        self.__buttons.setup()
        self.__table.setup()
        self.__status_bar.setup()

    def get_root(self) -> tk.Tk:
        return self.__root

    def get_footer(self) -> tk.Frame:
        return self.__footer

    def get_main_frame(self) -> tk.Frame:
        return self.__main_frame

    def get_table(self) -> Table:
        return self.__table

    def get_status_bar(self) -> StatusBar:
        return self.__status_bar

    def __center(self):
        screen_width = self.__root.winfo_screenwidth()
        screen_height = self.__root.winfo_screenheight()
        x = (screen_width - self.__width) // 2
        y = (screen_height - self.__height) // 2
        self.__root.geometry(f'{self.__width}x{self.__height}+{x}+{y}')
