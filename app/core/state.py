from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
     from app.core.models import Root


class State(object):
    _instance: 'State' = None

    def __init__(self):
        self.current_file_path: str | None = None
        self.modified: bool = False
        self.current_data: Optional['Root'] = None

    @staticmethod
    def get_state() -> 'State':
        if State._instance is None:
            raise Exception('State has not been initialized')
        return State._instance

    @staticmethod
    def reset():
        State._instance = State()
