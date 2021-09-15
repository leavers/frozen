class FrozenException(Exception):
    pass


class FrozenKeyError(FrozenException, KeyError):
    pass


class FrozenValueError(FrozenException, ValueError):
    pass
