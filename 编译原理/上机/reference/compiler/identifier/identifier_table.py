from typing import List

from compiler.identifier import Identifier
from compiler.utils import Singleton


class IdentifierTable(metaclass=Singleton):
    def __init__(self):
        self.table: List[Identifier] = list()
        self.pop = ""

    def __str__(self):
        return "\n".join([str(ident) for ident in self.table])

    def exist_identifier(self, name: str) -> bool:
        return name in [e.name for e in self.table]

    def pop_duplicate_identifier(self) -> str:
        ret: str = self.pop
        self.pop = ""
        return ret

    def add(self, name: str):
        if self.exist_identifier(name):
            self.pop = name
            return False
        self.table.append(Identifier(name, value="0"))
        return True

    def clear(self):
        self.table.clear()

    def get_identifier_idx(self, name: str) -> int:
        for idx, e in enumerate(self.table):
            if e.name == name:
                return idx

        return -1

    def set_identifier_type(self, name: str, type_: str) -> bool:
        idx: int = self.get_identifier_idx(name)
        if idx == -1:
            return False
        else:
            self.table[idx].type_ = type_
            return True

    def set_identifier_value(self, name: str, value: str) -> bool:
        idx: int = self.get_identifier_idx(name)
        if idx == -1:
            return False
        else:
            self.table[idx].value = value
            return True

    def get_identifier_value(self, name: str) -> str:
        idx: int = self.get_identifier_idx(name)
        if idx == -1:
            raise Exception("找不到标识符")
        else:
            return self.table[idx].value

    def get_identifier_value_as_int(self, name: str) -> int:
        return self.get_identifier_value_as_int(name)

    def get_identifier(self, name: str) -> Identifier:
        for e in self.table:
            if e.name == name:
                return e
        raise Exception("找不到标识符")
