#include <stdio.h>
#include <stdlib.h>
#include <time.h>

/************����������***************/
int Func( int n ,int m)
{
	
}
/************����������***************/

int main(){	
	FILE *fi,*fo;
	int x,y;
	fp = fopen("input.txt","r");
	wf = fopen("output.txt","w");
	while(!feof(fp)) {
		if(fscanf(fp,"%d %d",&x,&y) != EOF)
		fprintf(wf, "%d\n", Func(x,y));
	}
	fclose(fp); 
	fclose(wf); 
    return 0;
}