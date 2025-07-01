#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <malloc.h>
#define MAX_REPOS 0x100
char* repos[MAX_REPOS];
size_t repo_count = 0; // number of repositories acquired
void acquire_repo() {
	size_t asset_value;
	if (repo_count <= MAX_REPOS) {
		printf("Enter asset value for repo acquisition: $");
		scanf("%zu", &asset_value);
		getchar();
		repos[repo_count++] = calloc(asset_value, sizeof(char));
		puts("Successfully acquired repo for foreclosure.");
	} else {
		puts("Portfolio at maximum capacity.");
	}
}
void update_records() {
	size_t repo_id;
	printf("Enter repo ID to update: ");
	scanf("%zu", &repo_id);
	getchar();
	if (repo_id < repo_count && repos[repo_id]) {
		printf("Enter property records: ");
		fgets(repos[repo_id], malloc_usable_size(repos[repo_id]), stdin);
	} else {
		puts("Invalid repo ID.");
	}
	puts("Records updated.");
}
void examine_property() {
	size_t repo_id;
	printf("Enter repo ID to examine: ");
	scanf("%zu", &repo_id);
	getchar();
	if (repo_id < repo_count && repos[repo_id]) {
		printf("Property details: ");
		puts(repos[repo_id]);
	} else {
		puts("Invalid repo ID.");
	}
	puts("Examination complete.");
}
void foreclose_property() {
	size_t repo_id;
	printf("Enter repo ID for foreclosure: ");
	scanf("%zu", &repo_id);
	getchar();
	if (repo_id < repo_count && repos[repo_id]) {
		puts("Confirm foreclosure proceedings? (y/n)");
		printf("> ");
		char confirmation = getchar();
		if (confirmation == 'y') {
			free(repos[repo_id]);
			repos[repo_id] = NULL;
		}
	} else {
		puts("Invalid repo ID.");
	}
}
void display_menu() {
	puts("\n=== R.E.P.O. MANAGEMENT SYSTEM ===");
	puts("1. Acquire Repository");
	puts("2. Update Property Records");
	puts("3. Examine Property");
	puts("4. Foreclose Property");
	puts("==================================");
}
int main() {
	int choice;
	setbuf(stdin, 0);
	setbuf(stdout, 0);
	puts("Welcome to R.E.P.O. - Real Estate Property Operations");
	puts("Repossession and foreclosure management system active...\n");
	while (1) {
		display_menu();
		scanf("%d", &choice);
		getchar();
		switch (choice) {
			case 1:
				acquire_repo();
				break;
			case 2:
				update_records();
				break;
			case 3:
				examine_property();
				break;
			case 4:
				foreclose_property();
				break;
			default:
				break;
		}
	}
}
