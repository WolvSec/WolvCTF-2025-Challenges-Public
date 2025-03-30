#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h> 

#define MEMORYSIZE 32767 // max short
#define NUMREGS 8 // regs [0,7]

//short value;
//while (fread(&value, sizeof(short), 1, stdin) == 1) {
    // Process value here
//    printf("%hd\n", value); // or whatever you want to do with it
//}
int run();

typedef struct stateStruct {
  short pc;
  short mem[MEMORYSIZE];
  int reg[NUMREGS];
  short numMem;
} stateType;

void ignore(void)
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
}

int main(void){
  ignore();
  return run();  
}

int run(){

  stateType state;
  state.numMem = 0;
  for(int i = 0; i < NUMREGS; i++){
    state.reg[i] = 0;
  }
  state.pc = 0;
  
  short size;
  fread(&size, sizeof(short),1,stdin);

  short readVal;
  while(state.numMem < size && fread(&readVal, sizeof(short), 1, stdin) == 1){
    //read executable into memory
    state.mem[state.numMem++] = readVal;
  }
  
  int regA;
  int regB;
  int offset;
  
  while(true){
    //fetch
    short instruction = state.mem[state.pc];

    //decode 
    short opcode = (instruction >> 13) & 0b111;
    regA = (instruction >> 3) & 0b111;
    regB = (instruction) & 0b111;
    offset = (instruction >> 6) & 0b1111111;

    //execute
    switch(opcode){
      //add 
      case 0:
        state.reg[regA] = state.reg[regA] + state.reg[regB];
        break;

      //nand 
      case 1:
        state.reg[regA] = ~(state.reg[regA] & state.reg[regB]);
        break;

      //beq
      case 2:
        if(state.reg[regA] == state.reg[regB]){
          state.pc += offset-1;
        }
        break;

      //halt
      case 3:
        return 0;

      //lw
      case 4:
      case 5:
        state.reg[regA] = state.mem[state.reg[regB] + offset];
        break;

      case 6:
      case 7:
        state.mem[state.reg[regB] + offset] = state.reg[regA];
        break;
    }
    state.pc++;
  }
  return 0;
}
