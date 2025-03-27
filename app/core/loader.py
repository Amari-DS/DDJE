import json

from app.core.models import Root
from app.misc.misc import Storage


class Loader:

    def __init__(self, file_path: str):
        self.__filepath = file_path

    def load(self) -> None:
        with (open(self.__filepath) as jf):
            content = json.load(jf)
            Storage.current_data = Root.from_json(content)
