# 图像处理
根据要求对原始两个 24 位 bmp 图像进行处理，生成指定的文件同时显示到屏幕输出。

# 代码
```c++
/*
环境配置：项目-->属性-->C/C++-->预处理-->常规0-->SDL检查  设为 否
         项目-->属性-->C/C++-->预处理-->预处理定义：加入 _CRT_SECURE_NO_WARNINGS;

题目要求：1.完善CutImage()函数，完成从给定图中截取148*200大小的图块
		 2.完善ImageInvert()函数，实现将图像左右反转。
		 3.完善AppendEdge()函数，实现给图片四周加边框，边框宽度不小于6，边框颜色自行选定(参考RGB颜色表)。
		 4.完善Addimg()函数,实现将小图叠加至大图左下角,或者右上角。

结果提交: 1.将源文件复制粘贴到word文档中，并将运行结果图(四张)插入在程序后面，保存为“编程水平测试1.docx”文件，上传到“源代码”目录下
         2.将结果图(四张)打包成压缩文档"编程水平测试1.zip"上传到“运行结果”目录下
*/
#include<iostream>
#include<Windows.h>
#include<stdlib.h>
#include<conio.h>
#include<string.h>
using namespace std;
#define M 1024
#define N 960
//************针对不确定高度和宽度的bmp文件,定义高度最大1024,宽度最大960的二维数组*********

//r1,g1,b1用来存放fileName1对应的颜色分量
unsigned char r1[M][N];
unsigned char g1[M][N];
unsigned char b1[M][N];

//r2,g2,b2用来存放fileName2对应的颜色分量
unsigned char r2[M][N];
unsigned char g2[M][N];
unsigned char b2[M][N];

//***********将buf中的图像数据分解到b1、g1、r1中,数据存放使用了数组中h行,w列
void getRGB1(unsigned char* buf, int w, int h)
{
	int i, j;
	unsigned char *p = buf;
	for (i = 0;i < h;i++)
		for (j = 0;j < w;j++)
		{
			b1[i][j] = *p++;
			g1[i][j] = *p++;
			r1[i][j] = *p++;
		}
}

//***********将buf中的图像数据分解到b2、g2、r2中,数据存放使用了数组中h行,w列
void getRGB2(unsigned char* buf, int w, int h)
{
	int i, j;
	unsigned char *p = buf;
	for (i = 0;i < h;i++)
		for (j = 0;j < w;j++)
		{
			b2[i][j] = *p++;
			g2[i][j] = *p++;
			r2[i][j] = *p++;
		}
}

//********************截取图块********************
//参数buf为原图像数据(像素值),sw和sh为原图像宽度和高度
//参数subbuf存放所截图块的像素数据,dw和dh为图块宽度和高度
void CutImage(unsigned char* buf, unsigned char* subbuf, int& sw, int& sh, int& dw, int& dh)
{
	
	//**********完成函数,从buf中截取dh行,dw列像素的图块存入subbuf中*******
	
	
}

//**********图像翻转*******************
//参数buf为原图像数据(像素值),w和h为图像宽度和高度
void ImageInvert(unsigned char* buf, int& w, int& h)
{
	//**********完成函数,实现将buf中的图像翻转90度*************
	//90度翻转可以考虑是图像关于中间列的左右元素互换,即三个颜色分量数组同时进行90度翻转
	

	//******将翻转后的三个颜色分量重新写回buf中
	unsigned char *p = buf;
	for (int i = 0; i < h; i++)
	{
		for (int j = 0; j < w; j++)
		{
			*p++ = b1[i][j]; 
			*p++ = g1[i][j]; 
			*p++ = r1[i][j]; 
		}
	}


}
//*********************加边框*********************
//参数buf为原图像数据(像素值),w和h为图像宽度和高度
void AppendEdge(unsigned char* buf, int& w, int& h)
{
	//**********完成函数,给buf对应的图像加上宽度不小于6的边框,具体颜色根据附件中的配色表自行确定*************
	//加边框就是将二维数组的外围若干行、列对应的像素颜色都设为统一的颜色，修改过的三个颜色分量数组需要重新写回buf中

	
	

}

//*****************图像叠加************
//参数buf1为大图图像数据(像素值),w1和h1为大图宽度和高度
//参数buf2为小图图像数据(像素值),w2和h2为小图宽度和高度
void Addimg(unsigned char* buf1, int& w1, int& h1, unsigned char* buf2, int& w2, int& h2)
{

	//**********完成函数,将buf2对应的小图叠加到buf1对应的大图的左下角或者右上角*************
	//将小图叠加至大图,可以考虑遍历小图颜色数组,将每个像素覆盖大图对应位置的像素
	//叠加到右上角时,需要计算确定大图对应的位置
	//要实现说明文档中右上角的浅淡效果,可以考虑不直接用小图像素替换大图像素,而是  将大图像素颜色分量和小图对应像素颜色分量按照某种百分比进行相加
	//叠加过后的大图的三个颜色分量数组需要重新写回buf1中

	
}

//************读取图像,不要更改*************
unsigned char* readimage(char* fileName, int& w, int& h, BITMAPFILEHEADER & bf, BITMAPINFOHEADER & bi)
{
	FILE* fp = NULL;                                 //定义文件指针
	unsigned char* p = NULL;
	if ((fp = fopen(fileName, "rb")) == NULL)
	{
		cout << "文件未找到！";
		exit(0);
	}
	fread(&bf, sizeof(BITMAPFILEHEADER), 1, fp);//读取BMP文件头文件
	fread(&bi, sizeof(BITMAPINFOHEADER), 1, fp);//读取BMP文件头文件信息
	w = bi.biWidth;                            //获取图像的宽
	h = bi.biHeight;                           //获取图像的高
	p = new unsigned char[w * h * 3]; //分配缓冲区大小
	fseek(fp, long(sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER)), 0);//定位到像素起始位置
	fread(p, w * h * 3, 1, fp); //开始读取数据
	fclose(fp);
	return p;
}

//*************显示图像,不要更改****************
void ShowImage(unsigned char* buf, int& w, int& h) //, BITMAPFILEHEADER& bf, BITMAPINFOHEADER& bi)
{
	int r, g, b, pix;
	HWND wnd;                                 //窗口句柄
	HDC dc;
	unsigned char* p = buf;
	wnd = GetForegroundWindow();               //获取窗口句柄
	dc = GetDC(wnd);                           //获取绘图设备
	int x = 40;
	int y = 100;
	for (int j = 0; j < h; j++)
	{
		for (int i = 0; i < w; i++)
		{
			b = *p++; g = *p++; r = *p++;
			pix = RGB(r, g, b);
			SetPixel(dc, x + i, y + h - j, pix);
		}
	}
}

//******************生成新图像文件,不要更改******************************
void WriteNewImage(char* Name, unsigned char* buf, int& w, int& h)

{
	unsigned char* Buff = buf;
	BITMAPFILEHEADER bf;
	BITMAPINFOHEADER bi;
	FILE* Out = fopen(Name, "wb");
	if (!Out)
		return;
	bf.bfType = 0x4D42;
	bf.bfSize = w * h * 3;
	bf.bfReserved1 = 0;
	bf.bfReserved2 = 0;
	bf.bfOffBits =
		sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);
	bi.biSize = sizeof(BITMAPINFOHEADER);
	bi.biWidth = w;
	bi.biHeight = h;
	bi.biPlanes = 1;
	bi.biBitCount = 24;
	bi.biCompression = BI_RGB;
	bi.biSizeImage = 0;
	bi.biXPelsPerMeter = 0;
	bi.biYPelsPerMeter = 0;
	bi.biClrUsed = 0;
	bi.biClrImportant = 0;

	fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, Out);
	fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, Out);
	fwrite(Buff, w * h * 3, 1, Out);
	fclose(Out);

	delete[]Buff;
}
int main()
{
	//定义操作相关文件名,fileName为原有图像文件,OutName为输出图像文件,此处默认文件都存放于d盘exam文件夹中
	//可事先在考试机器上对应位置新建exam文件夹,存放下载的图像文件
	
	char fileName1[80] = "d:\\exam\\tiger.bmp";		//大图带路径文件名
	char fileName2[40] = "d:\\exam\\spring.bmp";	//小图带路径文件名
	char OutName1[80] = "d:\\exam\\cut.bmp";		//保存截图的带路径文件名
	char OutName2[40] = "d:\\exam\\invert.bmp";		//保存90度翻转后图的带路径文件名
	char OutName3[40] = "d:\\exam\\add.bmp";		//保存加边框后图的带路径文件名
	char OutName4[40] = "d:\\exam\\2in1.bmp";		//保存小图叠加至大图后的带路径文件名
	
	//定义读取文件后存放像素数据的指针
	unsigned char* buf1 = NULL;
	unsigned char* buf2 = NULL;
	int w1, h1, w2, h2;                                //定义读取图像的长和宽
	
	//定义读取文件后的文件头和信息头对象
	BITMAPFILEHEADER bf1, bf2;
	BITMAPINFOHEADER bi1, bi2;

	//*********截图测试***************
	w2 = 148; h2 = 200;
	unsigned char* subbuf = new unsigned char[w2 * h2 * 3];
	
	//读取大图像素数据
	buf1 = readimage(fileName1, w1, h1, bf1, bi1);

	CutImage(buf1, subbuf, w1, h1, w2, h2);			//调用截图函数
	ShowImage(subbuf, w2, h2);						//显示截图
	WriteNewImage(OutName1, subbuf, w2, h2);		//保存截图
	

	//*********图像翻转测试************
	//清屏处理,执行时直接按回车
	cout << "press any key continue......" << endl;
	getchar();
	system("cls");

	//读取大图
	buf1 = readimage(fileName1, w1, h1, bf1, bi1);
	ImageInvert(buf1, w1, h1);					//调用翻转函数
	ShowImage(buf1, w1, h1);					//显示翻转后图
	WriteNewImage(OutName2, buf1, w1, h1);		//保存翻转后的图
	
	

	//*********加边框测试***************
	//清屏处理,执行时直接按回车
	cout << "press any key continue......" << endl;
	getchar();
	system("cls");

	//读取大图
	buf1 = readimage(fileName1, w1, h1, bf1, bi1);
	AppendEdge(buf1, w1, h1);					//调用加边框函数
	ShowImage(buf1, w1, h1);					//显示加边框的图
	WriteNewImage(OutName3, buf1, w1, h1);		//保存加边框的图
	
	

	//**********图像叠加测试**************
	//清屏处理,执行时直接按回车
	cout << "press any key continue......" << endl;
	getchar();
	system("cls");

	buf1 = readimage(fileName1, w1, h1, bf1, bi1);		//读取大图
	buf2 = readimage(fileName2, w2, h2, bf2, bi2);		//读取小图
	Addimg(buf1, w1, h1, buf2, w2, h2);					//调用叠加函数
	ShowImage(buf1, w1, h1);							//显示叠加后的大图
	WriteNewImage(OutName4, buf1, w1, h1);				//显示保存叠加后的大图
	
		

	return 0;
}
```
