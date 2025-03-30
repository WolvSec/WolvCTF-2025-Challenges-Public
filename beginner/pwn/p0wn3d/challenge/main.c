#include <stdio.h>
#include <string.h>
#include <unistd.h>

struct __attribute__((__packed__)) data {
  char buf[32];
  int guard;
};

void ignore(void)
{
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);
}

void get_flag(void)
{
  char flag[1024] = { 0 };
  FILE *fp = fopen("flag.txt", "r");
  fgets(flag, 1023, fp);
  printf(flag);
}

int main(void) 
{
  struct data first_words;
  ignore(); /* ignore this function */

  printf("Hello little p0wn3r. Do you have any first words?\n");
  fgets(first_words.buf, 64, stdin);
  sleep(2);
	puts("Man that is so cute");
	sleep(2);
	puts("I remember last year people were screaming at the little p0wn3rs.. like AAAAAAAAAAAAAAAAAAAAAAAAAAAAA!");
	sleep(2);
	puts("Don't worry little one. I won't let them do that to you. I've set up a guard");

  if (first_words.guard == 0x42424242) {
    get_flag();
  }

  return 0;
}
