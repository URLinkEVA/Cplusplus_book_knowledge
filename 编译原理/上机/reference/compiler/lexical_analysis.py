from typing import List

from compiler import IdentifierTable
from compiler.token import Token
from compiler.token.state import State
from compiler.token.token_manager import TokenManager
from compiler.utils import Singleton


class LexicalAnalysis(metaclass=Singleton):
    def __init__(self, program: str, identifier_table_: IdentifierTable):
        self.program = program.strip() + "#"
        self.identifier_table = identifier_table_

        self.idx = 0
        self.temp: str = ""
        self.state: State = State.SPACE
        self.symbol: str = ''
        self.next_: bool = False
        self.last_ret_idx: int = 0

    def add_temp(self, state_: State = State.SPACE):
        self.state = state_
        self.temp += self.symbol

    def match_char(self, state_: State, target: str):
        return self.state == state_ and self.symbol == target

    def match_list(self, state_: State, target: List[str]):
        return self.state == state_ and self.symbol in target

    def make_token(self, name: str = "") -> Token:
        self.idx += self.next_
        self.last_ret_idx = self.idx
        return TokenManager.convert(Token(name, self.temp))

    def next_word(self) -> Token:
        self.temp = ""
        self.state = State.SPACE

        while True:
            self.next_ = True
            self.symbol = self.program[self.idx]

            # region Space
            if self.match_char(State.SPACE, ' '):
                pass
            # endregion

            elif self.match_list(State.SPACE, ['#', '(', ')', '*', '+', ',', ';']):
                self.add_temp()
                return self.make_token()

            # region Number
            elif self.state == State.SPACE and self.symbol.isdigit():
                self.add_temp(State.NUM)
            elif self.state == State.NUM:
                if self.symbol.isdigit():
                    self.add_temp(State.NUM)
                else:
                    self.next_ = False
                    return self.make_token("数字")
            # endregion

            # region LessThan and GreaterThan
            elif self.match_char(State.SPACE, '<'):
                self.add_temp(State.LESS)
            elif self.match_char(State.SPACE, '>'):
                self.add_temp(State.GREATER)
            elif self.match_char(State.SPACE, '!'):
                self.add_temp(State.NOT)

            # region Assignment
            elif self.match_char(State.SPACE, '='):
                self.add_temp(State.ASSIGN)
            # endregion
            # region Equal
            elif self.state in [State.ASSIGN, State.LESS, State.GREATER, State.NOT]:
                if self.symbol == '=':
                    self.add_temp()
                    return self.make_token()
                else:
                    self.next_ = False
                    return self.make_token()
            # endregion

            # region Identifier
            elif self.match_char(State.SPACE, '$'):
                self.add_temp(State.IDENT_BEGIN)
            elif self.state == State.IDENT_BEGIN and 'a' <= self.symbol <= 'z' or 'A' <= self.symbol <= 'Z' \
                    or self.symbol.isdigit():
                self.add_temp(State.IDENT_CHAR)
            elif self.state == State.IDENT_CHAR:
                if 'a' <= self.symbol <= 'z' or 'A' <= self.symbol <= 'Z' or self.symbol.isdigit():
                    self.add_temp(State.IDENT_CHAR)
                else:
                    self.next_ = False
                    self.identifier_table.add(self.temp)
                    return self.make_token("标识符")
            # endregion

            # region begin
            elif self.match_char(State.SPACE, 'b'):
                self.add_temp(State.CHAR_B)
            elif self.match_char(State.CHAR_B, 'e'):
                self.add_temp(State.BEGIN_E)
            elif self.match_char(State.BEGIN_E, 'g'):
                self.add_temp(State.BEGIN_G)
            elif self.match_char(State.BEGIN_G, 'i'):
                self.add_temp(State.BEGIN_I)
            elif self.match_char(State.BEGIN_I, 'n'):
                self.add_temp()
                return self.make_token()
            # endregion
            # region do
            elif self.match_char(State.SPACE, 'd'):
                self.add_temp(State.DO_D)
            elif self.match_char(State.DO_D, 'o'):
                self.add_temp()
                return self.make_token()
            # endregion
            # region else
            elif self.match_char(State.SPACE, 'e'):
                self.add_temp(State.CHAR_E)
            elif self.match_char(State.CHAR_E, 'l'):
                self.add_temp(State.ELSE_L)
            elif self.match_char(State.ELSE_L, 's'):
                self.add_temp(State.ELSE_S)
            elif self.match_char(State.ELSE_S, 'e'):
                self.add_temp()
                return self.make_token()
            # endregion
            # region end
            elif self.match_char(State.CHAR_E, 'n'):
                self.add_temp(State.END_N)
            elif self.match_char(State.END_N, 'd'):
                self.add_temp()
                return self.make_token()
            # endregion
            # region int
            elif self.match_char(State.SPACE, 'i'):
                self.add_temp(State.CHAR_I)
            elif self.match_char(State.CHAR_I, 'n'):
                self.add_temp(State.INT_N)
            elif self.match_char(State.INT_N, 't'):
                self.add_temp()
                return self.make_token()
            # endregion
            # region if
            elif self.match_char(State.CHAR_I, 'f'):
                self.add_temp()
                return self.make_token()
            # endregion
            # region elif
            elif self.match_char(State.CHAR_I, 'i'):
                self.add_temp()
                return self.make_token()
            # endregion
            # region then
            elif self.match_char(State.SPACE, 't'):
                self.add_temp(State.THEN_T)
            elif self.match_char(State.THEN_T, 'h'):
                self.add_temp(State.THEN_H)
            elif self.match_char(State.THEN_H, 'e'):
                self.add_temp(State.THEN_E)
            elif self.match_char(State.THEN_E, 'n'):
                self.add_temp()
                return self.make_token()
            # endregion
            # region while
            elif self.match_char(State.SPACE, 'w'):
                self.add_temp(State.WHILE_W)
            elif self.match_char(State.WHILE_W, 'h'):
                self.add_temp(State.WHILE_H)
            elif self.match_char(State.WHILE_H, 'i'):
                self.add_temp(State.WHILE_I)
            elif self.match_char(State.WHILE_I, 'l'):
                self.add_temp(State.WHILE_L)
            elif self.match_char(State.WHILE_L, 'e'):
                self.add_temp()
                return self.make_token()
            # endregion

            # region Unknown
            else:
                print("词法错误")
                print(f"位置：{self.last_ret_idx}")
                print(f"符号：{self.program[self.last_ret_idx]}")
                # 忽略错误，继续扫描
                self.idx = self.last_ret_idx
                self.temp = ""
                self.state = State.SPACE
            # endregion
            self.idx += self.next_
