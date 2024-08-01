#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <grp.h>
#include <sys/sendfile.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/mman.h>
#include <sys/stat.h>

__attribute__((constructor))
static void initproc() {
    setvbuf(stdin , NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int readfile(const char* file) {
    int size;
    printf("size > ");
    scanf("%d", &size);
    getchar_unlocked();
    printf("data > ");
    char* buf = malloc(size);
    if (fread(buf, 1, size, stdin) != size)
        return puts("fread != size"), exit(EXIT_FAILURE), -1;

    int fd = open(file, O_WRONLY | O_CREAT, 0777);
    if (fd < 0)
        return perror("open"), exit(EXIT_FAILURE), -1;
    write(fd, buf, size);
    close(fd);
    free(buf);

    return 0;
}

char* catpath(const char* dir, const char* file) {
    int dn = strlen(dir);
    int fn = strlen(file);
    char* path = malloc(dn + fn + 2);
    sprintf(path, "%s%s", dir, file);
    return path;
}

char* mapfile(const char* file) {
    int fd = open(file, O_RDONLY);
    if (fd < 0)
        return perror("open"), exit(EXIT_FAILURE), NULL;
    int pagesize = sysconf(_SC_PAGE_SIZE);
    char* page = mmap(0, pagesize, PROT_READ, MAP_PRIVATE | MAP_FILE, fd, 0);
    return page;
}

const char flag[] = "flag";
const char* relbinary = "/binary";
const char* relflag = "/flag";

int main() {
    char cagedir[] = "/tmp/tmpdir.XXXXXX";
    if (mkdtemp(cagedir) == NULL)
        return puts("mkdtemp"), exit(EXIT_FAILURE), -1;
    if (chmod(cagedir, 0777))
        return puts("chmod"), exit(EXIT_FAILURE), -1;

    const char* binpath  = catpath(cagedir, relbinary);
    const char* flagpath = catpath(cagedir, relflag);

    if (readfile(binpath)) return -1;

    int pid = fork();
    if (!pid) {
        if (chroot(cagedir))
            return puts("chroot"), exit(EXIT_FAILURE), -1;
        if (chdir("/"))
            return puts("chdir"), exit(EXIT_FAILURE), -1;
        uid_t uid = 65535;
        gid_t gid = 65535;
        setregid(gid, gid);
        setgroups(1, &gid);
        setreuid(uid, uid);
        close(0); close(1); close(2);
        return execlp(relbinary, relbinary, NULL);
    }

    int wstatus;
    if (waitpid(pid, &wstatus, 0) < 0)
        return perror("waitpid"), exit(EXIT_FAILURE), -1;

    if (!WIFEXITED(wstatus) || WEXITSTATUS(wstatus))
        return puts("exec fail"), exit(EXIT_FAILURE), -1;

    char* realflag = mapfile(flag);
    char* userflag = mapfile(flagpath);

    if (strcmp(realflag, userflag))
        return puts("flag not match"), exit(EXIT_FAILURE), -1;

    puts(userflag);
}
