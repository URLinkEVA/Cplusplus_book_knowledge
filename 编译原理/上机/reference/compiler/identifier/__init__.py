class Identifier:
    def __init__(self, name="", type_="", value=""):
        self.name: str = name
        self.type_: str = type_
        self.value: str = value

    def __str__(self):
        return f"name: {self.name}, type: {self.type_}, value: {self.value}; "
