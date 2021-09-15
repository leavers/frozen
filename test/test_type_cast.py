from frozen_box import (
    FrozenBool,
    FrozenInt,
    FrozenFloat,
    FrozenComplex,
    FrozenFrozenSet,
    FrozenStr,
    FrozenBytes,
    FrozenObject,
)


def test_cast_bool():
    a = FrozenBool(True)
    b = FrozenBool(a)
    assert a == b
    assert type(a) == type(b)


def test_cast_int():
    a = FrozenInt(1)
    b = FrozenInt(a)
    assert a == b
    assert type(a) == type(b)


def test_cast_float():
    a = FrozenFloat(3.14)
    b = FrozenFloat(a)
    assert a == b
    assert type(a) == type(b)


def test_cast_complex():
    a = FrozenComplex(1 + 2j)
    b = FrozenComplex(a)
    assert a == b
    assert type(a) == type(b)


def test_cast_frozenset():
    a = FrozenFrozenSet(frozenset({1, 2, 4}))
    b = FrozenFrozenSet(a)
    assert a == b
    assert type(a) == type(b)


def test_cast_str():
    a = FrozenStr('hello world')
    b = FrozenStr(a)
    assert a == b
    assert type(a) == type(b)


def test_cast_bytes():
    a = FrozenBytes(b'hello world')
    b = FrozenBytes(a)
    assert a == b
    assert type(a) == type(b)


def test_frozen_object():
    a = FrozenObject([1, 2, 3])
    b = FrozenObject(a)
    assert a == b
    assert type(a) == type(b)
