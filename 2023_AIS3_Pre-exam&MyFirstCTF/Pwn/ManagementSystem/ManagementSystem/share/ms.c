#include <stdio.h>
#include <string.h>
#include <stdlib.h>



void init(){
    setvbuf(stdout,0,2,0);
    setvbuf(stdin,0,2,0);
    setvbuf(stderr,0,2,0);
}

typedef struct User {
    char username[32];
    char user_account[16];
    char user_password[16];
    struct User *next;
} User;

void secret_function() {
    printf("Congratulations! You've successfully executed the secret function.\n");
    char *shell_args[] = {"/bin/sh", NULL};
    execv(shell_args[0], shell_args);
}

User *add_user(User *head) {
    User *new_user = malloc(sizeof(User));
    if (new_user == NULL) {
        printf("Error allocating memory for user.\n");
        exit(1);
    }

    printf("Enter username (max 31 characters): ");
    fgets(new_user->username, sizeof(new_user->username), stdin);
    strtok(new_user->username, "\n"); 

    printf("Enter user account (max 15 characters): ");
    fgets(new_user->user_account, sizeof(new_user->user_account), stdin);
    strtok(new_user->user_account, "\n"); 

    printf("Enter user password (max 15 characters): ");
    fgets(new_user->user_password, sizeof(new_user->user_password), stdin);
    strtok(new_user->user_password, "\n"); 

    new_user->next = NULL;

    if (head == NULL) {
        return new_user;
    } else {
        User *current = head;
        while (current->next != NULL) {
            current = current->next;
        }
        current->next = new_user;
        return head;
    }
}

void show_users(User *head) {
    User *current = head;
    int count = 1;
    while (current != NULL) {
        printf("User %d:\n", count);
        printf("Username: %s\n", current->username);
        printf("User account: %s\n", current->user_account);
        printf("User password: %s\n\n", current->user_password);
        current = current->next;
        count++;
    }
}
User *delete_user(User *head) {
    printf("Enter the index of the user you want to delete: ");
    char buffer[64];
    gets(buffer); 

    int user_index;
    sscanf(buffer, "%d", &user_index);

    if (user_index <= 0) {
        printf("Invalid index.\n");
        return head;
    }

    if (user_index == 1) {
        User *user_to_delete = head;
        head = head->next;
        free(user_to_delete);
        return head;
    }

    User *previous = head;
    User *current = head->next;
    int count = 2;

    while (current != NULL) {
        if (count == user_index) {
            previous->next = current->next;
            free(current);
            return head;
        }

        previous = current;
        current = current->next;
        count++;
    }

    printf("User not found.\n");
    return head;
}

void show_menu() {
    printf("Choose an option:\n");
    printf("1. Add user\n");
    printf("2. Show users\n");
    printf("3. Delete user\n");
    printf("4. Exit\n");
    printf("> ");
}

int main() {

    init();

    int choice;
    User *users = NULL;
    
    while (1) {
        show_menu();
        scanf("%d", &choice);
        getchar(); 
        switch (choice) {
 
            case 1:
                users = add_user(users);
                break;
            case 2:
                show_users(users);
                break;
            case 3:
                users = delete_user(users);
                break;
            case 4:
                printf("Exiting...\n");
                while (users != NULL) {
                    User *temp = users;
                    users = users->next;
                    free(temp);
                }
                exit(0);
                break;
            default:
                printf("Invalid option, please try again.\n");
                break;
        }
    }
    return 0;
}
