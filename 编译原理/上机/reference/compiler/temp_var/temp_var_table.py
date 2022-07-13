from compiler.identifier import Identifier
from compiler.temp_var import TempVar


class TempVarTable:
    index: int = -1

    @staticmethod
    def new_temp_var(value: str) -> TempVar:
        TempVarTable.index += 1
        return TempVar(f"T{TempVarTable.index}").set_value(value)

    @staticmethod
    def ident2temp_var(ident: Identifier) -> TempVar:
        ret = TempVar(str(ident.name))
        ret.type_ = str(ident.type_)
        ret.value = str(ident.value)
        return ret

    @staticmethod
    def temp_var2ident(temp_var: TempVar) -> Identifier:
        ret = Identifier()
        ret.name = temp_var.name
        ret.type_ = temp_var.type_
        ret.value = temp_var.value
        return ret
