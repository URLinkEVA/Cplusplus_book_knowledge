import sys
from compiler import Compiler


def receive_input():
    if len(sys.argv) == 1:
        default_file = "in.txt"
        text = input(f"请输入程序代码（为空则读取 {default_file}）: ")
        if text == "":
            file_name = default_file
        else:
            return text
    else:
        file_name = sys.argv[1]

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"文件 {file_name} 不存在")
        input("请按任意键继续. . .")


if __name__ == '__main__':
    compiler = Compiler(receive_input())
    compiler.compile()
    input("请按任意键继续. . .")
