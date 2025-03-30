#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define BUF_LEN 32
typedef void (*func_ptr)();

static char * binsh= "/bin/sh";
int run();

void ignore(void)
{
	setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
}

int main(void){
  ignore();
  return run();
}

void check_shellcode(char* buf, int len){
	unsigned char* uchar_ptr = (unsigned char*) buf;
	int err = 0;
	//check that after len everything else is a nop
	for(int i = len; i < BUF_LEN; i++){
		if(uchar_ptr[i] != (unsigned char)0x90){
			err = 1;
		}
	}
	// check odd even
	for(int i = 0; i < len-1; i++){
		if(((uchar_ptr[i] ^ uchar_ptr[i+1]) & 1) != 1){
			err = 1;
		}
	}
	// check xor constraint
	for(int i = 0; i < len-1; i++){
		if((uchar_ptr[i] ^ uchar_ptr[i+1]) > (unsigned char)0xC0){
			err = 1;
		}
	}
	for(int i = 0; i < len-2; i++){
		if((uchar_ptr[i] ^ uchar_ptr[i+2]) < (unsigned char) 0x20){
			err = 1;
		}
	}

	if(err){
		puts("You wouldn't cook on one of these... did you learn nothing from my chemistry class?");
		exit(1);
	}
	return;
}

int run(){
  char buf[BUF_LEN];
  puts("You got new lab grown shells? I don't care for that organic garbage... If you don't got shells fresh of the condenser get outta my shop!");
  puts("What, Still here? Hand it over, that thing, your synthetic shell");
  
	memset(buf, 0x90, BUF_LEN);
	fgets(buf, BUF_LEN, stdin);

	int len = 0;
	for(int i = 0; i < BUF_LEN; i++){
		if(buf[i] == '\n'){
			buf[i] = 0x90;
			buf[i+1] = 0x90;
			len = i;
		}
	}


  check_shellcode(buf,len);
	
	buf[BUF_LEN-2] = 0x0f;
	buf[BUF_LEN-1] = 0x05;
	asm volatile(
    "xor %esi, %esi\n\t"  /* Set ESI to 0 */
    "xor %edx, %edx"      /* Set EDX to 0 */
	);
	goto *((func_ptr)&buf);
	
  return 0;
}


