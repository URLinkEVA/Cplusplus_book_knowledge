import time

from analyzer.lexicalAnalyzer import LexicalAnalyzer
from analyzer.syntaxAnalyzer import SyntaxAnalyzer
from compiler.codeTable import CodeTable
from compiler.identifierTable import IdentifierTable
from compiler.tempVarTable import TempVarTable


def get_out():
    default_file = "in.txt"
    with open(default_file, encoding="utf-8") as file:
        source = file.read() + "#"

    print("源代码：\n" + source)

    lexicalanalyzer = LexicalAnalyzer(source)
    identifierTable = IdentifierTable()
    tempVarTable = TempVarTable()
    codeTable  = CodeTable()

    print("\n开始编译...")
    syntaxAnalyzer = SyntaxAnalyzer(lexicalanalyzer, identifierTable, codeTable, tempVarTable)
    syntaxAnalyzer.parseProgram()

    print("\n标识符表：\n" + identifierTable.dumpTable())
    print("临时变量表：\n" + tempVarTable.dumpTable())
    print("四元式表：\n" + codeTable.dumpTable())

    # writer("out.txt", codeTable.dumpTable())
    with open("out.txt", "w", encoding="utf-8") as file:
        file.write(str(codeTable.dumpTable()))

    print("按回车继续")


if __name__ == '__main__':
    get_out()
    input("Press any key to continue")