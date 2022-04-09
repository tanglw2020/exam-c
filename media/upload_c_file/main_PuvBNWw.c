#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#define Max_len 1024

int Func(char *s)
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

	while (!feof(fp))
	{
		if (fgets(s, Max_len - 1, fp) != NULL)
		{
			int cnt = Func(s);
			fprintf(wf, "%d\n", cnt);

			printf("%s", s);
			printf("%d\n", cnt);
		}
	}
	fclose(fp);
	fclose(wf);

	printf("======== The programm ends as expected ===========\n");

	return 0;
}
