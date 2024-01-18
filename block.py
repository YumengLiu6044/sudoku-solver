class Block(object):
    def __init__(self, index: tuple[int, int], value: int):
        self._index = index
        self._value = value

    def get_index(self) -> tuple[int, int]:
        return self._index

    def get_value(self) -> int:
        return self._value

    def __equal__(self, other) -> bool:
        return self._index == other.get_index() and self._value == other.get_value()
