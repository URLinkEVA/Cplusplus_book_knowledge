from compiler import utils
from compiler.utils import *


class Identifier:
    def __init__(self, name, type_, value):
        self.name = name
        self.type = type_
        self.value = value

    @staticmethod
    def isAbleToCal(i1, i2):
        is_ok = (i1.type == getTypenameByID(WORD_INT) or i1.type == getTypenameByID(NUM)) and \
                (i2.type == getTypenameByID(WORD_INT) or i2.type == getTypenameByID(NUM))
        if not is_ok:
            print("[语义错误]: 只能使用重载符")
        return is_ok

    def __str__(self):
        return "name: " + self.name + "  " + \
               "type: " + self.type + "  " + \
               "value: " + self.value

    def __add__(self, i2):
        if not Identifier.isAbleToCal(self, i2):
            return Identifier("", "", "")
        return Identifier("", self.type, str(int(self.value) + int(i2.value)))

    def __mul__(self, i2):
        if not Identifier.isAbleToCal(self, i2):
            return Identifier("", "", "")
        return Identifier("", self.type, str(int(self.value) * int(i2.value)))

    def __eq__(self, i2):
        if not Identifier.isAbleToCal(self, i2):
            return False
        return int(self.value) == int(i2.value)

    def __ne__(self, i2):
        if not Identifier.isAbleToCal(self, i2):
            return False
        return int(self.value) != int(i2.value)

    def __lt__(self, i2):
        if not Identifier.isAbleToCal(self, i2):
            return False
        return int(self.value) < int(i2.value)

    def __gt__(self, i2):
        if not Identifier.isAbleToCal(self, i2):
            return False
        return int(self.value) > int(i2.value)

    def __le__(self, i2):
        if not Identifier.isAbleToCal(self, i2):
            return False
        return int(self.value) <= int(i2.value)

    def __ge__(self, i2):
        if not Identifier.isAbleToCal(self, i2):
            return False
        return int(self.value) >= int(i2.value)
