from typing import List

from compiler import LexicalAnalysis, IdentifierTable, IntermediateCodeTable
from compiler.identifier import Identifier
from compiler.quadruple import Quadruple
from compiler.temp_var import TempVar
from compiler.temp_var.temp_var_table import TempVarTable
from compiler.token.token_manager import TokenManager
from compiler.utils import Singleton


class SyntacticAnalysis(metaclass=Singleton):
    def __init__(self, lexical_analysis: LexicalAnalysis,
                 identifier_table: IdentifierTable,
                 intermediate_code_table: IntermediateCodeTable):
        self.lexical_analysis = lexical_analysis
        self.identifier_table = identifier_table
        self.intermediate_code_table = intermediate_code_table

        self.word = self.lexical_analysis.next_word()
        self.lexical_logs: List[str] = []
        self.syntactic_logs: List[str] = []

    def match(self, type_: str):
        if self.word.value == "#":
            return
        else:
            if not TokenManager.match_type(self.word, type_):
                error_info = f"语法错误\n" \
                             f"位置：{self.lexical_analysis.idx}\n" \
                             f"符号：{self.lexical_analysis.symbol}"
                raise Exception(error_info)
            else:
                self.lexical_logs.append(str(self.word))
                self.word = self.lexical_analysis.next_word()

    def parse_program(self):
        self.syntactic_logs.append("<程序> →<变量说明部分>;<语句部分>")
        self.parse_variable_declaration_section()
        self.match(";")
        self.parse_statement_section()

        def print_logs(logs):
            for log in logs:
                print(log)
            print()

        print_logs(self.lexical_logs)
        print_logs(self.syntactic_logs)

    def parse_variable_declaration_section(self):
        self.syntactic_logs.append("<变量说明部分> → <变量说明><标识符列表>")
        type_: str = self.parse_variable_declaration()
        self.parse_identifier_list(type_)

    def parse_variable_declaration(self) -> str:
        self.syntactic_logs.append("<变量说明> → int")
        type_ = self.word.value
        if type_ != "int":
            raise Exception("变量类型错误")
        self.match("int")
        return "int"

    def parse_identifier_list(self, type_: str):
        self.syntactic_logs.append("<标识符列表> → <标识符><标识符列表prime>")
        self.identifier_table.set_identifier_type(self.word.value, "int")
        print(f"更新标识符{self.word.value}类型为 int")
        self.parse_identifier()
        self.parse_identifier_list_prime(type_)

    def parse_identifier_list_prime(self, type_: str):
        self.syntactic_logs.append("<标识符列表prime>→ ,<标识符><标识符列表prime>|ε")
        if TokenManager.match_type(self.word, ","):
            self.match(",")
            if TokenManager.match_type(self.word, "标识符"):
                duplicate_identifier = self.identifier_table.pop_duplicate_identifier()
                if duplicate_identifier:
                    error_info = f"重复定义错误\n" \
                                 f"位置：{self.lexical_analysis.idx - len(duplicate_identifier)}\n" \
                                 f"标识符：{duplicate_identifier}"
                    raise Exception(error_info)

                self.identifier_table.set_identifier_type(self.word.value, "int")
                print(f"更新标识符{self.word.value}类型为 int")
                self.parse_identifier()
            self.parse_identifier_list_prime(type_)
        else:
            pass

    def parse_identifier(self) -> str:
        self.syntactic_logs.append("<标识符> → $<字母>|<标识符><字母>|<标识符><数字>")
        ident_name: str = self.word.value
        self.match("标识符")
        return ident_name

    def parse_statement_section(self):
        self.syntactic_logs.append("<语句部分>→<语句>;<语句部分prime>")
        self.parse_statement()
        self.match(";")
        self.parse_statement_section_prime()

    def parse_statement_section_prime(self):
        self.syntactic_logs.append("<语句部分prime>→<语句>;语句部分prime>|ε")
        if TokenManager.match_type(self.word, "标识符") \
                or TokenManager.match_type(self.word, "if") or TokenManager.match_type(self.word, "while"):
            self.parse_statement()
            self.match(";")
            self.parse_statement_section_prime()
        else:
            pass

    def parse_statement(self):
        self.syntactic_logs.append("<语句> → <赋值语句>|<条件语句>|<循环语句>")
        if TokenManager.match_type(self.word, "标识符"):
            self.parse_assignment_statement()
        elif TokenManager.match_type(self.word, "if"):
            self.parse_conditional_statement()
        elif TokenManager.match_type(self.word, "while"):
            self.parse_loop_statement()
        else:
            raise Exception("语句错误")

    def parse_assignment_statement(self):
        self.syntactic_logs.append("<赋值语句> → <标识符>=<表达式>")
        ident_name: str = self.word.value
        self.parse_identifier()
        self.match("=")
        temp_var: Identifier = self.parse_expression()
        self.identifier_table.set_identifier_value(ident_name, temp_var.value)

    def parse_conditional_statement(self):
        self.syntactic_logs.append("<条件语句> → if (<条件>) then <嵌套语句>; else <嵌套语句>")
        self.match("if")
        self.match("(")
        temp_var: TempVar = self.parse_condition()
        self.match(")")
        self.match("then")

        self.intermediate_code_table.add(Quadruple("jmp", temp_var.name, "null",
                                                   str(self.intermediate_code_table.next_quadruple_index() + 2)))
        false_exit_index = self.intermediate_code_table.next_quadruple_index()
        self.intermediate_code_table.add(Quadruple("j", "null", "null", "0"))

        self.parse_nested_statement()
        exit_index = self.intermediate_code_table.next_quadruple_index()
        self.intermediate_code_table.add(Quadruple("j", "null", "null", "0"))
        self.intermediate_code_table.back_end(false_exit_index,
                                              str(self.intermediate_code_table.next_quadruple_index()))

        self.match(";")
        self.match("else")
        self.parse_nested_statement()

        self.intermediate_code_table.back_end(exit_index, str(self.intermediate_code_table.next_quadruple_index()))

    def parse_loop_statement(self):
        self.syntactic_logs.append("<循环语句> → while (<条件>) do <嵌套语句>")

        next_ = self.intermediate_code_table.next_quadruple_index()

        self.match("while")
        self.match("(")
        temp_var: TempVar = self.parse_condition()
        self.match(")")
        self.match("do")

        self.intermediate_code_table.add(Quadruple("jnz", temp_var.name, "null",
                                                   str(self.intermediate_code_table.next_quadruple_index() + 2)))
        false_exit_index = self.intermediate_code_table.next_quadruple_index()
        self.intermediate_code_table.add(Quadruple("j", "null", "null", "0"))

        self.parse_nested_statement()

        self.intermediate_code_table.add(Quadruple("j", "null", "null", str(next_)))
        self.intermediate_code_table.back_end(false_exit_index,
                                              str(self.intermediate_code_table.next_quadruple_index()))

    def parse_expression(self) -> TempVar:
        self.syntactic_logs.append("<表达式> →<项><表达式prime>")
        arg1: TempVar = self.parse_term()
        return self.parse_expression_prime(arg1)

    def parse_expression_prime(self, arg1: TempVar) -> TempVar:  # XXX:是否生成临时变量
        self.syntactic_logs.append("<表达式prime> →<加法运算符><项><表达式prime>|ε")
        arg1 = TempVarTable.temp_var2ident(arg1)
        if TokenManager.match_type(self.word, "+"):
            self.parse_addition_operator()
            arg2: TempVar = self.parse_term()
            res: TempVar = TempVarTable.new_temp_var(str(int(arg1.value) + int(arg2.value)))
            quadruple: Quadruple = Quadruple("+", arg1.name, arg2.name, res.name)
            self.intermediate_code_table.add(quadruple)
            return self.parse_expression_prime(res)
        else:
            return TempVarTable.ident2temp_var(arg1)

    def parse_term(self) -> TempVar:
        self.syntactic_logs.append("<项> → <因子><项prime>")
        arg1: TempVar = self.parse_factor()
        return self.parse_term_prime(arg1)

    def parse_term_prime(self, arg1: TempVar) -> TempVar:
        self.syntactic_logs.append("<项prime> → <乘法运算符><因子><项prime>|ε")
        arg1 = TempVarTable.temp_var2ident(arg1)
        if TokenManager.match_type(self.word, "*"):
            self.parse_multiplication_operator()
            arg2: Identifier = self.parse_factor()
            res: TempVar = TempVarTable.new_temp_var(str(int(arg1.value) * int(arg2.value)))
            quadruple: Quadruple = Quadruple("*", arg1.name, arg2.name, res.name)
            self.intermediate_code_table.add(quadruple)
            return self.parse_term_prime(res)
        else:
            return TempVarTable.ident2temp_var(arg1)

    def parse_factor(self) -> TempVar:
        self.syntactic_logs.append("<因子> → <标识符>|<常量>|(<表达式>)")
        if TokenManager.match_type(self.word, "标识符"):
            foo = self.parse_identifier()
            bar = self.identifier_table.get_identifier(foo)
            return TempVarTable.ident2temp_var(bar)
        elif TokenManager.match_type(self.word, "数字"):
            return self.parse_constant()
        elif TokenManager.match_type(self.word, "("):
            self.match("(")
            temp_var: TempVar = self.parse_expression()
            self.match(")")
            return temp_var

    def parse_constant(self) -> TempVar:
        self.syntactic_logs.append("<常量> → <无符号整数>")
        ret = self.parse_unsigned_integer()
        return ret

    def parse_unsigned_integer(self) -> TempVar:
        self.syntactic_logs.append("<无符号整数> → <数字序列>")
        ret = self.parse_numeric_sequence()
        return ret

    def parse_numeric_sequence(self) -> TempVar:
        self.syntactic_logs.append("<数字序列> → <数字序列><数字>|<数字>")
        value: str = self.word.value
        self.match("数字")
        ident = Identifier(name=value, value=value)
        return TempVarTable.ident2temp_var(ident)

    def parse_addition_operator(self):
        self.syntactic_logs.append("<加法运算符> → +")
        self.match("+")

    def parse_multiplication_operator(self):
        self.syntactic_logs.append("<乘法运算符> → *")
        self.match("*")

    def parse_relative_operator(self) -> bool:
        self.syntactic_logs.append("<关系运算符> → <|>|!= |>=|<= |== ")
        if TokenManager.match_type(self.word, "<"):
            self.match("<")
        elif TokenManager.match_type(self.word, ">"):
            self.match(">")
        elif TokenManager.match_type(self.word, "!="):
            self.match("!=")
        elif TokenManager.match_type(self.word, ">="):
            self.match(">=")
        elif TokenManager.match_type(self.word, "<="):
            self.match("<=")
        elif TokenManager.match_type(self.word, "=="):
            self.match("==")
        else:
            return False
        return True

    def parse_condition(self):
        self.syntactic_logs.append("<条件> → <表达式><关系运算符><表达式>")
        exp1: TempVar = self.parse_expression()
        logical_operator: str = self.word.value
        self.parse_relative_operator()
        exp2: TempVar = self.parse_expression()
        temp_var = TempVarTable.new_temp_var("")
        self.intermediate_code_table.add(Quadruple(logical_operator, exp1.name, exp2.name, temp_var.name))
        temp_var.type_ = "bool"
        if logical_operator == "<":
            temp_var.value = str(int(exp1.value) < int(exp2.value))
        elif logical_operator == ">":
            temp_var.value = str(int(exp1.value) > int(exp2.value))
        elif logical_operator == "<=":
            temp_var.value = str(int(exp1.value) <= int(exp2.value))
        elif logical_operator == ">=":
            temp_var.value = str(int(exp1.value) >= int(exp2.value))
        elif logical_operator == "==":
            temp_var.value = str(int(exp1.value) == int(exp2.value))
        elif logical_operator == "!=":
            temp_var.value = str(int(exp1.value) != int(exp2.value))
        else:
            raise Exception("未知的逻辑运算符")

        return temp_var

    def parse_compound_statement(self):
        self.syntactic_logs.append("<复合语句> → begin <语句部分> end")
        self.match("begin")
        self.parse_statement_section()
        self.match("end")

    def parse_nested_statement(self):
        self.syntactic_logs.append("<嵌套语句> → <语句>|<复合语句>")
        if TokenManager.match_type(self.word, "标识符") \
                or TokenManager.match_type(self.word, "if") or TokenManager.match_type(self.word, "while"):
            self.parse_statement()
        elif TokenManager.match_type(self.word, "begin"):
            self.parse_compound_statement()
        else:
            raise Exception("嵌套语句错误")
