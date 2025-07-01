#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <fcntl.h>
#include <unistd.h>

#define AIRCON_COUNT    10

int AIRCON_REMOTE_TEMP[AIRCON_COUNT] = { 0 };
int AIRCON_ACTUAL_TEMP[AIRCON_COUNT] = { 0 };

void setup(){
    setbuf(stdin, 0);
	setbuf(stdout, 0);
    setbuf(stderr, 0);
}

void setup_aircon() {
    // set temperature of aircon to be different, from 20 - 29 degree celsius
    for (int i = 0; i < AIRCON_COUNT; i++) {
        AIRCON_REMOTE_TEMP[i] = 20 + i;
        AIRCON_ACTUAL_TEMP[i] = 20 + i;
    }
}

void display_menu() {
	puts("1. Change air-con temp");
    puts("2. View air-con temps");
	puts("3. Get flag\n");
}

bool validate_inputs(__int16_t remote_id, __int16_t temperature) {
    if (remote_id < 0 || remote_id >= AIRCON_COUNT) {
        puts("\nError: Your input air-con remote ID doesn't exist!\n");
        return false;
    }
    if (temperature < 20 || temperature >= 30) {
        puts("\nError: Your input temperature is too cold/hot!\n");
        return false;
    }
    return true;
}

bool aircon_has_same_temps() {
    puts("\nChecking that all air-con temperatures are different ...");
    for (int i = 0; i < AIRCON_COUNT; i++) {
        for (int j = i + 1; j < AIRCON_COUNT; j++) {
            if (AIRCON_REMOTE_TEMP[i] == AIRCON_REMOTE_TEMP[j]) {
                puts("\nError: Different air-cons have the same temperature displayed! I'm kicking u out!\n");
                return true;
            }
        }
    }
    puts("Successfully updated air-con temperature!\n");
    return false;
}

void change_aircon_temp() {
    __int16_t remote_id = 0;
    __int16_t aircon_id = 0;
    __int16_t temperature = 0;
       
    puts("\nWhich air-con remote to use: ");
    scanf("%d", &remote_id);
    
    aircon_id = remote_id; // aircon remote ID should match the ID of the actual aircon
    
    puts("\nWhat temperature to set to: ");
    scanf("%d", &temperature);
    
    if (validate_inputs(remote_id, temperature)) {
        puts("\nChanging temperature on remote ... ");
        AIRCON_REMOTE_TEMP[remote_id] = temperature;
        
        // NEXT TIME CAN INTRODUCE A RACE CONDITION BUG HERE!
        
        puts("Updating temperature of air-con ...");
        AIRCON_ACTUAL_TEMP[aircon_id] = AIRCON_REMOTE_TEMP[remote_id];
        
        if (aircon_has_same_temps()) {
            exit(1);
        }
    }
}

void view_aircon_temps() {
    // set temperature of aircon to be different, from 20 - 29 degree celsius
    puts("");
    for (int i = 0; i < AIRCON_COUNT; i++) {
        printf("[ID %d] Remote Temp: %d, Actual Temp: %d\n", i, AIRCON_REMOTE_TEMP[i], AIRCON_ACTUAL_TEMP[i]);
    }
    puts("");
}

void cat_flag() {
    for (int i = 0; i < AIRCON_COUNT; i++) {
        if (AIRCON_ACTUAL_TEMP[i] != 25) {
            puts("\nError: Not all air-cons are set to 25 degree celsius! I'm kicking u out!\n");
            exit(1);
        } 
    }
    
    int fd = open("flag.txt", O_RDONLY);
    if (fd < 0) {
        perror("Failed to open flag.txt");
        exit(1);
    }
    
    char buffer[128];
    ssize_t bytes_read = read(fd, buffer, sizeof(buffer) - 1);
    if (bytes_read < 0) {
        perror("Failed to read flag.txt");
        close(fd);
        exit(1);
    }

    buffer[bytes_read] = '\0';
    printf("\nFlag: %s\n", buffer);
    close(fd);
    exit(1);
}


int main() {
    setup();
    setup_aircon();
    
    int choice;
    while (1) {
		display_menu();
        printf("> ");
		scanf("%d", &choice);
		getchar();
		switch (choice) {
			case 1:
				change_aircon_temp();
				break;
            case 2:
				view_aircon_temps();
				break;
			case 3:
				cat_flag();
				break;
			default:
                printf("\033[2J\033[H");
				break;
		}
	}
}
