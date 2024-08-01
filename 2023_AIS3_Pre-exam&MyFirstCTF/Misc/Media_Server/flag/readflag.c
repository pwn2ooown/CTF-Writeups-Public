#include <stdio.h>

int main(int argc, char **argv) {
	FILE *fp = fopen("/flag", "r");
	char buf[256];
	if (fread(buf, 1, 256, fp) < 0) {
		perror("fread");
		return 1;
	}
	puts(buf);
	fclose(fp);
    return 0;
}
