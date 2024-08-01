#include <stdio.h>
#include <stdlib.h>

int main(){
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);

    char buf[0x10] = {};
    char compare_buf[0x10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'a', 'a', 'a', 'a'};

    scanf("%s", buf);

    int *test_num = (int *)(compare_buf + 12);
    if (*(test_num) > 1633771873){
        puts("Here's your flag : SCIST{test}");
    }

    puts("Bye~");

    return 0;
}