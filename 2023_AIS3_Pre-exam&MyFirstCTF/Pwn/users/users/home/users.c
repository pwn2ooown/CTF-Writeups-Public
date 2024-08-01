#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <error.h>

__attribute__((constructor))
static void initproc() {
    setvbuf(stdin , NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

typedef struct User User_t;
typedef void (*fp)(User_t*);
#define SIZE 10

struct User {
    char name[8];
    char* data;
    fp function;
};

void User_admin(User_t* user) {
    system("id");
    printf(user->data, user->name);
}
void User_guest(User_t* user) {
    puts(user->data);
}

User_t* users[SIZE];

int readint(const char* prompt) {
    printf("%s", prompt);
    int i;
    scanf("%d", &i);
    return i;
}

int readstr(const char* prompt, char* buf, int size) {
    printf("%s", prompt);
    int r = read(STDIN_FILENO, buf, size);
    strtok(buf, "\n");
    return r;
}

int menu() {
    puts("---- menu ----");
    puts("[1] reset");
    puts("[2] new user");
    puts("[3] del user");
    puts("[4] do function");
    puts("[5] view users");
    puts("[6] exit");
    int r = readint("> ");
    return r;
}

int readidx() {
    int idx = readint("index > ");
    if (idx < 0 || SIZE <= idx) {
        puts("index error");
        return 0;
    }
    return idx;
}

void newUser() {
    int idx = readidx();
    if (!idx) return;
    User_t* ptr = malloc(sizeof(User_t));
    readstr("name > ", ptr->name, sizeof(ptr->name));
    int size = readint("size > ");
    ptr->data = malloc(size);
    readstr("data > ", ptr->data, size);
    users[idx] = ptr;
}

void delUser() {
    int idx = readidx();
    if (!idx) return;
    free(users[idx]->data);
    free(users[idx]);
}

void func() {
    int idx = readidx();
    if (!idx) return;
    User_t* ptr = users[idx];
    if (ptr->function)
        ptr->function(ptr);
    else
        puts("no function");
}

void view() {
    for (int idx = 0; idx < SIZE; idx++) {
        User_t* ptr = users[idx];
        if (ptr) printf("%d: %s\n", idx, ptr->name);
    }
}

int main() {
    printf("users @ %p\n", users);

    users[0] = malloc(sizeof(User_t));
    strcpy(users[0]->name, "admin");
    users[0]->data = strdup("admin");
    users[0]->function = User_admin;

    users[1] = malloc(sizeof(User_t));
    strcpy(users[1]->name, "guest");
    users[1]->data = strdup("guest");
    users[1]->function = User_guest;

    while (1) {
        switch (menu()) {
        case 1:
            return main();
        case 2:
            newUser();
            break;
        case 3:
            delUser();
            break;
        case 4:
            func();
            break;
        case 5:
            view();
            break;
        default:
            exit(0);
        }
    }
}
