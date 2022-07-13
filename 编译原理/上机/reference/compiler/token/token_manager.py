from compiler.token import Token


class TokenManager:
    data = {
        " ": "空格",

        "#": "井号",
        "(": "左括号",
        ")": "右括号",
        "*": "乘号",
        "+": "加号",
        ",": "逗号",
        ";": "分号",
        "<": "关系运算符",
        ">": "关系运算符",

        "=": "赋值号",
        "==": "关系运算符",
        "!=": "关系运算符",
        "<=": "关系运算符",
        ">=": "关系运算符",

        "begin": "begin",
        "bool": "bool",
        "do": "do",
        "else": "else",
        "end": "end",
        "if": "if",
        "int": "int",
        "then": "then",
        "while": "while"
    }

    @staticmethod
    def convert(cls: Token) -> Token:
        name, value = cls.name, cls.value
        if value in TokenManager.data.keys():
            return Token(TokenManager.data[value], value)
        else:
            return cls

    @staticmethod
    def match_type(cls: Token, value) -> bool:
        if value in TokenManager.data.keys():
            return cls.name == TokenManager.data[value]
        else:
            return cls.name == value
