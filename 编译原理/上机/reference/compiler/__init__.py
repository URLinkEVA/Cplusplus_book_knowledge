from compiler.identifier.identifier_table import IdentifierTable
from compiler.lexical_analysis import LexicalAnalysis
from compiler.quadruple.intermediate_code_table import IntermediateCodeTable
from compiler.syntactic_analysis import SyntacticAnalysis
from compiler.temp_var.temp_var_table import TempVarTable


class Compiler:
    def __init__(self, program: str):
        self.program = program
        self.identifier_table = IdentifierTable()
        self.intermediate_code_table = IntermediateCodeTable()

    def compile(self):
        lexical_analysis_ = LexicalAnalysis(self.program, self.identifier_table)
        syntactic_analysis_ = SyntacticAnalysis(lexical_analysis_, self.identifier_table, self.intermediate_code_table)
        syntactic_analysis_.parse_program()

        # print(self.identifier_table)
        with open("out.txt", "w") as file:
            file.write(str(self.intermediate_code_table))
