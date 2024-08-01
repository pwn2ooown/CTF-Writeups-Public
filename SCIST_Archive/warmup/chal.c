// gcc -fno-stack-protector -no-pie chal.c -o chal
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>

void backdoor()
{
    system("/bin/sh");
    exit(0);
}

int main()
{
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);

    char buf[0x20];

    printf("What's your name?\n> ");
    read(0, buf, 0x100);

    printf("Hello, %s !\n", buf);

    return 0;
}