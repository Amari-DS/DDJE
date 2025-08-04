class State(object):
    _instance: 'State' = None

    def __init__(self):
        self.current_file_path: str | None = None
        self.modified: bool = False

    @staticmethod
    def get_state() -> 'State':
        if State._instance is None:
            raise Exception('State has not been initialized')
        return State._instance

    @staticmethod
    def reset():
        State._instance = State()
