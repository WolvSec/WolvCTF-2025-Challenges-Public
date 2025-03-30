#include <errno.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h> // For sleep function

int balance = 1337;
uint8_t random_val = 0;
uint8_t events = 0;
int day_rate = 10;

uint8_t tps_mask = 2+8;
uint8_t meet_mask = 2+4+16;
uint8_t jam_mask = 8+16;
uint8_t sat_mask = 8+32;
uint8_t fire_mask =  128+32+8;
uint8_t stapler_mask = 32+64;
uint8_t quit_mask = 1;


void work() {
	if (events & tps_mask) {
		printf("You forget to put the cover sheet on your TPS report\n");
	}
	if (events & meet_mask) {
		printf("You have a meeting with a consultant\n");
	}
	if (events & jam_mask) {
		printf("The printer jams\n");
	}
	if (events & sat_mask) {
		printf("Your boss tells you that you have to come in on Saturday\n");
	}
	if (events & fire_mask) {
		printf("The fire alarm goes off\n");
	}
	if (events & stapler_mask) {
		printf("Your cowworker asks if you have seen his stapler\n");
	}
	if (events & quit_mask) {
		printf("You think about quitting\n");
	}
	printf("Time to clock out. You made $%d today\n", day_rate);
	balance += day_rate;
	events = events ^ (balance & 0xff);
}

void print_menu() {
	printf("Balance: $%d\n", balance);
	printf("1) Clock in\n");
	printf("2) Ask for raise\n");
	printf("3) Quit job\n");
	printf("> ");
	fflush(stdout);
}

void raise() {
	char val_buf[10];
	long val;

	printf("How much do you want to make per day?\n");
	printf("> ");
	fflush(stdout);
	fgets(val_buf, 10, stdin);
	errno = 0;
	val = strtol(val_buf, NULL, 10);
	if (errno || val < day_rate) {
		printf("Huh?\n");
		return;
	}
	printf("Mmm yeah, ok\n");
	day_rate = val;
}

void quit() {
	char flag_buf[48];
	FILE *flag_file;
	if (balance == (random_val | (random_val << 8))) {
		flag_file = fopen("./flag.txt", "r");
		if (!flag_file) {
			printf("Cannot open ./flag.txt");
			exit(1);
		}
		fread(&flag_buf, 32, 1, flag_file);
		flag_buf[32] = 0;
		printf("You were actually nice to have around\n");
		printf("Here, take this parting gift:\n");
		printf("%s\n", flag_buf);
		exit(0);
	}
	printf("Good riddance\n");
	exit(0);
}

void get_ready(){
	puts("You're getting ready for work");
	for (int i = 1; i <= 10; i++) {
		printf("%d\n", i);
    sleep(1); // Sleep for 1 second
  	fflush(stdout); // Ensure output is displayed immediately
  }
}

int main() {
	int choice;
	char choice_buf[3];
	FILE *random_file;
	
	get_ready();

	random_file = fopen("/dev/urandom", "r");
	if (!random_file) {
		printf("Cannot open /dev/urandom\n");
		exit(1);
	}
	fread(&random_val, 1, 1, random_file);
	fclose(random_file);
	events = random_val;

	while (1) {
		print_menu();
		fgets(choice_buf, 3, stdin);
		errno = 0;
		choice = strtol(choice_buf, NULL, 10);
		if (errno) {
			continue;
		}
		switch (choice) {
			case 1:
				work();
				break;
			case 2:
				raise();
				break;
			case 3:
				quit();
				break;
			default:
				printf("choice: %d\n", choice);
				break;
		}
		if (balance < 1) {
			printf("You can't even spend money and yet you lost it all. You're fired.\n");
			exit(0);
		}
	}
		
	return 0;
}
