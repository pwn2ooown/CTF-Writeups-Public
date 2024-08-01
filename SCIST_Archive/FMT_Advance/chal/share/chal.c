#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(){
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);

    char buf[0x30];
    char flag[0x30];

    strcpy(flag, "SCIST{Please_don't_answer_this_fake_flag}");

    read(0, buf, 0x2f);

    printf(buf);

    return 0;
}