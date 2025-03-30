#include <stdio.h>
#include <string.h>
#include <unistd.h>

struct __attribute__((__packed__)) data {
  char buf[32];
  int guard1;
	int guard2;
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
  struct data second_words;
  ignore(); /* ignore this function */

  printf("I can't believe you just did that. Do you have anything to say for yourself?\n");
  fgets(second_words.buf, 64, stdin);
  sleep(2);
	puts("Yeah Yeah whatever");
	sleep(2);
	puts("I've got two guards now, what are you gonna do about it?");
	sleep(2);

  if (second_words.guard1 == 0xdeadbeef && second_words.guard2 == 0x0badc0de) {
    get_flag();
  }

  return 0;
}
