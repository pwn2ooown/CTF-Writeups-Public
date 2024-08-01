// gcc -z lazy -no-pie chal.c -o chal 
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

char title[0x10];

int main()
{
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);

    if ((unsigned long)main == 0x8787)
        system("echo owo");

    unsigned long from, to;

    printf("Title\n> ");
    read(0, title, 0x10);

    printf("Sender\n> ");
    scanf("%lu", &from);
    
    printf("Receiver\n> ");
    scanf("%lu", &to);

    memcpy((void *)to, (void *)from, 0x8);

    puts(title);
    puts("Done !");

    exit(0);
}