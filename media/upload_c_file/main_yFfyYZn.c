#include <stdio.h>

/************考试作答区***************/
int Func( int n ,int m)
{
	
}
/************考试作答区***************/

void main()
{	
	FILE *fp,*wf;
	int x,y;
	fp = fopen("input.txt","r+");
	wf = fopen("output.txt","w");
	while(!feof(fp)) {
		if(fscanf(fp,"%d %d",&x,&y) != EOF)
		fprintf(wf, "%d\n", Func(x,y));
	}
	fclose(fp); 
	fclose(wf); 
  
}