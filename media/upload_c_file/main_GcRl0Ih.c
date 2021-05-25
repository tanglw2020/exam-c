#include <stdio.h>

/****************************************************/
int Func(int m,int n)
{
	


}
/****************************************************/

void main()
{  
	FILE *fp, *wf;
	int a,b;
	fp = fopen("input.txt","r+");
	wf = fopen("output.txt","w");
	while(!feof(fp)) {
		if(fscanf(fp,"%d %d",&a,&b) != EOF)
			fprintf(wf, "%d\n", Func(a,b));
	}
	fclose(fp); 
	fclose(wf);     
}
