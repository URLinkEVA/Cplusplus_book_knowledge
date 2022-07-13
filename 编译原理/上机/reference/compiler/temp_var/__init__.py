from compiler.identifier import Identifier


class TempVar(Identifier):
    def __init__(self, name: str):
        super().__init__(name=name)

    def set_name(self, name):
        self.name = name
        return self

    def set_type(self, type_):
        self.type_ = type_
        return self

    def set_value(self, value):
        self.value = value
        return self
