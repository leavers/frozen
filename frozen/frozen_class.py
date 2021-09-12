from typing import List, Union, Sequence
from abc import abstractmethod, ABC
from copy import deepcopy

from frozen.exception import FrozenKeyError, FrozenValueError

QueryableItem = Union[str, int, slice]
Queryable = Union[QueryableItem, Sequence[QueryableItem]]


class Frozen(ABC):
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def unpack(self):
        raise NotImplementedError()


class _FrozenBool(Frozen, int):
    def __init__(self, value, **kwargs):
        value = 1 if value else 0
        super().__init__(value, **kwargs)

    def __bool__(self):
        return True.__bool__() if self != 0 else False.__bool__()

    def __str__(self):
        return True.__str__() if self != 0 else False.__bool__()

    def __repr__(self):
        return True.__repr__() if self != 0 else False.__repr__()

    def unpack(self):
        return bool(self)


def _make_frozen_bool(value):
    return _FrozenBool(1 if value else 0)


def _simple_frozen_class(name: str, cls: type):
    return type(
        name,
        (Frozen, cls),
        {'unpack': lambda s: cls(s)}
    )


FrozenBool = _make_frozen_bool
FrozenInt = _simple_frozen_class('FrozenInt', int)
FrozenFloat = _simple_frozen_class('FrozenFloat', float)
FrozenComplex = _simple_frozen_class('FrozenComplex', complex)
FrozenFrozenSet = _simple_frozen_class('FrozenFrozenSet', frozenset)
FrozenStr = _simple_frozen_class('FrozenFrozenSet', str)
FrozenBytes = _simple_frozen_class('FrozenBytes', bytes)

_simple_types = (
    bool,
    int,
    float,
    complex,
    frozenset,
    str,
    bytes,
)
_simple_classes = (
    FrozenBool,
    FrozenInt,
    FrozenFloat,
    FrozenComplex,
    FrozenFrozenSet,
    FrozenStr,
    FrozenBytes,
)


class _Carrier:
    __slots__ = ('data',)

    def __init__(self, data):
        self.data = data


class FrozenObject(Frozen):

    def __init__(self, data):
        super().__init__()
        # TODO: make self._data more secure
        t = type(data)
        if t == _Carrier:
            self._data = data.data
        elif t == FrozenObject:
            self._data = data._data
        else:
            try:
                idx = _simple_classes.index(t)
                self._data = _simple_types[idx](data)
            except ValueError:
                self._data = deepcopy(data)

    @classmethod
    def _cast(cls, value: str) -> Union[str, float]:
        if not value:
            return value
        try:
            res = int(value)
        except ValueError:
            res = value
        return res

    @classmethod
    def _convert(cls, value: str):
        if ':' in value:
            items = value.split(':')
            for i, item in enumerate(items):
                casted = cls._cast(item)
                items[i] = casted if casted else None
            res = slice(*items)
        else:
            res = cls._cast(value)
        return res

    @classmethod
    def _freeze(cls, data):
        try:
            idx = _simple_types.index(type(data))
            return _simple_classes[idx](data)
        except ValueError:
            return cls(_Carrier(data))

    @classmethod
    def _split_queries(cls, query: str) -> List[Queryable]:
        if not query:
            raise FrozenValueError('Param "query" is empty')
        length = len(query)
        if length == 1:
            return [query]
        seq = []
        start, i = 0, 0
        item = ''
        # TODO: switch escaping char from '.' to '`'
        while i < length:
            if query[i] == '.':
                if i + 1 < length and query[i + 1] == '.':
                    i += 1
                    item += query[start:i]
                else:
                    item += query[start:i]
                    seq.append(cls._convert(item))
                    item = ''
                i += 1
                start = i
            else:
                i += 1
        if start < length:
            item += query[start:]
        seq.append(cls._convert(item))
        return seq

    @classmethod
    def _getitem(cls, data, item: QueryableItem):
        if isinstance(item, (int, slice)):
            return data.__getitem__(item)
        elif isinstance(item, str):
            try:
                return data.__getitem__(item)
            except KeyError:
                try:
                    return getattr(data, item)
                except KeyError:
                    raise FrozenKeyError(item)

    def __getitem__(self, query: Queryable) -> Frozen:
        if isinstance(query, slice):
            data = self._data.__getitem__(query)
        elif isinstance(query, int):
            data = self._data.__getitem__(query)
        elif isinstance(query, str):
            queries = self._split_queries(query)
            data = self._data
            for q in queries:
                data = self._getitem(data, q)
        else:
            raise FrozenKeyError(f'Type {type(query)} is not queryable')
        return self._freeze(data)

    def __eq__(self, other):
        if isinstance(other, FrozenObject):
            if id(self) == id(other):
                return True
            if self._data == other._data:
                return True
            return False
        return False

    def unpack(self):
        return deepcopy(self._data)


def freeze(data):
    try:
        if isinstance(data, Frozen):
            return type(data)(data)
        idx = _simple_types.index(type(data))
        return _simple_classes[idx](data)
    except ValueError:
        return FrozenObject(data)
