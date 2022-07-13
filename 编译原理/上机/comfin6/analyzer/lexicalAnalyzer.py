from compiler.utils import *


# 词法分析
class LexicalAnalyzer:
    def __init__(self, source=None):
        self.source = source if source is not None else ""
        self.ptr = 0

    @staticmethod
    def is_letter(ch):
        return 'a' <= ch <= 'z' or 'A' <= ch <= 'Z'

    @staticmethod
    def is_digit(ch):
        return '0' <= ch <= '9'

    @staticmethod
    def is_legal_symbol(ch):
        return ch in legal_symbols

    @staticmethod
    def start_type(ch):  # 指出由词首字符推理得出的当前词的可能类型
        if LexicalAnalyzer.is_letter(ch): return WORD
        if LexicalAnalyzer.is_digit(ch): return NUM
        if LexicalAnalyzer.is_legal_symbol(ch): return SYMBOL
        if ch == '$': return IDENTIFIER
        return -1

    def ptr_arrive_end(self, p):
        return p == len(self.source) or self.source[p] == '#'

    @staticmethod
    def is_reserved_words(str_):
        return str_ in reserved_words.keys()

    def getCur(self):
        return self.ptr

    def getNextWord(self):
        while not self.ptr_arrive_end(self.ptr) and self.source[self.ptr] in ignore_symbols:
            self.ptr += 1  # 忽略可忽略字符，并且指针没到文末
        if self.ptr_arrive_end(self.ptr):
            if self.source[self.ptr] != '#':
                print("[Warning]: 没有更多词!")
                return False, "", 0
            else:
                print("【词】(#, #)")
                print("词法分析结束")
                return True, '#', -1

        def WORD_():
            len_ = 1
            sub_word = self.source[self.ptr: self.ptr + len_]
            # 如果还不是关键字，则需要继续拼下一个字符
            # 防越界
            # 字符合法
            while not self.is_reserved_words(sub_word) and \
                    not self.ptr_arrive_end(self.ptr + len_) and \
                    self.is_letter(self.source[self.ptr + len_]):
                len_ += 1
                sub_word = self.source[self.ptr: self.ptr + len_]

            if not self.is_reserved_words(sub_word):
                # 处理匹配结束但非法情况
                print("[词法错误]: 这里 " + str(self.ptr) + ". '" + sub_word + \
                      "' 不是一个保留字! 采取忽视!")
                self.ptr += len_
                return "", 0

            lv2_type = reserved_words[sub_word]
            print("【词】(保留字" + sub_word + ", " + sub_word + ")")

            return sub_word, lv2_type, len_

        def NUM_():
            len_ = 1
            sub_word = self.source[self.ptr: self.ptr + len_]
            # 防越界
            # 字符合法，可以拼成更长的数字序列
            while not self.ptr_arrive_end(self.ptr + len_) and \
                    self.is_digit(self.source[self.ptr + len_]):
                len_ += 1
                sub_word = self.source[self.ptr: self.ptr + len_]
            print("【词】(常量, " + sub_word + ")")

            return sub_word, NUM, len_

        def SYMBOL_():
            len_ = 1
            sub_word = self.source[self.ptr: self.ptr + len_]
            # 防越界
            # 字符合法，考虑 "!=", ">=", "<=", "=="
            while not self.ptr_arrive_end(self.ptr + len_) and \
                    self.source[self.ptr + len_] == '=':
                len_ += 1
                sub_word = self.source[self.ptr: self.ptr + len_]

            lv2_type = reserved_symbols[sub_word][0]
            print("【词】(" + reserved_symbols[sub_word][1] + ", " + sub_word + ")")
            return sub_word, lv2_type, len_

        def IDENTIFIER_():
            len_ = 1
            sub_word = self.source[self.ptr: self.ptr + len_]
            # 防越界
            # 变量名由$开头，并由字母或数字组成
            while not self.ptr_arrive_end(self.ptr + len_) and \
                    (self.is_letter(self.source[self.ptr + len_]) or
                     self.is_digit(self.source[self.ptr + len_])):
                len_ += 1
                sub_word = self.source[self.ptr: self.ptr + len_]

            print("【词】(标识符, " + sub_word + ")")
            return sub_word, IDENTIFIER, len_

        method2 = {
            WORD: WORD_,
            NUM: NUM_,
            SYMBOL: SYMBOL_,
            IDENTIFIER: IDENTIFIER_
        }

        # 枚举长度向后拼接，并输出二元式
        lv1_type = self.start_type(self.source[self.ptr])

        try:
            res, lv2_type, len_ = method2[lv1_type]()
        except Exception as e:
            print(e)
            print("[词法错误]: 这里 " + str(self.ptr) + ". '" + self.source[self.ptr] + "' 不合法!")
            self.ptr += 1
            return False, "", 0

        type_ = lv2_type if lv2_type is None or lv2_type != 0 else lv1_type
        self.ptr += len_

        return True, res, type_
