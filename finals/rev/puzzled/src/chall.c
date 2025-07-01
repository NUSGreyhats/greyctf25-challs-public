#include <time.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/ptrace.h>


// Rubik's cube state representation
// Each face has 9 positions (3x3), represented as integers 0-5 (colors)
// Faces: 0=Front, 1=Back, 2=Left, 3=Right, 4=Up, 5=Down
uint8_t cube[6][9] = {0, 1, 5, 0, 0, 4, 1, 1, 4, 3, 4, 0, 2, 1, 5, 5, 2, 0, 4, 0, 4, 3, 2, 5, 5, 4, 3, 2, 5, 4, 1, 3, 4, 2, 2, 3, 2, 3, 1, 3, 4, 1, 3, 2, 1, 5, 3, 1, 0, 5, 5, 2, 0, 0};

// Check if cube is in solved state
int is_solved() {
	char scrap_space[0x10];
	for (int face = 0; face < 6; face++) {
		for (int pos = 0; pos < 9; pos++) {
			if (cube[face][pos] != face) {
				return 0;
			}
		}
	}
	return 1;
}

// Rotate a face clockwise
void rotate_face(int face) {
	int temp[9];
	for (int i = 0; i < 9; i++) {
		temp[i] = cube[face][i];
	}
	// Rotate positions: 0->2, 1->5, 2->8, 3->1, 4->4, 5->7, 6->0, 7->3, 8->6
	cube[face][0] = temp[6]; cube[face][1] = temp[3]; cube[face][2] = temp[0];
	cube[face][3] = temp[7]; cube[face][4] = temp[4]; cube[face][5] = temp[1];
	cube[face][6] = temp[8]; cube[face][7] = temp[5]; cube[face][8] = temp[2];
}

// Perform F move (Front face rotation)
void move_f() {
	rotate_face(0);
	// Rotate adjacent edges
	int temp[3];
	// Save bottom edge of Up face
	temp[0] = cube[4][6]; temp[1] = cube[4][7]; temp[2] = cube[4][8];
	// Up <- Left
	cube[4][6] = cube[2][8]; cube[4][7] = cube[2][5]; cube[4][8] = cube[2][2];
	// Left <- Down
	cube[2][2] = cube[5][0]; cube[2][5] = cube[5][1]; cube[2][8] = cube[5][2];
	// Down <- Right
	cube[5][0] = cube[3][6]; cube[5][1] = cube[3][3]; cube[5][2] = cube[3][0];
	// Right <- temp (Up)
	cube[3][0] = temp[0]; cube[3][3] = temp[1]; cube[3][6] = temp[2];
}

// Perform B move (Back face rotation)
void move_b() {
	rotate_face(1);
	int temp[3];
	temp[0] = cube[4][0]; temp[1] = cube[4][1]; temp[2] = cube[4][2];
	cube[4][0] = cube[3][2]; cube[4][1] = cube[3][5]; cube[4][2] = cube[3][8];
	cube[3][2] = cube[5][8]; cube[3][5] = cube[5][7]; cube[3][8] = cube[5][6];
	cube[5][8] = cube[2][6]; cube[5][7] = cube[2][3]; cube[5][6] = cube[2][0];
	cube[2][0] = temp[2]; cube[2][3] = temp[1]; cube[2][6] = temp[0];
}

// Perform L move (Left face rotation)
void move_l() {
	rotate_face(2);
	int temp[3];
	temp[0] = cube[4][0]; temp[1] = cube[4][3]; temp[2] = cube[4][6];
	cube[4][0] = cube[1][8]; cube[4][3] = cube[1][5]; cube[4][6] = cube[1][2];
	cube[1][2] = cube[5][6]; cube[1][5] = cube[5][3]; cube[1][8] = cube[5][0];
	cube[5][0] = cube[0][0]; cube[5][3] = cube[0][3]; cube[5][6] = cube[0][6];
	cube[0][0] = temp[0]; cube[0][3] = temp[1]; cube[0][6] = temp[2];
}

// Perform R move (Right face rotation)
void move_r() {
	rotate_face(3);
	int temp[3];
	temp[0] = cube[4][2]; temp[1] = cube[4][5]; temp[2] = cube[4][8];
	cube[4][2] = cube[0][2]; cube[4][5] = cube[0][5]; cube[4][8] = cube[0][8];
	cube[0][2] = cube[5][2]; cube[0][5] = cube[5][5]; cube[0][8] = cube[5][8];
	cube[5][2] = cube[1][6]; cube[5][5] = cube[1][3]; cube[5][8] = cube[1][0];
	cube[1][0] = temp[2]; cube[1][3] = temp[1]; cube[1][6] = temp[0];
}

// Perform U move (Up face rotation)
void move_u() {
	rotate_face(4);
	int temp[3];
	temp[0] = cube[0][0]; temp[1] = cube[0][1]; temp[2] = cube[0][2];
	cube[0][0] = cube[3][0]; cube[0][1] = cube[3][1]; cube[0][2] = cube[3][2];
	cube[3][0] = cube[1][0]; cube[3][1] = cube[1][1]; cube[3][2] = cube[1][2];
	cube[1][0] = cube[2][0]; cube[1][1] = cube[2][1]; cube[1][2] = cube[2][2];
	cube[2][0] = temp[0]; cube[2][1] = temp[1]; cube[2][2] = temp[2];
}

