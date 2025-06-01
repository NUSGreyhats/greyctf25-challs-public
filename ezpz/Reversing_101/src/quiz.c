/*
*
* 1. what is the address of the main function in hex (i.e. 0x1234)
* 2. what is the name of the libc function that has the same effect as function a?
* 3. what is the length of the correct password?
* 4. function b returns a constant value that is later used to check the password. what is the value returned by the function?
* 5. function c implements a popular encryption algorithm. what is this algorithm?
* 6. finally, what is the correct password for this program?
*
*
* the answers are
* 1. 0x402db6
* 2. strlen
* 3. 0xf or 15
* 4. 13969625720425389615 or 0xc1de1494171d9e2f
* 5. rc4 (case insensitive)
* 6. honk-mimimimimi (case sensitive)
*
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

// ANSI color codes
#define RESET   "\033[0m"
#define RED     "\033[31m"
#define GREEN   "\033[32m"
#define YELLOW  "\033[33m"
#define BLUE    "\033[34m"
#define MAGENTA "\033[35m"
#define CYAN    "\033[36m"
#define WHITE   "\033[37m"
#define BOLD    "\033[1m"

void print_banner(void) {
    printf(BOLD CYAN "╔══════════════════════════════════════════════════════════════╗\n");
    printf("║" RESET CYAN "              REVERSE ENGINEERING QUIZ CHALLENGE              " BOLD CYAN "║\n");
    printf("╚══════════════════════════════════════════════════════════════╝\n" RESET);
    printf(YELLOW "Answer all questions correctly to reveal the flag!\n" RESET);
    printf("─────────────────────────────────────────────────────────────────\n\n");
}

void print_flag(void) {
    FILE *file = fopen("flag.txt", "r");
    if (file == NULL) {
        printf(YELLOW "flag.txt not found, but you got all answers correct!\n" RESET);
        printf(GREEN BOLD "🎉 CONGRATULATIONS! YOU PASSED THE QUIZ! 🎉\n" RESET);
        return;
    }
    
    printf(GREEN BOLD "\n🎉 CONGRATULATIONS! HERE'S YOUR FLAG: 🎉\n" RESET);
    printf(CYAN "─────────────────────────────────────────\n" RESET);
    
    char buffer[256];
    while (fgets(buffer, sizeof(buffer), file)) {
        printf(BOLD WHITE "%s" RESET, buffer);
    }
    
    printf(CYAN "\n─────────────────────────────────────────\n" RESET);
    fclose(file);
}

void exit_wrong(void) {
    printf(RED BOLD "\n❌ WRONG ANSWER! QUIZ TERMINATED.\n" RESET);
    exit(1);
}

int main(void) {
    char input[256];
    uint64_t num_input;
    
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
    print_banner();
    
    // Question 1
    printf(BOLD BLUE "Question 1:" RESET " What is the address of the main function in hex (i.e. 0x1234)?\n");
    printf(CYAN "Answer: " RESET);
    if (scanf("%255s", input) != 1) exit_wrong();
    if ((strcmp(input, "0x402db6") != 0) && (strcmp(input, "4206006") != 0) && (strcmp(input, "0x402DB6") != 0)) {
        exit_wrong();
    }
    printf(GREEN "✓ Correct!\n\n" RESET);
    
    // Question 2
    printf(BOLD BLUE "Question 2:" RESET " What is the name of the libc function that has the same effect as function a?\n");
    printf(BOLD BLUE "Hint:" RESET " We can try dis-assembling or de-compiling the program to understand what the function is doing.\n");
    printf(CYAN "Answer: " RESET);
    if (scanf("%255s", input) != 1) exit_wrong();
    if (strcmp(input, "strlen") != 0) {
        exit_wrong();
    }
    printf(GREEN "✓ Correct!\n\n" RESET);
    
    // Question 3
    printf(BOLD BLUE "Question 3:" RESET " What is the length of the correct password?\n");
    printf(CYAN "Answer: " RESET);
    if (scanf("%255s", input) != 1) exit_wrong();
    if (strcmp(input, "0xf") != 0 && strcmp(input, "15") != 0) {
        exit_wrong();
    }
    printf(GREEN "✓ Correct!\n\n" RESET);
    
    // Question 4
    printf(BOLD BLUE "Question 4:" RESET " Function b returns a constant value that is later used to check the password. What is the value returned by the function?\n");
    printf(BOLD BLUE "Hint:" RESET " If a function is too complex, we can use a debugger to analyze the values at runtime! Note that the return value is typically stored in the RAX register at the end of a function.\n");
    printf(CYAN "Answer: " RESET);
    if (scanf("%255s", input) != 1) exit_wrong();
    if (strcmp(input, "13969625720425389615") != 0 && strcmp(input, "0xc1de1494171d9e2f") != 0) {
        exit_wrong();
    }
    printf(GREEN "✓ Correct!\n\n" RESET);
    
    // Question 5
    printf(BOLD BLUE "Question 5:" RESET " Function c implements a popular encryption algorithm. What is this algorithm?\n");
    printf(BOLD BLUE "Hint:" RESET " Google or even ChatGPT is your best friend.\n");
    printf(CYAN "Answer: " RESET);
    if (scanf("%255s", input) != 1) exit_wrong();
    // Convert to lowercase for case insensitive comparison
    for (int i = 0; input[i]; i++) {
        if (input[i] >= 'A' && input[i] <= 'Z') {
            input[i] = input[i] + 32;
        }
    }
    if (strcmp(input, "rc4") != 0) {
        exit_wrong();
    }
    printf(GREEN "✓ Correct!\n\n" RESET);
    
    // Question 6
    printf(BOLD BLUE "Question 6:" RESET " Finally, what is the correct password for this program?\n");
    printf(CYAN "Answer: " RESET);
    if (scanf("%255s", input) != 1) exit_wrong();
    if (strcmp(input, "honk-mimimimimi") != 0) {  // Case sensitive
        exit_wrong();
    }
    printf(GREEN "✓ Correct!\n\n" RESET);
    
    // All answers correct!
    print_flag();
    
    return 0;
}
