#define _CRT_SECURE_NO_WARNINGS
#include <graphics.h>
#include <conio.h>
#include <Windows.h>
#include <iostream>
#include <math.h>
#include <time.h>
#include <string>
#include <MMSystem.h>//播放音乐的头文件
#pragma comment(lib,"winmm.lib")//加载库文件

#define ALLIMAGE 275
#define PI 3.14

using namespace std;

class drawHPWord {
private:
	int x;
	int y;
public:
	drawHPWord(int x, int y) {
		this->x = x;
		this->y = y;
	}
	void draw() {
		srand((unsigned int)time(NULL));
		int x = 10;
		while (1)
		{
			settextcolor(RGB(rand() % 256, rand() % 256, rand() % 256));
			settextstyle(x, 0, "楷体");
			outtextxy(x, y, "Happy Birthday！！！");
			Sleep(200);
			if (x <= 30)
				x = x + 3;
		}
	}
	int getX() {
		return this->x;
	}
	void setX(int x) {
		this->x = x;
	}
	int getY() {
		return this->y;
	}
	void setY(int y) {
		this->y = y;
	}
};

class drawLittle {
public:
	//贺卡小人
	drawLittle() {}
	//绘制贺卡小人的头
	void drawLittleHead(const POINT* pts4) {
		setfillcolor(RGB(253, 177, 169));
		setlinecolor(RGB(253, 177, 169));

		solidpolygon(pts4, 3);

		setlinecolor(RGB(248, 106, 89));
		setfillcolor(RGB(248, 106, 89));
		fillcircle(321, 363, 15);
		fillcircle(418, 360, 15);

		setlinecolor(WHITE);
		setfillcolor(RGB(255, 255, 255));
		fillcircle(321, 493, 15);
		fillcircle(418, 493, 15);
	}
	//绘制贺卡小人的身体
	void drawLittleBody(const POINT* pts4) {
		setlinecolor(RGB(248, 106, 89));
		setfillcolor(RGB(248, 106, 89));
		fillrectangle(304, 229, 339, 342);
		fillrectangle(400, 229, 435, 342);

		setlinecolor(RGB(246, 178, 175));
		setfillcolor(RGB(246, 178, 175));
		fillrectangle(304, 339, 339, 452);
		fillrectangle(400, 339, 435, 452);


		setfillcolor(RGB(248, 106, 89));
		setlinecolor(RGB(248, 106, 89));
		floodfill(395, 150, RGB(248, 106, 89));

		setlinecolor(RGB(109, 147, 163));
		setfillcolor(RGB(109, 147, 163));
		fillrectangle(169, 271, 350, 295);
		fillrectangle(402, 271, 582, 294);

		setfillcolor(RGB(90, 59, 70));
		setlinecolor(RGB(90, 59, 70));
		arc(281, 245, 464, 436, 0, 3.1415);
		line(281, 339, 466, 339);
		floodfill(395, 290, RGB(90, 59, 70));

		setfillcolor(RGB(248, 106, 89));
		setlinecolor(RGB(248, 106, 89));
		solidpolygon(pts4, 3);

		setfillcolor(RGB(253, 177, 169));
		setlinecolor(RGB(253, 177, 169));
		POINT pts5[] = { {378,50},{432,107},{377,161},{323,107},{378,50} };
		solidpolygon(pts5, 4);

		setfillcolor(RGB(248, 106, 89));
		setlinecolor(RGB(248, 106, 89));
		solidpolygon(pts5, 4);

		setfillcolor(RGB(253, 177, 169));
		setlinecolor(RGB(253, 177, 169));
		POINT pts6[] = { {378,134},{432,191},{378,245},{323,191},{378,134} };
		solidpolygon(pts6, 4);


		setlinecolor(WHITE);
		setfillcolor(RGB(255, 255, 255));
		fillcircle(378, 190, 30);


		setlinecolor(BLACK);
		setfillcolor(RGB(0, 0, 0));
		fillcircle(378, 190, 10);

		setlinecolor(WHITE);
		setfillcolor(RGB(255, 255, 255));
		fillcircle(141, 284, 13);
		fillcircle(616, 284, 13);

		setlinecolor(RGB(125, 123, 123));
		setfillcolor(RGB(125, 123, 123));
		fillroundrect(125, 500, 308, 508, 5, 5);
	}
	void draw() {
		setbkcolor(RGB(250, 100, 70));
		POINT pts4[] = { {325,0},{375,50},{425,0},{325,0} };
		drawLittleHead(pts4);
		drawLittleBody(pts4);
	}
};

