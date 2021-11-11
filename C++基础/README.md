# 仓库
以课件为主，尽量快速掌握
# 代码
参考案例

从键盘上输入10个整数，并求出这10个数所有奇数之和及偶数之和。

```cpp
#include "iostream"
using namespace std;
int	main()

{

	int num,n=0, sum1=0,sum2=0;
	cout << "please input ten munbers：";
	while (n < 10)
	{
		cin >> num;
		if (num % 2 != 0)
			sum1 = sum1 + num;
		else
			sum2 = sum2 + num;
		n++;
	}
	cout << "odd:" << sum1 << endl;
	cout << "Even:" << sum2 << endl;
	return	0;
}
```
