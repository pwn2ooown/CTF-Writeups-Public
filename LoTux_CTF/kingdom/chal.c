#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <string.h> 

//gcc server.c -o server -no-pie -fno-stack-protector

//SET UP
void ignore_me_init_buffering() {
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
}


//MENU
void backdoor() {
    system("/bin/sh");
}

int year = 2023;
void game() {
    printf("=====GAME MENU=====\n");
    printf("Welcome to Hyrule, Link!\n");
    printf("Choose your ability.\n");
    printf("(1) Recall\n");
    printf("(2) Ultrahand\n");
    printf("(3) Fuse\n");
    int mode = 0;
    scanf("%d", &mode);
    getchar();


    switch (mode)
    {
    case 1:
        year--;
        printf("Rewind Success!\nIt's %d now.\n", year);
        break;
    
    case 2:
        printf("Choose two items and stick them together.\n");
        printf("(1) Apple\n");
        printf("(2) Lynel Horn\n");
        printf("(3) Flame Emitter\n");
        char item_list[3][20] = {"Apple","Lynel Horn","Flame Emitter"};

        int item_1 = 0;
        int item_2 = 0;
        printf("Item 1 : ");
        scanf("%d", &item_1);
        printf("Item 2 : ");
        scanf("%d", &item_2);

        printf("Wow, you get a ");
        printf(item_list[item_1-1]);
        printf(item_list[item_2-1]);
        printf("!\n");

        break;

    case 3:
        printf("What do you want to combine your Master Sword with?\n");

        char item_buf[0xff];
        gets(item_buf);

        printf("Wow, you get a Master %s Sword!\n", item_buf);

        break;
    
    default:
        break;
    }
}

//MAIN
void main(int argc, char* argv[]) {
    ignore_me_init_buffering();
    for(;;){
        game();
    }
}
