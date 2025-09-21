#include<stdio.h>
#include<stdlib.h>
void main (void)
{
  int i = 0;
  int size = 0;
  long int offset = 0;
  long int value = 0;

  setvbuf(stdin, 0, 2, 0);
  setvbuf(stdout, 0, 2, 0);

  printf("Size:");
  scanf("%lu", &size);
  unsigned long *chunk = malloc(size);

  if (chunk)
  {
    printf("Magic:%p\n", chunk);

    for (i = 0; i < 2; ++i)
    {
      printf("Offset & Value:");
      scanf("%lx %lx", &offset, &value);
      chunk[offset] = value;
    }
  }
  return;
}