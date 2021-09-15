from frozen_box import FrozenObject
from frozen_box.exception import FrozenException
import pytest

split = FrozenObject._split_queries


def test_split_simple_query():
    src = 'a'
    res = split(src)
    assert res == ['a']

    src = 'a.b'
    res = split(src)
    assert res == ['a', 'b']

    src = 'a.b.c.d.e'
    res = split(src)
    assert res == ['a', 'b', 'c', 'd', 'e']


def test_split_query():
    # double-dot-escaping will be replaced with '`' in the future
    src = '..l..e..v..e..l..1..'
    res = split(src)
    assert res == ['.l.e.v.e.l.1.']

    src = '..l..e..v..e..l..1...l..e..v..e..l..2..'
    res = split(src)
    assert res == ['.l.e.v.e.l.1.', 'l.e.v.e.l.2.']

    src = 'level 1.level 2.level 3'
    res = split(src)
    assert res == ['level 1', 'level 2', 'level 3']

    src = 'level1.2.3'
    res = split(src)
    assert res == ['level1', 2, 3]

    src = 'level1.-2.-3'
    res = split(src)
    assert res == ['level1', -2, -3]

    src = 'level1.:.name'
    res = split(src)
    assert res == ['level1', slice(None, None, None), 'name']

    src = 'level1.:9.name'
    res = split(src)
    assert res == ['level1', slice(None, 9, None), 'name']

    src = 'level1.-1:.name'
    res = split(src)
    assert res == ['level1', slice(-1, None, None), 'name']

    src = 'level1.-1:9.name'
    res = split(src)
    assert res == ['level1', slice(-1, 9, None), 'name']

    src = 'level1.9:-1:-1.name'
    res = split(src)
    assert res == ['level1', slice(9, -1, -1), 'name']


def test_empty():
    with pytest.raises(FrozenException):
        split('')
