#include <stdio.h>

/****************************************************/
int Func(int n)
{
	
}
/****************************************************/

void main()
{  
	FILE *fp, *wf;
	int sum;

	fp = fopen("input.txt","r+");
	wf = fopen("ouput.txt","w");
	while(!feof(fp)) {
		if(fscanf(fp,"%d",&sum) != EOF)
			fprintf(wf, "%d\n", Func(sum));
	}
	fclose(fp); 
	fclose(wf);     
}
