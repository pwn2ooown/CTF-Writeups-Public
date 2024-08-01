// gcc -fno-stack-protector chal.c -o chal
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <time.h>
#include <sys/mman.h>

char new_name_buff[0x30];
char *cat_list[] = {
    "kiki",
    "lucky",
    "cola",
    "dio",
};
void (*meow)();

void meow1()
{
    puts("MEOW!!");
}

void meow2()
{
    puts("m~e~o~w~");
}

void meow3()
{
    puts("m...eo...w");
}

void init_proc()
{
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
    
    unsigned long data_addr = (unsigned long)&new_name_buff & ~0xfff;
    mprotect((void *)data_addr, 0x1000, PROT_EXEC | PROT_READ | PROT_WRITE);
}

int main()
{
    init_proc();

    int idx;

    srand(time(NULL));
    switch (rand() % 3) {
    case 0: meow = meow1; break;
    case 1: meow = meow2; break;
    case 2: meow = meow3; break;
    }

    printf("Welcome to catshop, which one do you want to buy?\n");
    for (int i = 0; i < sizeof(cat_list) / sizeof(cat_list[0]); i++)
        printf("%d. %s\n", i + 1, cat_list[i]);
    printf("> ");

    scanf("%d", &idx);

    printf("New name\n> ");
    read(0, new_name_buff, 0x30);
    cat_list[idx] = &new_name_buff;

    printf("%s: ", cat_list[idx]);
    meow();
    printf("\n");

    return 0;
}