# 类型定义
WORD = 100
WORD_INT = 101
WORD_BEGIN = 102
WORD_END = 103
WORD_IF = 104
WORD_ELSE = 105
WORD_THEN = 106
WORD_WHILE = 107
WORD_DO = 108
NUM = 200
SYMBOL = 300
SYMBOL_ADD = 301
SYMBOL_MUL = 302
SYMBOL_LT = 303
SYMBOL_GT = 304
SYMBOL_LE = 305
SYMBOL_GE = 306
SYMBOL_NE = 307
SYMBOL_EQ = 308
SYMBOL_COMMA = 309
SYMBOL_SEMICOLON = 310
SYMBOL_LPAREN = 311
SYMBOL_RPAREN = 312
SYMBOL_ASSIGN = 313
IDENTIFIER = 400

# 保留字集合，以及到词法类型映射


reserved_words = {"int": WORD_INT,
                  "begin": WORD_BEGIN,
                  "end": WORD_END,
                  "if": WORD_IF,
                  "else": WORD_ELSE,
                  "then": WORD_THEN,
                  "while": WORD_WHILE,
                  "do": WORD_DO}

# 保留符号集合，以及到词法类型映射，附赠词法分析部分的文字描述
reserved_symbols = {"+": (SYMBOL_ADD, "加法运算符"),
                    "*": (SYMBOL_MUL, "乘法运算符"),
                    "<": (SYMBOL_LT, "关系运算符"),
                    ">": (SYMBOL_GT, "关系运算符"),
                    "<=": (SYMBOL_LE, "关系运算符"),
                    ">=": (SYMBOL_GE, "关系运算符"),
                    "!=": (SYMBOL_NE, "关系运算符"),
                    "==": (SYMBOL_EQ, "关系运算符"),
                    ",": (SYMBOL_COMMA, "分隔符逗号"),
                    ";": (SYMBOL_SEMICOLON, "分隔符分号"),
                    "(": (SYMBOL_LPAREN, "左括号"),
                    ")": (SYMBOL_RPAREN, "右括号"),
                    "=": (SYMBOL_ASSIGN, "赋值号")}

legal_symbols = {'+', '*', '<', '>', '!', ',', ';', '(', ')', '='}
ignore_symbols = {' ', '\n', '\t'}


# 工具函数
def getTypenameByID(ID):
    def case1():
        for k in reserved_words.keys():
            if reserved_words[k] == ID:
                return k

    def case2():
        return "Constant"

    def case3():
        for k in reserved_symbols.keys():
            if reserved_symbols[k][0] == ID:
                return k

    def case4():
        return "Identifier"

    def default():
        return "UnknownType"

    methods = {
        1: case1,
        2: case2,
        3: case3,
        4: case4
    }

    try:
        type_ = methods[int(ID / 100)]()
    except Exception as e:
        type_ = default()

    return type_

# def readFile(filePath):
#     ifstream ifs
#     ifs.open(filePath, ios::in)
#
#     if not ifs.is_open():
#         print("[Error]: Open file failed!")
#         return ""
#
#     buf = ""
#     content = ""
#     while getline(ifs, buf):
#         content = content + buf
#
#     ifs.close()
#     return content
#
# def writeFile(filePath, content):
#     ofstream ofs
#     ofs.open(filePath, ios::out)
#     if not ofs.is_open():
#         print("[Error]: Open file failed!")
#         return
#     ofs << content
#     ofs.close()
