#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

ssize_t unserialize(FILE *fp, char *buf, size_t size) {
  char szbuf[0x20];
  char *tmpbuf;

  for (size_t i = 0; i < sizeof(szbuf); i++) {
    szbuf[i] = fgetc(fp);
    if (szbuf[i] == ':') {
      szbuf[i] = 0;
      break;
    }
    if (!isdigit(szbuf[i]) || i == sizeof(szbuf) - 1) {
      return -1;
    }
  }

  if (atoi(szbuf) > size) {
    return -1;
  }

  tmpbuf = (char*)alloca(strtoul(szbuf, NULL, 0));

  size_t sz = strtoul(szbuf, NULL, 10);
  for (size_t i = 0; i < sz; i++) {
    if (fscanf(fp, "%02hhx", tmpbuf + i) != 1) {
      return -1;
    }
  }

  memcpy(buf, tmpbuf, sz);
  return sz;
}

int main() {
  char buf[0x100];
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);

  if (unserialize(stdin, buf, sizeof(buf)) < 0) {
    puts("[-] Deserialization faield");
  } else {
    puts("[+] Deserialization success");
  }
  
  return 0;
}
