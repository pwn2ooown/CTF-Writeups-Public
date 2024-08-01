#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

char name[1024];

void call_me_maybe()
{
    system("/bin/sh");
}

void unbuffer_io()
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
}

void set_timeout()
{
    alarm(120);
}

void ask_name()
{
    printf("What's your name? ");
    gets(name);
}

void say_goodbye()
{
    printf("Goodbye, %s\n", name);
}

void run_program()
{
    int arr[10], i, v, act;

    for(i = 0; i < 10; i++)
        arr[i] = 0;

    while(1) {
        puts("0 > exit");
        puts("1 > edit number");
        puts("2 > show number");
        puts("3 > sum");
        puts("4 > dump all numbers");
        printf(" > ");
        scanf("%d", &act);

        switch(act) {
            case 0:
                return;
            case 1:
                printf("Index to edit: ");
                scanf("%d", &i);
                printf("How many? ");
                scanf("%d", &v);
                arr[i] = v;
                break;
            case 2:
                printf("Index to show: ");
                scanf("%d", &i);
                printf("arr[%d] is %d\n", i, arr[i]);
                break;
            case 3:
                v = 0;
                for(i = 0; i < 10; i++)
                    v += arr[i];
                printf("Sum is %d\n", v);
                break;
            case 4:
                for(i = 0; i < 10; i++)
                    printf("arr[%d] is %d\n", i, arr[i]);
                break;
        }
    }
}

int main()
{
    set_timeout();
    unbuffer_io();
    ask_name();
    run_program();
    say_goodbye();
    return 0;
}
