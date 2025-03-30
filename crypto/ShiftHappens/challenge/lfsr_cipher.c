#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

int FEEDBACK = 0b1011010000000000; //do not show in distribution
int L = 16;

uint16_t next(uint16_t current_state){
    uint16_t bit = 0;
    for(int i = 0; i < L; i++){
        bit = bit ^ ( ((current_state >> i) & 1) & ((FEEDBACK >> i) & 1 ) );
    }
    uint16_t new_state = (current_state << 1) | (bit);
    return new_state;
}

void print_bin(uint16_t state){
    for(int i = 0; i < L; i++){
        if(state & (1 << i)){
            printf("1");
        }
        else{
            printf("0");
        }
    }
    printf("\n");
}

int main(int argc, char** argv){
    FILE* fp = fopen("./flag.txt","r");
    if(fp == NULL){
        exit(1);
    }
    char flag[61];
    fscanf(fp, "%s", flag);
    fclose(fp);

    uint16_t state = 1452346534 & 0xFFFF; //do not show in distribution

    int bitstream[60*8];
    for(int i = 0; i < 60*8; i++){
        int bit = (state >> 15) & 1;
        bitstream[i] = bit;
        // printf("Bitstream at %d is %d \n",i,bitstream[i]);
        // printf("State %d: 0x%02X\n", i, state);
        // print_bin(state);
        state = next(state);
    }

    printf("\nCiphertext: \n");
    for(int i = 0; i < 60; i++){
        //for every character
        for(int j = 0; j < 8; j++){
            int to_print = (flag[i] >> (7-j)) & 1;
            to_print = to_print ^ bitstream[i*8 + j];
            printf("%d",to_print);
        }
        printf("\n");
    }

    

    return 0;
}