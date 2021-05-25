#include <stdio.h>
#define Max_len 1024

/****************************************************/
int Func(char  *s)
{

}
/****************************************************/

void main()
{  
	FILE *fp, *wf;
	char s[Max_len];

	fp = fopen("input.txt","r");
	wf = fopen("ouput.txt","w");
	while(!feof(fp)) {
		if(fgets(s, Max_len-1, fp) != NULL)
		{
			fprintf(wf, "%d\n", Func(s));
		}
	}
	fclose(fp); 
	fclose(wf);
}
