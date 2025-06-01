// gcc -Wl,-z,lazy infinite_connect_four.c -o infinite_connect_four

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>

char player1symbol;
char player2symbol;

char board[8][8] = {
    '\x20', '\x20', '\x20', '\x20', '\x20', '\x20', '\x20', '\x20', 
    '\x20', '\x20', '\x20', '\x20', '\x20', '\x20', '\x20', '\x20', 
    '\x20', '\x20', '\x20', '\x20', '\x20', '\x20', '\x20', '\x20', 
    '\x20', '\x20', '\x20', '\x20', '\x20', '\x20', '\x20', '\x20', 
    '\x20', '\x20', '\x20', '\x20', '\x20', '\x20', '\x20', '\x20', 
    '\x20', '\x20', '\x20', '\x20', '\x20', '\x20', '\x20', '\x20', 
    '\x20', '\x20', '\x20', '\x20', '\x20', '\x20', '\x20', '\x20', 
    '\x20', '\x20', '\x20', '\x20', '\x20', '\x20', '\x20', '\x20'
};

void setup(){
    setvbuf(stdout, NULL, _IONBF, 0);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
}

void printbanner() {
    printf("   .::::     .::::.      .::::     .::::       ::::.     ::::.       ::::.     ::::.\n");    
    printf("   .::::     .::::.      .::::     .::::       ::::.     ::::.       ::::.     ::::.\n");    
    printf("  :::::::.  :::::::.    ::::::::  ::::::::   ::::::::  .:::::::    .:::::::  .:::::::\n");   
    printf("   .::::      ::::       .::::.    .::::.     .::::.    .::::.      .:::::    .:::::\n");    
    printf("     ..        ..          :.        :.         .:        .:          ::.       ::.\n");     
    printf("\n");                                                                                      
    printf(".+++=--=+++++++=--=++++++=---=++++++=---+++++++=--=+++++++=--=+++++++---=++++++=---=++=\n"); 
    printf(".#=      -*#*-     .=##*:     .+##+.     :*##=.     -*#*-      =##*:     .+##+.     :*+\n"); 
    printf(".+        -#-        +#.        **        :#+        -#-        +#:        *#.       .+\n"); 
    printf(".+        =#-        +#.        **        :#+        =#=        +#:        *#.       .+\n"); 
    printf(".#+.    .=###=.    .+##*-     :*##*:     -*##+.    .=###=.    .+##*-     :+##*:     -*+\n"); 
    printf(".###*++*#######*++*######**++*######*++**######*++*#######*++*######**++*######*++**##+\n"); 
    printf(".#*-.  .-*###+-.  .-*###+:. .:=*##*=:. .:+###*-.  .-+###+-.  .-*###+:. .:=*##*=:. .:+#+\n"); 
    printf(".*        +#=        *#-       .**.       -#*        +#+        *#-       .*#:       -+\n"); 
    printf(".=        -#:        =#         **        .#=        -#-        =#.        *#         +\n"); 
    printf(".*.      .*#*.      :*#=       -##-       +#*:      .*#*.      .*#+       -##=       =+\n");
    printf(".##+--:-+####*+-:--+####*=-:-=*####*=-:-=*####+--:-+*###*+-:--+####*=-:-=*####*=-:-=*#+\n"); 
    printf(".##*=--=+#####+=--=*####*+---=*####*=---+*####*=--=+#####+=--=*####*+---=*####*=---+*#+\n"); 
    printf(".*:      :*#*.      -*#+.      =##=      .+#*-      .*#*.      :*#+.      -##=      .++\n"); 
    printf(".=        -#:        =#         **        :#=        -#-        =#:        *#         +\n"); 
    printf(".*        +#=        *#-       .**.       -#*        +#+        *#-       .*#:       -+\n"); 
    printf(".#*-.   :+###+:   .-*###=.   .=*##*=.   :=###*-.   :+###+:   .-*###=:   .-*##*=.   .=#+\n"); 
    printf(".###****#######****#######***########***########***#######****#######***########***###+\n"); 
    printf(".#+:    .=###=.    :+##*-.    :*##*:    .-*##+:    .=###=.    :+##*-.    :+##*:    .-*+\n"); 
    printf(".+        =#-        +#.        **        :#+        =#=        +#:        *#.       .+\n"); 
    printf(".+        -#:        +#.        **        :#+        -#-        +#:        *#        .+\n"); 
    printf(".#-      -*#*:     .=##*:     .+##+.     :*##=.     :*#*:      -##*:     .=##+.     :*+\n"); 
    printf(".##*+==+*#####*+==+######*+=+*######*+=+*######+==+*#####*+==+*#####*+=+*######*+=+*##+\n"); 
    printf(".#*=:..:=*###*=:..:=*###*-:..-+#####----######+:..:=*###*=:..:=*###*-:..-+*###+-:.:-*#+\n"); 
    printf(".*.       +#+       .*#=       :*#--------##*.       +#+       .*#=       :*#-       =+\n"); 
    printf(".=        -#:        =#         *#---------#=        -#-        =#.        *#         +\n"); 
    printf(".*.       +#+       .*#=       :*#--------##*.       +#+       .*#=       :*#-       =+\n"); 
    printf(".#*=:..:=*###*=:..:=*###*-:..-+#####----######+:..:=*###*=:..:=*###*-:..-+*###+-:.:-*#+\n"); 
    printf(".##*+==+*#####*+==+*##########################*+==+*#####*+==+*#####*===+*####*+===+##+\n"); 
    printf(".#-      :*#*:      -###-------####-------###-      :*#*:      -##*.      =##+.     .*+\n"); 
    printf(".+        -#:        +#---------##---------#+        -#-        +#:        *#        .+\n"); 
    printf(".+        =#-        +#---------##---------#+        =#=        +#:        *#.       .+\n"); 
    printf(".#+:    .=###=.    :+####------####------####+:    .=###=.    :+##*-.    :+##*:    .-*+\n"); 
    printf(".####***#######***#############################****#######***#######**++**######***###+\n"); 
    printf(".#*=----=*###+:   .-*###+=----+*##*+----=+###*-.   :+###*=----=*##*+*####*+*#*=.   .=#+\n"); 
    printf(".*-::::::-+#=        *#=:::::::-**-:::::::+#*        =#+-::::::-*+*########+*:       :+\n"); 
    printf(".+::::::::=#:        =#-::::::::**::::::::=#=        -#=::::::::++#########*+         +\n"); 
    printf(".*=-:::::=*#*.      -*#*-:::::-+##+-:::::-*#*-      .*#*-:::::-=**+#######*+*=      .++\n"); 
    printf(".##*++++*#####+=--=*####*+++++*####*++++**####*=--=+#####*++++*###**+****+**##*+=-=+*#+\n"); 
    printf(".####--######*=-::-+######---######*+===+*####*+===+*###*+===+*######---########---###+\n"); 
    printf(".#--------##*.      :*##-------###+-:::::-*#*=::::::-*#*-::::::=*##--------###-------#+\n"); 
    printf(".#--------##:        =#---------#*::::::::=#+::::::::=#=::::::::+#---------##---------+\n"); 
    printf(".#--------##=        *##--------#*=::::::-+#*-::::::-*#*-::::::-*##--------##--------#+\n"); 
    printf(".###----#####*-. .:=*####-----#####+=---=*###*+=---=*###*=---=+*####-----######-----##+\n"); 
    printf(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::. \n");
}

void preparegame() {
    printf("Enter player 1 symbol > ");
    player1symbol = (char) getchar();
    getchar();
    printf("Enter player 2 symbol > ");
    player2symbol = (char) getchar();
    getchar();
}

bool checkgameended() {
    // check for horizontal wins
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j <= 4; j++) {
            if ((board[i][j] == board[i][j + 1]
            && board[i][j + 1] == board[i][j + 2]
            && board[i][j + 2] == board[i][j + 3]) 
            && (board[i][j] == player1symbol || board[i][j] == player2symbol)) {
                return true;
            }
        }
    }
    // check for vertical wins
    for (int j = 0; j < 8; j++) {
        for (int i = 0; i <= 4; i++) {
            if ((board[i][j] == board[i + 1][j]
            && board[i + 1][j] == board[i + 2][j]
            && board[i + 2][j]== board[i + 3][j])
            && (board[i][j] == player1symbol || board[i][j] == player2symbol)) {
                return true;
            }
        }
    }
    // check for diagonal wins (bottom left to top right)
    for (int i = 0; i <= 4; i++) {
        for (int j = 0; j <= 4; j++) {
            if ((board[i][j]  == board[i + 1][j + 1]
            && board[i + 1][j + 1] == board[i + 2][j + 2]
            && board[i + 2][j + 2] == board[i + 3][j + 3]) 
            && (board[i][j] == player1symbol || board[i][j]  == player2symbol)) {
                return true;
            }
        }
    }

    // check for diagonal wins (top left to bottom right)
    for (int i = 3; i < 8; i++) {
        for (int j = 0; j <= 4; j++) {
            if ((board[i][j] == board[i - 1][j + 1]
            && board[i - 1][j + 1] == board[i - 2][j + 2]
            && board[i - 2][j + 2] == board[i - 3][j + 3])
            && (board[i][j] == player1symbol || board[i][j] == player2symbol)) {
                return true;
            }    
        }
    }
    return false;
}

