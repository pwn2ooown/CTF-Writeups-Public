#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

char *gNotes[16];
int gSizes[16];

void create_note() {
	int index, size;
	void *chunk;

	printf("Index: ");
	scanf("%i", &index);
	getchar();
	printf("Size: ");
	scanf("%i", &size);
        getchar();

	if ((index >= 0 && index <= 16) && (size > 0 && size < 0x410)) {
		chunk = malloc(size);
		gNotes[index] = chunk;
		gSizes[index] = size;
	} else {
		printf("no\n");
	}
}

void delete_note() {
	int index;

	printf("Index: ");
        scanf("%i", &index);
        getchar();

	if (index >= 0 && index <= 16) {
		free(gNotes[index]);
		gNotes[index] = NULL;
		gSizes[index] = 0;
	} else {
		printf("Not a valid index dumbass\n");
	}
}

void read_note() {
	int index;

        printf("Index: ");
        scanf("%i", &index);
        getchar();

	if (gNotes[index] != NULL && (index >= 0 && index <= 16)) {
		printf("Content: %s\n", gNotes[index]);
	}
}

void edit_note() {
	int index;

        printf("Index: ");
        scanf("%i", &index);
        getchar();

	if (gNotes[index] != NULL && (index >= 0 && index <= 16)) {
		printf("Content: ");
		read(0, gNotes[index], gSizes[index]);
	}
}

void menu() {
	printf("1. New note\n");
	printf("2. Delete note\n");
	printf("3. Read note\n");
	printf("4. Edit note\n");
	printf("5. Exit\n");
	printf("> ");
}

void ignore_buffering() {
	setbuf(stdout, NULL);
	setbuf(stdin, NULL);
}

int main() {
	char choice;

	ignore_buffering();

	printf("Welcome to the pinnacle of C projects; the notes app. Except this one is memory-safe, so no UAF for you :)\n");
	do {
		menu();
		scanf("%c", &choice);
		getchar();

		switch (choice) {
			case '1':
				create_note();
				break;
			case '2':
				delete_note();
				break;
			case '3':
				read_note();
				break;
			case '4':
				edit_note();
				break;
		}
	} while (choice != '5');
}
