from typing import List

from compiler.quadruple import Quadruple
from compiler.utils import Singleton


class IntermediateCodeTable(metaclass=Singleton):
    def __init__(self):
        self.table: List[Quadruple] = list()

    def __str__(self):
        return "\n".join([f"{index}: {quadruple}" for index, quadruple in enumerate(self.table)])

    def add(self, quadruple: Quadruple):
        self.table.append(quadruple)

    def clear(self):
        self.table.clear()

    def next_quadruple_index(self) -> int:
        return len(self.table)

    def back_end(self, index: int, res: str):
        self.table[index].res = res
