// gcc -z now -fno-stack-protector -no-pie chal.c -o chal
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

#define FILE_LEN 4

struct File {
    char content[0x20];
};

struct File *curr;
char name_buf[0x40];

int main()
{
    if ((unsigned long)main == 0x8787)
        execve("/bin/sh", NULL, NULL);

    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);

    struct File files[FILE_LEN];
    char opt[2];
    int copy_file_idx;
    int file_idx = 0;

    printf("What's your name?\n> ");
    read(0, name_buf, 0x40);
    printf("Hello, %s !\n", name_buf);

    while (1)
    {
        printf(
            "1. new file\n"
            "2. edit file\n"
            "3. copy file\n"
            "4. exit\n"
            "> ");
        read(0, opt, 2);

        switch (opt[0]) {
        case '1':
            if (file_idx < 0 || file_idx++ >= FILE_LEN)
                break;
            
            curr = &files[file_idx];
            printf("Current file %d\n", file_idx);
            break;

        case '2':
            printf("New content\n> ");
            read(0, curr->content, 0x20);
            break;

        case '3':
            printf("Copy from\n> ");
            scanf("%d", &copy_file_idx);
            memcpy(&curr->content, files[copy_file_idx].content, 0x20);
            break;
        
        case '4':
            goto bye;
        }
    }

bye:
    __asm__("xor %rdx, %rdx");
    return 0;
}