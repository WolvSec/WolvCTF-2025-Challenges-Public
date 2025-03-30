#include <stdio.h>
#include <string.h>
#include <unistd.h>



void ignore(void)
{
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);
}

void get_flag(void)
{
	 char *args[] = {"/bin/cat", "flag.txt", NULL};
   execve(args[0], args, NULL);
}

int main(void) 
{
	char buf[32];
  ignore(); /* ignore this function */

  printf("Now this is an original challenge. I don't think I've ever seen something like this before\n");
  sleep(2);
	gets(buf);
	puts("Drumroll please!");
	sleep(2);

  return 0;
}
