#include <stdio.h>
#include <string.h>
#include <unistd.h>

char * flag = "wctf{n0_w4y_y0u_f0unD_1t!}\0";

int main(void){
	char buf[1024] = {0};

	puts("Are you enjoying the CTF?");
	scanf("%s",buf);
	sleep(1);
	if(strcmp(buf,"yes") == 0){
		puts(":D");
	}
	else if(strcmp(buf,"no") == 0){
		puts(":(");
	}
	else{
		puts(":|");
	}

	for(int i = 0; i < 5; i++){
		puts(".");
		sleep(1);
	}
	puts("\nOh yeah the flag!");
	sleep(1);
	puts("Ha! You thought I was just gonna hand it over?");
	return 0;
}
