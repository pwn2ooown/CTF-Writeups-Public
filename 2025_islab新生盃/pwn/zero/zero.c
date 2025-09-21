#include<stdio.h>
#include<stdlib.h>

void init(){
    setvbuf(stdout,0,2,0);
    setvbuf(stdin,0,2,0);
    setvbuf(stderr,0,2,0);
}

int main(){

    init();

    puts("One buffer overflow to get a shell!");

    char buf[0x40];
    gets(buf);

    return 0;
}