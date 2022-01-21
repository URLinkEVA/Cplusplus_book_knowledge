void ImageInvert(unsigned char* buf, int& w, int& h)
{
	int i, j;
	unsigned char* d = buf;
	for (i = 0; i < h; i++)
		for (j = 0; j < w; j++)
		{
			b1[i][j] = *d++;
			g1[i][j] = *d++;
			r1[i][j] = *d++;
			b1[i][j] = b1[i][w - j - 1];
			g1[i][j] = g1[i][w - j - 1];
			r1[i][j] = r1[i][w - j - 1];

		}
	//**********完成函数,实现将buf中的图像翻转90度*************
	//90度翻转可以考虑是图像关于中间列的左右元素互换,即三个颜色分量数组同时进行90度翻转


	//******将翻转后的三个颜色分量重新写回buf中
	unsigned char* p = buf;
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
