#include <stdio.h>

int main()
{
    for(int i=0;i>=-65536;i--){
        if((unsigned short)i == 7){
            printf("%d",i); // -65529
            break;
        }
    }

    return 0;
}