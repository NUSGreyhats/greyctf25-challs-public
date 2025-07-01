// gcc -Wl,-z,relro,-z,now yourprog.c -o yourprog
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

#define MAX_POOPS 5
const int MAX_MESSES = 2;

int poops_used = 0;
int messes_used = 0;

void* poopsies[MAX_POOPS];

struct Poop {
    long poopsize;
    void* poopAddress;
};

void setup(){
    setvbuf(stdout, NULL, _IONBF, 0);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
}

void take_a_big_poop() {
    if (poops_used >= MAX_POOPS) {
        puts("You've pooped too many times!");
        return;
    }
    void* curpoop = malloc(0x800);
    struct Poop* poopwrapper = malloc(sizeof(struct Poop));
    poopwrapper->poopsize = 0x800;
    poopwrapper->poopAddress = curpoop;
    printf("Poop taken at index %d\n", poops_used);
    poopsies[poops_used] = poopwrapper;
    poops_used++;
}

void clear_poop() {
    puts("Which poop would you like to clear?");
    int idx;
    scanf("%d", &idx);
    if (idx < 0 || idx >= MAX_POOPS) {
        puts("Invalid index.");
        return;
    }
    struct Poop* curpoop = poopsies[idx];
    if (curpoop == NULL) {
        puts("There's no poop here...");
        return;
    }
    free(curpoop->poopAddress);
    curpoop->poopsize = 0;
    puts("All done!");
}

void view_poop() {
    puts("Which poop would you like to view?");
    int idx;
    scanf("%d", &idx);
    if (idx < 0 || idx >= MAX_POOPS) {
        puts("Invalid index.");
        return;
    }
    struct Poop* curpoop = poopsies[idx];
    if (curpoop == NULL) {
        puts("There's no poop here...");
        return;
    }
    printf("Oh! Someone took a poop of size 0x%lx at %p!", curpoop->poopsize, curpoop->poopAddress);
    printf("The poop content was: %s", curpoop->poopAddress);
}

void mess_with_poop() {
    if (messes_used >= MAX_MESSES) {
        puts("With your entire body smelling like poop, you get taken out by security...");
        exit(0);
    }
    messes_used++;
    puts("You decide to get dirty and mess with your poop...");
    puts("Which poop would you like to mess with?");
    int idx;
    scanf("%d", &idx);
    if (idx < 0 || idx >= MAX_POOPS) {
        puts("Invalid index.");
        return;
    }
    struct Poop* curpoop = poopsies[idx];
    if (curpoop == NULL) {
        puts("There's no poop here...");
        return;
    }
    long curpoopsize = curpoop->poopsize;
    puts("Which part of your poop would you like to mess with?");
    long offset;
    scanf("%ld", &offset);
    if (offset < 0 || idx >= curpoopsize) {
        puts("Invalid offset.");
        return;
    }
    char* addr_to_mess = curpoop->poopAddress + offset;
    puts("Enter your modified poop: ");
    read(0, addr_to_mess, curpoopsize);
    puts("Poop modified! Now don't be doing that again!");
}

void banner() {
    puts("What would you like to do?");
    puts("1. Clear poop");
    puts("2. Take a big poop");
    puts("3. View poop");
    puts("4. Mess with poop");
    puts("5. Leave the toilet");
    printf("> ");
}

int main() {
    setup();
    puts("Welcome to the toilet!");
    while (1) {
        banner();
        int opt;
        scanf("%u", &opt);
        if (opt == 1) {
            clear_poop();
        } else if (opt == 2) {
            take_a_big_poop();
        } else if (opt == 3) {
            view_poop();
        } else if (opt == 4) {
            mess_with_poop();
        } else if (opt == 5) {
            exit(0);
        } else {
            puts("Erm... I don't think you can do that in the toilet.");
        }
    }
}