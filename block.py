class BadBlockError(Exception):
    ...


class Block:
    def __init__(self, index: tuple[int, int], value: int, removable=False) -> None:
        self._index = index
        self._removable = removable
        if index[0] not in range(9) or index[1] not in range(9) or value not in range(10):
            raise BadBlockError("Bad block")

        self._value = value

    def get_index(self) -> tuple[int, int]:
        return self._index

    def is_removable(self) -> bool:
        return self._removable

    def set_removable(self, removable: bool) -> None:
        self._removable = removable

    def __getitem__(self, index: int) -> int:
        return self._index[index]

    def get_value(self) -> int:
        return self._value

    def set_value(self, value: int) -> None:
        self._value = value

    def get_super_block_index(self) -> tuple[int, int]:
        return self._index[0] // 3, self._index[1] // 3

    def __eq__(self, other) -> bool:
        return (self._index == other.get_index()) and (self._value == other.get_value())
