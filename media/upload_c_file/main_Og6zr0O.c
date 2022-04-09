#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#define Max_len 1024

int Func(int n)
{
	int ans = 0;
	/*******************write your code here**************/

	/****************************************************/
	return ans;
}

int main()
{
	FILE *fp, *wf;
	char s[Max_len];

	fp = fopen("input.txt", "r");
	if (fp == NULL)
	{
		printf("Open input.txt failed!!\n");
		return -1;
	}
	wf = fopen("ouput.txt", "w");

	int n;
	while (!feof(fp))
	{
		if (fscanf(fp, "%d", &n) != EOF)
		{
			int cnt = Func(n);
			fprintf(wf, "%d\n", cnt);
			printf("%d %d\n", n, cnt);
		}
	}
	fclose(fp);
	fclose(wf);

	printf("======== The programm ends as expected ===========\n");

	return 0;
}
