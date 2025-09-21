#include <stdio.h>
#include <unistd.h>
#include <string.h>

int main() {
  setvbuf(stdin, 0, 2, 0);
  setvbuf(stdout, 0, 2, 0);
  char secret[8];
  char s[16];
  printf("Tell me your secret:");
  gets(secret);
  printf("Your secret:");
  printf(secret);
  printf("\n");
  printf("One chance to get my secret:");
  read(0, s, 2025);
  puts(s);
  return 0;
}
