#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#define Max_len 1024

int Func(int n, int m)
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
	wf = fopen("output.txt", "w");

	int n, m;
	while (!feof(fp))
	{
		if (fscanf(fp, "%d %d", &n, &m) != EOF)
		{
			int cnt = Func(n, m);
			fprintf(wf, "%d\n", cnt);
			printf("%d %d %d\n", n, m, cnt);
		}
	}
	fclose(fp);
	fclose(wf);

	printf("======== The programm ends as expected ===========\n");

	return 0;
}
