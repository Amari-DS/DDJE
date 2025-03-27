from dataclasses import dataclass, field, asdict
from functools import cached_property
from typing import Any, List, Dict

from app.misc.misc import BindedEnum


@dataclass
class BaseEntry:
    other_data: Dict[str, Any]

    def to_dict(self):
        return dict(self.other_data)

@dataclass
class Position:
    x: int  # horizontal
    y: int  # vertical

    @property
    def v_pos(self) -> int:
        return self.y

    @v_pos.setter
    def v_pos(self, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError('Value must be an integer')
        self.y = value

    @property
    def h_pos(self) -> int:
        return self.x

    @h_pos.setter
    def h_pos(self, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError('Value must be an integer')
        self.x = value

    def __str__(self):
        return f'X={self.x}(H) Y={self.y}(V)'

    @staticmethod
    def from_json(json_data: Dict[str, int]) -> 'Position':
        return Position(x=json_data['x'], y=json_data['y'])


class NoteType(BindedEnum):
    HAND_LEFT = 6, '✋L (blue)'
    HAND_RIGHT = 7, '✋R (red)'
    FOOT_LEFT = 8, '🦶L (blue)'
    FOOT_RIGHT = 9, '🦶R (red)'


@dataclass
class Node(BaseEntry):
     noteOrder: int
     time: float
     position: Position
     noteType: NoteType
     __parent: 'Data' = field(metadata={'skip': True}, default=None)

     def to_repr(self):
         return self.time_real, self.position.y, self.position.x, self.noteType

     @property
     def time_real(self):
         seconds_float: float = self.noteOrder / self.__parent.order_div
         seconds_total = int(seconds_float)
         millis = int((seconds_float - seconds_total) * 1000)
         minutes, seconds = divmod(seconds_total, 60)
         return  f"{minutes:d}:{seconds:02d}.{millis:03d}"

     @staticmethod
     def from_json(parent: 'Data', json_data) -> 'Node':
         node = Node(
             noteOrder=json_data['noteOrder'],
             time=json_data['time'],
             position=Position.from_json(json_data.pop('position')),
             noteType=NoteType(json_data['noteType']),
             other_data=json_data
         )
         node.__parent = parent
         return node

     @property
     def id(self):
         return f'{self.noteOrder}.{self.noteType.value}'

     def to_dict(self) -> Dict[str, Any]:
         obj_dict = super().to_dict()
         obj_dict['position'] = asdict(self.position)
         return obj_dict


@dataclass
class Data(BaseEntry):
     orderCountPerBeat: int
     sphereNodes: List[Node] = None
     __parent: 'Root'  = field(metadata={'skip': True}, default=None)

     @staticmethod
     def from_json(parent: 'Root', json_data: Dict[str, Any]) -> 'Data':
         data = Data(orderCountPerBeat=json_data['orderCountPerBeat'], other_data=json_data)
         data.__parent = parent
         data.sphereNodes = [Node.from_json(data, nj) for nj in json_data.pop('sphereNodes')]
         return data

     @cached_property
     def order_div(self):
         return self.orderCountPerBeat * self.__parent.BPM / 60

     def to_dict(self) -> Dict[str, Any]:
         obj_dict = super().to_dict()
         obj_dict['sphereNodes'] = [n.to_dict() for n in self.sphereNodes]
         return obj_dict


@dataclass
class Root(BaseEntry):
     BPM: int
     data: Data = None

     @staticmethod
     def from_json(raw_data: Dict[str, Any]) -> 'Root':
         root = Root(BPM=raw_data['BPM'], other_data=raw_data)
         root.data = Data.from_json(root, raw_data.pop('data'))
         return root

     def to_dict(self) -> Dict[str, Any]:
         obj_dict = super().to_dict()
         obj_dict['data'] = self.data.to_dict()
         return obj_dict
