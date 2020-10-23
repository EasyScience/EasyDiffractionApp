__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'

from abc import abstractmethod
from typing import Union, overload, TypeVar

from easyCore import np
from easyCore.Utils.json import MSONable, MontyDecoder
from collections.abc import Sequence

T = TypeVar('T')


class ProjectData(MSONable):
    def __init__(self, name='DataStore', exp_data=None, sim_data=None):
        self.name = name
        if exp_data is None:
            exp_data = DataStore(name='Exp Datastore')
        if sim_data is None:
            sim_data = DataStore(name='Sim Datastore')
        self.exp_data = exp_data
        self.sim_data = sim_data


class DataStore(Sequence, MSONable):

    def __init__(self, *args, name='DataStore', x_label: str = 'x', y_label: str = 'y'):
        self.name = name
        self.x_label = x_label
        self.y_label = y_label
        self.items = list(args)

    def __getitem__(self, i: int) -> T:
        return self.items.__getitem__(i)

    def __len__(self) -> int:
        return len(self.items)

    def __setitem__(self, key, value):
        self.items[key] = value

    def append(self, *args):
        self.items.append(*args)

    def as_dict(self, skip: list = []) -> dict:
        this_dict = super(DataStore, self).as_dict(self)
        this_dict['items'] = [
            item.as_dict() for item in self.items if hasattr(item, 'as_dict')
        ]

    @classmethod
    def from_dict(cls, d):
        items = d['items']
        del d['items']
        obj = cls.from_dict(d)
        decoder = MontyDecoder()
        obj.items = [decoder.process_decoded(item) for item in items]
        return obj


class DataSet1D(MSONable):
    
    def __init__(self, name: str = 'Series',
                 x: Union[np.ndarray, list] = None, y: Union[np.ndarray, list] = None):
        if x is None:
            x = np.array([])
        if y is None:
            y = np.array([])
        self.name = name
        if not isinstance(x, np.ndarray):
            x = np.array(x)
        if not isinstance(y, np.ndarray):
            y = np.array(y)
            
        self.x = x
        self.y = y
        self._color = None

    def __repr__(self) -> str:
        return "1D DataStore of '{:s}' Vs '{:s}' with {} data points".format(self.x_label, self.y_label, len(self.x))
