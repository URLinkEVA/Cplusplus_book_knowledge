class Quadruple:
    def __init__(self, op: str, arg1: str, arg2: str, res: str):
        self.op: str = op
        self.arg1: str = arg1
        self.arg2: str = arg2
        self.res: str = res

    def __str__(self):
        return f"({', '.join([self.op, self.arg1, self.arg2, self.res])})"
