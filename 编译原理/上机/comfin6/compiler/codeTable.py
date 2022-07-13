from compiler import utils


class Quaternary:
    def __init__(self, op: str, arg1: str, arg2: str, result: str):
        self.op: str = op
        self.arg1: str = arg1
        self.arg2: str = arg2
        self.result: str = result

    def __str__(self):
        return f"({', '.join([self.op, self.arg1, self.arg2, self.result])}"


class CodeTable:

    def __init__(self):
        self.quaternaries = []

    def addQuaternary(self, op, arg1, arg2, result):
        self.quaternaries.append(Quaternary(op, arg1, arg2, result))
        return True

    def NXQ(self):
        return len(self.quaternaries)

    def updateResultByIndex(self, idx, result):
        if 0 > idx >= len(self.quaternaries):
            return False
        self.quaternaries[idx].result = result
        return True

    def clearTable(self):
        self.quaternaries.clear()

    def dumpTable(self):
        res = ""
        for i in range(0, len(self.quaternaries)):
            item = self.quaternaries[i]
            res += "(" + str(i + 1) + ") (" \
                   + item.op + ", " + item.arg1 + ", " + item.arg2 + ", " + item.result + ")\n"
        return res
