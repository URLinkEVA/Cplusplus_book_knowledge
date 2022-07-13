from compiler import utils


class TempVarTable:
    def __init__(self):
        self.table = []

    def getNewTempVarName(self):
        name = "T" + str(len(self.table) + 1)
        self.table.append(name)
        return name

    def dumpTable(self):
        res = "["
        for i in self.table:
            res += i + ", "
        return res + "]\n"
