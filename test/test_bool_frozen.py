from frozen_box import FrozenBool


def test_bool_frozen():
    frz = FrozenBool(True)
    ref = bool(True)
    assert frz == ref

    frz = FrozenBool(False)
    ref = bool(False)
    assert frz == ref

    frz = FrozenBool(1)
    ref = bool(1)
    assert frz == ref

    frz = FrozenBool(0)
    ref = bool(0)
    assert frz == ref

    frz = FrozenBool(-1)
    ref = bool(-1)
    assert frz == ref

    frz = FrozenBool('True')
    ref = bool('True')
    assert frz == ref

    frz = FrozenBool('False')
    ref = bool('False')
    assert frz == ref

    frz = FrozenBool('')
    ref = bool('')
    assert frz == ref

    frz = FrozenBool([])
    ref = bool([])
    assert frz == ref

    frz = FrozenBool([1, 2, 4])
    ref = bool([1, 2, 4])
    assert frz == ref

    frz = FrozenBool(())
    ref = bool(())
    assert frz == ref

    frz = FrozenBool((1, 2, 4))
    ref = bool((1, 2, 4))
    assert frz == ref

    frz = FrozenBool({})
    ref = bool({})
    assert frz == ref

    frz = FrozenBool({1: 1, 2: 2, 4: 4})
    ref = bool({1: 1, 2: 2, 4: 4})
    assert frz == ref

    frz = FrozenBool(set())
    ref = bool(set())
    assert frz == ref

    frz = FrozenBool({1, 2, 4})
    ref = bool({1, 2, 4})
    assert frz == ref
