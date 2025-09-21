#include <stdio.h>
#include <stdlib.h>
void init() {
    setvbuf(stdout,0,2,0);
    setvbuf(stdin,0,2,0);
    setvbuf(stderr,0,2,0);
}

void menu() {
  puts("------>> NTUT islab memo <<------");
  puts("1. show");
  puts("2. edit");
  puts("3. exit");
  puts("Give me your choice:");
}

int main(){
  init();
  unsigned long long memo[200] = {};
    while(1) {
      menu();
      int n, index = 0;
      scanf("%d", &n);
      if(n != 1 && n != 2) break;
      puts("index:");
      scanf("%d", &index);
      if(n == 1) 
        printf("memo[%d]: %lld\n",index,memo[index]);
      else {
        puts("Give me your secret:");
        scanf("%lld", &memo[index]);
      }
  }
  puts("bye~");
  return 0;
}