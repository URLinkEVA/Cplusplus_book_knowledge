from enum import auto, Enum, unique


@unique
class State(Enum):
    SPACE = auto()
    NUM_SIGN = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    MUL = auto()
    ADD = auto()
    COMMA = auto()
    SEMICOLON = auto()
    LESS = auto()
    ASSIGN = auto()
    EQUAL = auto()
    GREATER = auto()
    NOT = auto()

    NUM = auto()
    IDENT_BEGIN = auto()
    IDENT_CHAR = auto()

    CHAR_B = auto()  # begin
    BEGIN_E = auto()
    BEGIN_G = auto()
    BEGIN_I = auto()
    BEGIN_N = auto()
    BOOL_O1 = auto()
    BOOL_O2 = auto()
    BOOL_L = auto()
    DO_D = auto()  # do
    DO_O = auto()
    CHAR_E = auto()  # else, end
    ELSE_L = auto()  # else
    ELSE_S = auto()
    ELSE_E = auto()
    END_N = auto()  # end
    END_D = auto()
    CHAR_I = auto()  # int, if
    IF_F = auto()  # if
    INT_N = auto()  # int
    INT_T = auto()
    THEN_T = auto()  # then
    THEN_H = auto()
    THEN_E = auto()
    THEN_N = auto()
    WHILE_W = auto()  # while
    WHILE_H = auto()
    WHILE_I = auto()
    WHILE_L = auto()
    WHILE_E = auto()
