import os
from typing import Iterator

from app.core.state import State


class Backup(object):
    _BAK_BASE_EXT = '.bak'
    _BAK_EXT_LIST = [_BAK_BASE_EXT, _BAK_BASE_EXT + '.1', _BAK_BASE_EXT + '.2']

    def __init__(self) -> None:
        self.__filepath = State.get_state().current_file_path

    def backup(self):
        ext_iter = iter(self._BAK_EXT_LIST)
        self.__move(self.__filepath, ext_iter)

    def __move(self, src_path: str, ext_iter: Iterator[str]) -> None:
        if not os.path.exists(src_path):
            return
        try:
            dst_path = self.__filepath + next(ext_iter)
            if os.path.exists(dst_path):
                self.__move(dst_path, ext_iter)
            os.rename(src_path, dst_path)
        except StopIteration:
            os.remove(src_path)
