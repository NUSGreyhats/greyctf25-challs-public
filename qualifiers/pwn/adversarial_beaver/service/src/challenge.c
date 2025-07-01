#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include <stdbool.h>

typedef unsigned int uint;
#define HALT 0

typedef enum {
    LEFT  = 0,
    RIGHT = 1
} Direction;

static Direction parseDirection(const char *token)
{
    if (strcmp(token, "L") == 0) return LEFT;
    if (strcmp(token, "R") == 0) return RIGHT;
    fprintf(stderr, "Error: Invalid direction: %s\n", token);
    exit(EXIT_FAILURE);
}

typedef struct {
    uint      symbol_0;
    uint      transition_0;
    Direction direction_0;

    uint      symbol_1;
    uint      transition_1;
    Direction direction_1;
} State;

typedef struct {
    uint   n_states;
    State  states[101];      /* index 0 = HALT, 1-100 usable       */
    uint8_t tape[10005];     /* effectively “infinite” tape (0-init) */
} Machine;

static int runMachine(Machine *m)
{
    int score            = 0;
    int current_state_id = 1;
    int tape_bit_index   = 0;
    int tape_byte_index  = 0;

    while (current_state_id != HALT) {
        State *s = &m->states[current_state_id];
        uint tape_bit = (m->tape[tape_byte_index] >> tape_bit_index) & 1U;

        uint      new_bit  = tape_bit ? s->symbol_1     : s->symbol_0;
        Direction dir      = tape_bit ? s->direction_1  : s->direction_0;
        current_state_id   = tape_bit ? s->transition_1 : s->transition_0;

        m->tape[tape_byte_index] &= ~(1U << tape_bit_index);
        m->tape[tape_byte_index] |=  (new_bit << tape_bit_index);
        if (dir == LEFT) {
            if (tape_bit_index == 0) {
                --tape_byte_index;
                tape_bit_index = 7;
            } else {
                --tape_bit_index;
            }
        } else {
            if (tape_bit_index == 7) {
                ++tape_byte_index;
                tape_bit_index = 0;
            } else {
                ++tape_bit_index;
            }
        }
        ++score;
    }
    return score;
}

void alarm_handler(int signum) {
    puts("\nError: Timeout. No infinite programs allowed!");
    exit(EXIT_FAILURE);
}

void init() {
    signal(SIGALRM, alarm_handler);
    alarm(10);
    setvbuf(stdout, NULL, _IONBF, 0);
}

Machine machine;
int main(void)
{
    init();
    puts(
        "\n[ Adversarial Beaver ]\n"
        "\n"
        "       .=\"   \"=._.---.\n"
        "     .\"         c ' Y'`p\n"
        "    /   ,       `.  w_/\n"
        "    |   '-.   /     /\n"
        "_,..._|      )_ -\\ \\_=.\\\n"
        " `-....-'`------)))`=-'\"`'\"'\n"
    );

    printf("Enter the number of states you require (Max 100): ");
    fflush(stdout);
    if (scanf("%u", &machine.n_states) != 1) {
        fputs("Error: Bad input.\n", stderr);
        return EXIT_FAILURE;
    }
    if (machine.n_states < 1 || machine.n_states > 100) {
        fputs("Error: Number of states must be between 1 and 100.\n", stderr);
        return EXIT_FAILURE;
    }

    puts("\nDefine the transitions for each state below!");
    puts("Each transition: <sym_0 (0/1)> <dir_0 (L/R)> <next_0>"
         " <sym_1 (0/1)> <dir_1 (L/R)> <next_1>");
    puts("Example: 1 R 32 0 L 12");
    puts("Note: State 0 is reserved for the HALT state.\n");

    for (uint i = 1; i <= machine.n_states; ++i) {
        State *s = &machine.states[i];
        char dir0[8], dir1[8];

        printf("State %u: ", i);
        fflush(stdout);
        if (scanf("%u %7s %u %u %7s %u",
                  &s->symbol_0, dir0, &s->transition_0,
                  &s->symbol_1, dir1, &s->transition_1) != 6)
        {
            fputs("Error: Bad input.\n", stderr);
            return EXIT_FAILURE;
        }

        if (s->symbol_0 > 1 || s->symbol_1 > 1) {
            fputs("Error: Symbol must be 0 or 1.\n", stderr);
            return EXIT_FAILURE;
        }
        if (s->transition_0 > machine.n_states ||
            s->transition_1 > machine.n_states)
        {
            fprintf(stderr, "Error: Transition state > %u\n",
                    machine.n_states);
            return EXIT_FAILURE;
        }

        s->direction_0 = parseDirection(dir0);
        s->direction_1 = parseDirection(dir1);
    }

    puts("\nRunning your machine...");
    uint score = runMachine(&machine);
    printf("Your machine has a score of: %u\n", score);
    return 0;
}