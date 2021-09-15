from frozen_box import freeze, FrozenObject
from frozen_box.exception import FrozenKeyError, FrozenValueError

import pytest


def __getitem__(obj: FrozenObject):
    return obj._data


def test_get_data_illegal():
    frozen = freeze({'value': 1})

    with pytest.raises(FrozenKeyError):
        assert frozen._data['value'] == 1
    with pytest.raises(FrozenKeyError):
        assert getattr(frozen, '_data') == 1
    with pytest.raises(FrozenKeyError):
        assert __getitem__(frozen) == 1


def test_get_data_legal():
    frozen = freeze({'value': 1})

    assert frozen['value'] == 1
    assert frozen.__getitem__('value') == 1
    assert frozen.value == 1
    assert frozen.get('value') == 1
    assert frozen.get('value2') is None


def test_set_data():
    frozen = freeze({'value': 1})

    with pytest.raises(FrozenValueError):
        frozen['value'] = 2
    with pytest.raises(FrozenValueError):
        frozen.value = 2