void printboard() {
    puts("---------------------------------");
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
            putchar('|');
            putchar(' ');
            if (board[7 - i][j] == player1symbol || board[7 - i][j]  == player2symbol) {
                putchar(board[7 - i][j]);
            } else {
                putchar(' ');
            }
            putchar(' ');
        }
        puts("|");
        puts("---------------------------------");
    }
}

// return true if game has ended
bool game(bool player) {
    char currsym;
    if (player) {
        currsym = player1symbol;
        printf("Player 1 choose your column (0 - 7) > ");
    } else {
        currsym = player2symbol;
        printf("Player 2 choose your column (0 - 7) > ");
    }
    char col = getchar();
    getchar();
    if (col < '0' || col > '7') {
        printf("erm... what the sigma?\n");
        exit(1);
    }
    int colint = col - '0';
    if (board[7][colint] == player1symbol || board[7][colint] == player2symbol) {
        // we have to shift the entire column down
        int lastfree = 0;
        while (board[lastfree][colint] == player1symbol || board[lastfree][colint] == player2symbol) {
            lastfree--;
        }
        while (true) {
            if (lastfree == 7 || (board[lastfree + 1][colint] != player1symbol && board[lastfree + 1][colint] != player2symbol)) {
                board[lastfree][colint] = currsym;
                break;
            }
            board[lastfree][colint] = board[lastfree + 1][colint];
            lastfree++;
        }
    } else {
        // the column still has space
        int x = 0;
        
        while (board[x][colint] == player1symbol || board[x][colint] == player2symbol) {
            x++;
        }
        board[x][colint] = currsym;
    }

    printboard();
    return checkgameended();
}

void win() {
    system("/bin/sh");
}

int main() {                 
    setup();                                         
    printbanner();
    preparegame();
    bool game_ended = false;
    // player = true for player1
    bool player = true;
    while (!game_ended) {
        game_ended = game(player);
        player = !player;
    } 
    char name[16];
    puts("Enter your name winner!");
    fgets(name, 16, stdin);
    printf("Player %s won!\n", name);
}