class drawCC {
public:
	drawCC() {	}
	void draw() {
		initgraph(1280, 720);//创建窗口
	//// 绘制
	//	while (!_kbhit()) {
		drawCard();
		//}
		//closegraph();//关闭窗口
	}
	void drawWord() {
		settextstyle(45, 0, "楷体");
		outtextxy(20, 400, "Happy Birthday！！！");
		outtextxy(20, 20, "201921003342");
	}
	void drawCard() {
		setbkcolor(WHITE);
		cleardevice();
		Sleep(300);
		setcolor(BLACK);			//circle的线条为hei
		setfillcolor(YELLOW);			//circle内huang色填充
		settextcolor(YELLOW);
		drawWord();
		fillcircle(300, 300, 60);	//circle center为（100，100）半径20
		Sleep(300);
		cleardevice();

		setcolor(BLACK);			//circle的线条为hei
		setfillcolor(RED);			//circle内huang色填充	
		settextcolor(RED);
		drawWord();
		fillcircle(90, 90, 60);	//circle center为（100，100）半径20
		Sleep(200);
		cleardevice();

		setcolor(BLACK);			//circle的线条为hei
		setfillcolor(BLUE);			//circle内huang色填充	
		settextcolor(BLUE);
		drawWord();
		fillcircle(300, 90, 60);	//circle center为（100，100）半径20
		Sleep(300);
		cleardevice();

		setcolor(BLACK);			//circle的线条为hei
		setfillcolor(GREEN);			//circle内huang色填充	
		settextcolor(GREEN);
		drawWord();
		fillcircle(90, 300, 60);	//circle center为（100，100）半径20
		Sleep(200);
		cleardevice();
		//setbkcolor(WHITE);
		//cleardevice();
	}
};

class drawChess {
public:
	void draw() {
		int step = 50;
		setbkcolor(WHITE);
		//cleardevice();
		int i, j;
		for (i = 1; i <= 8; i++)
		{
			for (j = 1; j <= 8; j++)
			{
				if ((i + j) % 2 == 1)
				{
					setfillcolor(WHITE);
					solidrectangle(i * step, j * step, (i + 1) * step, (j + 1) * step);

				}
				else
				{
					setfillcolor(RED);
					solidrectangle(i * step, j * step, (i + 1) * step, (j + 1) * step);
				}
			}
		}
	}
};

class drawChangeC {
private:
	int c;
	double a;
	int x = 120, y = 120;
	int r = 130;
public:
	void draw() {
		for (a = 0; a < PI * 2; a += 0.0001)
		{
			x = (int)(r * cos(a) + 230 + 0.5);
			y = (int)(r * sin(a) + 230 + 0.5);
			c = (int)(a * 255 / (2 * PI) + 0.5);
			setcolor(RGB(255, 0, c));
			line(230, 230, x, y);
		}
		//_getch();
		Sleep(200);
	}
};

class hbCard {
private:
	int WIDTH = 1280; //窗口宽度
	int HEIGHT = 720; //窗口高度
	drawHPWord hp = drawHPWord(80, 120);
	drawLittle lt = drawLittle();
	drawCC dcc = drawCC();
	drawChess dc = drawChess();
	drawChangeC dcc1 = drawChangeC();
public:
	hbCard() {}
	void draw2() {
		cleardevice();
		//initgraph(WIDTH, HEIGHT);//创建窗口
	// 绘制
		//while (!_kbhit()) {
		lt.draw(); outtextxy(20, 20, "201921003342");
		hp.draw();

		//}
		Sleep(200);
		cleardevice();
		closegraph();//关闭窗口
	}
	void draw1() {
		dcc.draw();
	}
	void draw3() {
		settextcolor(DARKGRAY);

		dcc.drawWord(); outtextxy(20, 20, "201921003342");
		dcc1.draw();
		cleardevice();
	}
	void draw4() {
		dc.draw();
		for (int i = 0; i < 5; i++) {
			settextcolor(BLACK); outtextxy(20, 20, "201921003342");
			dcc.drawWord();
			Sleep(150);
			settextcolor(WHITE);
			dcc.drawWord();
			Sleep(150);
		}
		cleardevice();
	}
};


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
	mciSendString(_T("play fs.mp3 repeat"), 0, 0, 0);


	for (int i = 0; i < 275; i++)
	{
		putimage(0, 0, &image[i]);
		Sleep(75);
	}

	//_getch();
	closegraph();

	hbCard hbc;
	hbc.draw1();
	hbc.draw3();
	hbc.draw4();
	hbc.draw2();
}
