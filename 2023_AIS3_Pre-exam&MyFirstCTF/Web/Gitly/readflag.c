#include <stdio.h>

int main(int argc, char **argv) {
    FILE *fp;
    char flag[0x100];

    fp = fopen("/flag", "r");
    if (fp == NULL) {
        printf("Flag file not found, please contact admin.");
        return 1;
    }
    fgets(flag, 64, fp);
    puts(flag);
    return 0;
}
