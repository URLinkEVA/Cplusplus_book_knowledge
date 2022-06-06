#define _CRT_SECURE_NO_WARNINGS
#include <graphics.h>
#include <conio.h>
#include <Windows.h>
#include <iostream>
#include <MMSystem.h>//播放音乐的头文件
#pragma comment(lib,"winmm.lib")//加载库文件
#define ALLIMAGE 275

using namespace std;


int main()
{
	char file_name[300];
	IMAGE image[ALLIMAGE];
	cout << "loading ..." << endl;
	for (int i = 1; i <= 275; i++) {//预加载
		sprintf(file_name, "d:\\C++ code\\worktest1\\worktest1\\imgs\\%d.jpg", 275 - i, i);
		loadimage(&image[i - 1], file_name);
	}
	
	initgraph(1280, 720);
	mciSendString(("play fs.mp3 repeat"), 0, 0, 0);

	while (1) {
		for (int i = 0; i < 275; i++) {
		putimage(0, 0, &image[i]);
		Sleep(75);
		}
	}
	
	_getch();
	closegraph();
}
