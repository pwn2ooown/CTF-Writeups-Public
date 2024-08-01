#include <stdio.h>

int main() {
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);

    puts("Welcome To LoTuX Skewer Shop!");

    char buf[0x10];
    read(0, buf, 0x20);

    return 0;
}