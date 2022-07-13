from compiler.utils import *

# <程序> → <变量说明部分>;<语句部分>
# <变量说明部分> → int<标识符列表>
# <标识符列表> → <标识符><标识符列表prime>
# <标识符列表prime> → ,<标识符><标识符列表prime>|ε
# <语句部分> → <语句>;<语句部分prime>
# <语句部分prime> → <语句>;<语句部分prime>|ε
# <语句> → <赋值语句>|<条件语句>|<循环语句>
# <赋值语句> → <标识符>=<表达式>
# <条件语句> → if （<条件>） then <嵌套语句>; else <嵌套语句>
# <循环语句> → while （<条件>） do <嵌套语句>
# <表达式> → <项><表达式prime>
# <表达式prime> → +<项><表达式prime>|ε
# <项> → <因子><项prime>
# <项prime> → *<因子><项prime>|ε
# <因子> → <标识符>|<常量>|(<表达式>)
# <条件> → <表达式><关系运算符><表达式>
# <嵌套语句> → <语句>|<复合语句>
# <复合语句> → begin <语句部分> end
from compiler.identifier import Identifier


class SyntaxAnalyzer:
    def __init__(self, lexicalAnalyzer, identifierTable, codeTable, tempVarTable):
        self.lexicalAnalyzer = lexicalAnalyzer
        self.identifierTable = identifierTable
        self.codeTable = codeTable
        self.tempVarTable = tempVarTable
        self.have_error = False
        # self.next_word  # 下一个等待匹配的词 <词, 类型>
        # self.next_type  # 下一个等待匹配的词 <词, 类型>

        _, self.next_word, self.next_type = self.lexicalAnalyzer.getNextWord()

    def parseProgram(self):
        print("【语】推导：<程序> -> <变量说明部分>;<语句部分>")
        self.parseExplainVars()
        self.match_word(SYMBOL_SEMICOLON)
        self.parseStatementSection()
        if self.have_error:
            print("[语法错误]: 解析程序失败!")
        print("语法分析结束")

    def parseExplainVars(self):
        print("【语】推导：<变量说明部分> → int<标识符列表>")
        self.match_word(WORD_INT)
        self.parseIdentifierList(WORD_INT)

    def parseIdentifierList(self, identifierType):
        print("【语】推导：<标识符列表> → <标识符><标识符列表prime>")
        if self.next_type == IDENTIFIER:
            self.identifierTable.addIdentifier(self.next_word)
            self.identifierTable.updateIdentifierType(self.next_word, getTypenameByID(identifierType))
            self.match_word(IDENTIFIER)
        self.parseIdentifierListPrime(identifierType)

    def parseIdentifierListPrime(self, identifierType):
        print("【语】推导：<标识符列表prime> → ,<标识符><标识符列表prime>|ε")
        if self.next_type != SYMBOL_COMMA:
            return
        self.match_word(SYMBOL_COMMA)
        if self.next_type == IDENTIFIER:
            identifierName = self.next_word
            if self.identifierTable.existIdentifier(identifierName):
                print("[语义错误]: 这里 " + self.lexicalAnalyzer.getCur() \
                      + ". 标识符 '" + identifierName + "' 重定义!")
            else:
                self.identifierTable.addIdentifier(identifierName)
                self.identifierTable.updateIdentifierType(identifierName, getTypenameByID(identifierType))
            self.match_word(IDENTIFIER)
        self.parseIdentifierListPrime(identifierType)

    def parseStatementSection(self):
        print("【语】推导：<语句部分> → <语句>;<语句部分prime>")
        self.parseStatement()
        self.match_word(SYMBOL_SEMICOLON)
        self.parseStatementSectionPrime()

    def parseStatementSectionPrime(self):
        print("【语】推导：<语句部分prime> → <语句>;<语句部分prime>|ε")
        if self.next_type != IDENTIFIER and self.next_type != WORD_IF and self.next_type != WORD_WHILE:
            return
        self.parseStatement()
        self.match_word(SYMBOL_SEMICOLON)
        self.parseStatementSectionPrime()

    def parseStatement(self):
        print("【语】推导：<语句> → <赋值语句>|<条件语句>|<循环语句>")
        if self.next_type == IDENTIFIER:
            self.parseAssignStatement()
        elif (self.next_type == WORD_IF):
            self.parseIfStatement()
        elif (self.next_type == WORD_WHILE):
            self.parseWhileStatement()

    def parseAssignStatement(self):
        print("【语】推导：<赋值语句> → <标识符>=<表达式>")
        # 由于只有 self.next_type == IDENTIFIER 才会调用该函数，故不需要再次判断
        identifierName = self.next_word
        identifierType = self.identifierTable.getIdentifier(self.next_word).type
        if not self.identifierTable.existIdentifier(identifierName):
            print("[语义错误]: 这里 " + self.lexicalAnalyzer.getCur() \
                  + ". 标识符 '" + identifierName + "' 未定义!")
        self.match_word(IDENTIFIER)
        self.match_word(SYMBOL_ASSIGN)
        E = self.parseExpression()
        # 赋值并产生四元式，若类型不符则报错
        if E.type == identifierType:
            self.codeTable.addQuaternary("=", E.name, "null", identifierName)
            self.identifierTable.updateIdentifierValue(identifierName, E.value)
        else:
            print("[语义错误]: 这里 " + self.lexicalAnalyzer.getCur() \
                  + ". When assigning a value to " + identifierName \
                  + ". Expect type '" + identifierType \
                  + "', but got '" + E.type + "'")

    def parseIfStatement(self):
        print("【语】推导：<条件语句> → if （<条件>） then <嵌套语句>; else <嵌套语句>")
        self.match_word(WORD_IF)
        self.match_word(SYMBOL_LPAREN)
        E = self.parseCondition()
        self.match_word(SYMBOL_RPAREN)
        self.match_word(WORD_THEN)

        self.codeTable.addQuaternary("jnz", E.name, "null", str(self.codeTable.NXQ() + 2))
        # 假出口
        falseExitIndex = self.codeTable.NXQ()
        self.codeTable.addQuaternary("j", "null", "null", "0")

        self.parseNestedStatement()
        exitIndex = self.codeTable.NXQ()
        self.codeTable.addQuaternary("j", "null", "null", "0")
        # 回填假出口
        self.codeTable.updateResultByIndex(falseExitIndex, str(self.codeTable.NXQ()))
        self.match_word(SYMBOL_SEMICOLON)
        self.match_word(WORD_ELSE)
        self.parseNestedStatement()
        # 回填真出口
        self.codeTable.updateResultByIndex(exitIndex, str(self.codeTable.NXQ()))

    def parseWhileStatement(self):
        print("【语】推导：<循环语句> → while （<条件>） do <嵌套语句>")
        self.match_word(WORD_WHILE)
        self.match_word(SYMBOL_LPAREN)

        nextIndex = self.codeTable.NXQ()
        E = self.parseCondition()
        self.codeTable.addQuaternary("jnz", E.name, "null", str(self.codeTable.NXQ() + 2))
        # 假出口，需要回填
        falseExitIndex = self.codeTable.NXQ()
        self.codeTable.addQuaternary("j", "null", "null", "0")

        self.match_word(SYMBOL_RPAREN)
        self.match_word(WORD_DO)
        self.parseNestedStatement()

        self.codeTable.addQuaternary("j", "null", "null", str(nextIndex))
        self.codeTable.updateResultByIndex(falseExitIndex, str(self.codeTable.NXQ()))

    def parseExpression(self):
        print("【语】推导：<表达式> → <项><表达式prime>")
        E = self.parseItem()
        return self.parseExpressionPrime(E)

    def parseExpressionPrime(self, E1):
        print("【语】推导：<表达式prime> → +<项><表达式prime>|ε")
        if self.next_type != SYMBOL_ADD:
            return E1

        self.match_word(SYMBOL_ADD)
        E2 = self.parseItem()
        E3 = E2 + E1
        E3.name = self.tempVarTable.getNewTempVarName()  # E3是申请的一个新临时变量
        self.codeTable.addQuaternary("+", E1.name, E2.name, E3.name)
        return self.parseExpressionPrime(E3)

    def parseItem(self):
        print("【语】推导：<项> → <因子><项prime>")
        E = self.parseFactor()
        return self.parseItemPrime(E)

    def parseItemPrime(self, E1):
        print("【语】推导：<项prime> → *<因子><项prime>|ε")
        if self.next_type != SYMBOL_MUL:
            return E1

        self.match_word(SYMBOL_MUL)
        E2 = self.parseFactor()
        E3 = E2 * E1
        E3.name = self.tempVarTable.getNewTempVarName()  # E3是申请的一个新临时变量
        self.codeTable.addQuaternary("*", E1.name, E2.name, E3.name)
        return self.parseItemPrime(E3)

    def parseFactor(self):
        print("【语】推导：<因子> → <标识符>|<常量>|(<表达式>)")

        E = None
        if self.next_type == IDENTIFIER:
            E = self.identifierTable.getIdentifier(self.next_word)
            self.match_word(IDENTIFIER)
        elif self.next_type == NUM:
            E = Identifier(self.next_word, getTypenameByID(WORD_INT), self.next_word)
            self.match_word(NUM)
        else:
            self.match_word(SYMBOL_LPAREN)
            E = self.parseExpression()
            self.match_word(SYMBOL_RPAREN)
        return E

    def parseCondition(self):
        print("【语】推导：<条件> → <表达式><关系运算符><表达式>")

        E1: Identifier = self.parseExpression()
        op: str = getTypenameByID(self.next_type)
        temp = ""
        if SYMBOL_LT <= self.next_type <= SYMBOL_EQ:
            self.match_word(self.next_type)
        E2 = self.parseExpression()

        if op == "==":
            temp = "true" if E1 == E2 else "false"
        elif op == "!=":
            temp = "true" if E1 != E2 else "false"
        elif op == "<":
            temp = "true" if E1 < E2 else "false"
        elif op == ">":
            temp = "true" if E1 > E2 else "false"
        elif op == "<=":
            temp = "true" if E1 <= E2 else "false"
        elif op == ">=":
            temp = "true" if E1 >= E2 else "false"

        E3 = Identifier(self.tempVarTable.getNewTempVarName(), "bool", temp)
        self.codeTable.addQuaternary(op, E1.name, E2.name, E3.name)
        return E3

    def parseNestedStatement(self):
        print("【语】推导：<嵌套语句> → <语句>|<复合语句>")
        if self.next_type == WORD_BEGIN:
            self.parseCompoundStatement()
        else:
            self.parseStatement()

    def parseCompoundStatement(self):
        print("【语】推导：<复合语句> → begin <语句部分> end")
        self.match_word(WORD_BEGIN)
        self.parseStatementSection()
        self.match_word(WORD_END)

    def match_word(self, expected_type):
        if self.next_type != expected_type:
            print("[语法错误]: 这里 " + self.lexicalAnalyzer.getCur() \
                  + ". Expect type '" + getTypenameByID(expected_type) \
                  + "', but got '" + self.next_word + "'")
            self.have_error = True
        _, self.next_word, self.next_type = self.lexicalAnalyzer.getNextWord()
