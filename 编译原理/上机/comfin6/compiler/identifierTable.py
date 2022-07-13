from compiler import identifier
from compiler.utils import *
from compiler.identifier import Identifier


class IdentifierTable:
    def __init__(self):
        self.table: dict = {}

    def addIdentifier(self, name):
        if self.existIdentifier(name):
            return False
        self.table[name] = Identifier(name, "", "")
        # print(str(self.table[name]))
        return True

    def clearTable(self):
        self.table.clear()

    def dumpTable(self):
        res = ""
        for k in self.table.keys():
            print(k, self.table[k])
            res += k + str(self.table[k]) + "\n"
        return res

    def existIdentifier(self, name):
        return name in self.table.keys()

    def updateIdentifierType(self, name, type_):
        if not self.existIdentifier(name):
            return False
        self.table[name].type = type_
        if type_ == getTypenameByID(WORD_INT):
            self.table[name].value = "0"
        return True

    def updateIdentifierValue(self, name, value):
        if not self.existIdentifier(name):
            return False
        self.table[name].value = value
        return True

    def getIdentifier(self, name):
        if not self.existIdentifier(name):
            return Identifier("", "", "")
        return self.table[name]
