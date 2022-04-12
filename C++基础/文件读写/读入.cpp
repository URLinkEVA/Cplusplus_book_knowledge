// 读入一个文本文件的内容，然后将它打印到屏幕上。注意我们使用了一个新的成员函数叫做eof
// 它是ifstream 从类 ios 中继承过来的，当到达文件末尾时返回true

#include<iostream>
#include<fstream>
#include<stdlib.h>

using namespace std;

int main(){
    char buffer[256];
    ifstream in("out.txt");
    if(! in.is_open())
    {
        cout << "Error opening file"; exit(1);
    }
    while (! in.eof())
    {
        in.getline(buffer,100);
        cout << buffer << endl;
    }
    return 0;
}