// Perform D move (Down face rotation)
void move_d() {
	rotate_face(5);
	int temp[3];
	temp[0] = cube[0][6]; temp[1] = cube[0][7]; temp[2] = cube[0][8];
	cube[0][6] = cube[2][6]; cube[0][7] = cube[2][7]; cube[0][8] = cube[2][8];
	cube[2][6] = cube[1][6]; cube[2][7] = cube[1][7]; cube[2][8] = cube[1][8];
	cube[1][6] = cube[3][6]; cube[1][7] = cube[3][7]; cube[1][8] = cube[3][8];
	cube[3][6] = temp[0]; cube[3][7] = temp[1]; cube[3][8] = temp[2];
}

void process_move(char move) {
	char scrap_space[0x10];
	if (move == 'a')
		move_f();
	else if (move == 'b')
		move_b();
	else if (move == 'c')
		move_l();
	else if (move == 'd')
		move_r();
	else if (move == 'e')
		move_u();
	else if (move == 'f')
		move_d();
}

void read_flag() {
	char scrap_space[0x10];
	FILE *file = fopen("flag.txt", "r");
	if (file == NULL) {
		printf("Configuration file not found.\n");
		return;
	}
	
	char line[256];
	while (fgets(line, sizeof(line), file)) {
		printf("%s", line);
	}
	fclose(file);
}

// Anti-debugging mechanism with added evasion techniques
void detect_debugger(void) {
	char stack_space[0x20];

    // Fork and check for debugger
    pid_t child = fork();

    if (child == 0) {
        // Child process checks if it's being traced
        if (ptrace(PTRACE_TRACEME, 0, NULL, NULL) == -1) {
            // If we can't trace ourselves, someone else is tracing us
            _exit(1);  // Use _exit to avoid flushing buffers
        }
        _exit(0);  // Child exits normally
    } else if (child > 0) {
        // Parent process
        int status;
        waitpid(child, &status, 0);

        // If child exit code was 1, a debugger was detected
        if (WEXITSTATUS(status) == 1) {
            // Anti-debugging detected; take evasive action
            // Obfuscate our exit by corrupting some memory first
			printf("Access denied. Sequence invalid.\n");
            exit(0);
        }
    }

}

void deobfs_string(char* str) {
	char stack_space[0x20];

	for (int i = 0; ; i++) {
		if (!str[i])
			return;
		str[i] ^= 0x41;
	}
}

char gdb[] = "&%#";
char strace[] = "253 \"$";
char ltrace[] = "-53 \"$";
char radare2[] = "3 % 3$s";
char r2[] = "3s";
char x64dbg[] = "9wu%#&";
char lldb[] = "--%#";

void detect_debugger_2(void) {

    FILE *stat_file;
    char stat_line[1024];
    char parent_comm[256];
    pid_t ppid;
    
    // Open /proc/self/stat
    stat_file = fopen("/proc/self/stat", "r");
    if (!stat_file) {
        return; // Assume not debugged if we can't read
    }
    
    // Read the stat line
    if (!fgets(stat_line, sizeof(stat_line), stat_file)) {
        fclose(stat_file);
        return;
    }
    fclose(stat_file);
    
    // Parse to get PPID (4th field)
    // Format: pid (comm) state ppid ...
    char *token = strtok(stat_line, " ");
    for (int i = 0; i < 3 && token; i++) {
        token = strtok(NULL, " ");
    }
    
    if (!token) return;
    ppid = atoi(token);
    
    // Now check parent process name
    snprintf(parent_comm, sizeof(parent_comm), "/proc/%d/comm", ppid);
    
    FILE *comm_file = fopen(parent_comm, "r");
    if (!comm_file) {
        return;
    }
    
	deobfs_string(gdb);
	deobfs_string(strace);
	deobfs_string(ltrace);
	deobfs_string(radare2);
	deobfs_string(r2);
	deobfs_string(x64dbg);
	deobfs_string(lldb);

    char parent_name[256];
    if (fgets(parent_name, sizeof(parent_name), comm_file)) {
        // Remove newline
        parent_name[strcspn(parent_name, "\n")] = 0;
        
        // Check for common debuggers
        if (strstr(parent_name, gdb) ||
            strstr(parent_name, strace) ||
            strstr(parent_name, ltrace) ||
            strstr(parent_name, radare2) ||
            strstr(parent_name, r2) ||
            strstr(parent_name, x64dbg) ||
            strstr(parent_name, lldb)) {
            fclose(comm_file);
			printf("Access denied. Sequence invalid.\n");
			exit(0);
        }
    }
    
    fclose(comm_file);
    return; // No debugger detected
}

int main() {
	char input[61];
	
	setbuf(stdout, 0);
	setbuf(stdin, 0);
	detect_debugger();

	printf("Enter secret sequence: ");
	if (fgets(input, sizeof(input), stdin) == NULL) {
		printf("Invalid input.\n");
		return 1;
	}
	
	detect_debugger_2();
	// Remove newline if present
	size_t len = strlen(input);
	if (len > 0 && input[len-1] == '\n') {
		input[len-1] = '\0';
		len--;
	}
	
	// init_cube();
	
	// Process each move
	for (size_t i = 0; i < len; i++) {
		if (input[i] != ' ') {
			process_move(input[i]);
		}
	}

	if (is_solved()) {
		printf("Success! Access granted.\n");
		read_flag();
	} else {
		printf("Access denied. Sequence invalid.\n");
	}

	return 0;
}

void __attribute__((used)) lol() {
	asm volatile (
    ".rept 0x20000\n\t"
    ".byte 0x90\n\t"
    ".endr"
	);
}
