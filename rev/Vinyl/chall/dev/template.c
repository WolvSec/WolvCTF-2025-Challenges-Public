#include "stdio.h"
#include "stdlib.h"
#include "string.h"

#define SIZE 96
const int START[] = START_POS;
const int CHECKPOINTS[7][3] = {
    CHECKPOINT_DATA
};
const int END[] = END_POS;

struct State{
    int current_side;
    int x;
    int y;
    char sides[2][SIZE][SIZE];
};

struct State state = {
    .current_side = 0,
    .x = 48,
    .y = 48,
    .sides = 
    {
        {
           SIDE_A_DATA
        },
        {
            SIDE_B_DATA
        }
    }
};


void check_checkpoint(int i){
    int index = (i/4) - 1;
    int err = 0;
    if(state.current_side != CHECKPOINTS[index][0]){
        err = 1;
    }
    if(state.x != CHECKPOINTS[index][1]){
        err = 1;
    }
    if(state.y != CHECKPOINTS[index][2]){
        err = 1;
    }

    if(err){
        puts("You're no DJ... get outta here >:(");
        exit(1);
    }
}

void rotate_cw(char matrix[SIZE][SIZE]){
    // Perform Transpose
    for (int i = 0; i < SIZE; i++) {
        for (int j = i + 1; j < SIZE; j++) {
            int temp = matrix[i][j];
            matrix[i][j] = matrix[j][i];
            matrix[j][i] = temp;
        }
    }

    // Reverse each row
    for (int i = 0; i < SIZE; i++) {
        int start = 0, end = SIZE - 1;
        while (start < end) {
            int temp = matrix[i][start];
            matrix[i][start] = matrix[i][end];
            matrix[i][end] = temp;
            start++;
            end--;
        }
    }
}

void rotate_ccw(char matrix[SIZE][SIZE]){
    // Reverse each row
    for (int i = 0; i < SIZE; i++) {
        int start = 0, end = SIZE - 1;
        while (start < end) {
            int temp = matrix[i][start];
            matrix[i][start] = matrix[i][end];
            matrix[i][end] = temp;
            start++;
            end--;
        }
    }

    // Perform Transpose
    for (int i = 0; i < SIZE; i++) {
        for (int j = i + 1; j < SIZE; j++) {
            int temp = matrix[i][j];
            matrix[i][j] = matrix[j][i];
            matrix[j][i] = temp;
        }
    }
}

void flip_matrix(char matrix[SIZE][SIZE]) {
    for (char i = 0; i < SIZE / 2; i++) {
        for (char j = 0; j < SIZE; j++) {
            char temp = matrix[i][j];
            matrix[i][j] = matrix[SIZE - i - 1][j];
            matrix[SIZE - i - 1][j] = temp;
        }
    }
}

void rotate_right(){
    //active side rotates cw
    rotate_cw(state.sides[state.current_side]);
    //backside rotates ccw
    rotate_ccw(state.sides[1-state.current_side]);
    //apply rotation matrix
    int tmpx = state.x;
    int tmpy = state.y;
    state.x = tmpy;
    state.y = 95-tmpx;
}

void rotate_left(){
    // active side rotates ccw
    rotate_ccw(state.sides[state.current_side]);
    // backside rotates cw
    rotate_cw(state.sides[1-state.current_side]);
    //apply rotation matrix
    int tmpx = state.x;
    int tmpy = state.y;
    state.x = 95-tmpy;
    state.y = tmpx;
}

void horizontal_flip(){
    //flip horizontal posiiton
    state.y = SIZE - 1 - state.y;
    //toggle active side
    state.current_side = 1 - state.current_side;

    //check for walls
    if(state.sides[state.current_side][state.x][state.y] == '#'){
        puts("You tryna glitch through walls or sum?");
        exit(1);
    }
}

void vertical_flip(){
    //flip vertical
    int tmpx = state.x;
    int tmpy = state.y;
    state.x = SIZE - 1 - tmpx;
    state.y = tmpy;
    //toggle active side
    state.current_side = 1 - state.current_side;
    //sides flip vertically
    flip_matrix(state.sides[state.current_side]);
    flip_matrix(state.sides[1 - state.current_side]);

    //check for walls
    if(state.sides[state.current_side][state.x][state.y] == '#'){
        puts("You tryna glitch through walls or sum?");
        exit(1);
    }
}

void do_command(char move){
    switch(move){
        case 0b00:
            //Rotate Right
            printf("RR ");
            rotate_right();
            break;
        case 0b11:
            //Rotate Left
            printf("RL ");
            rotate_left();
            break;
        case 0b10:
            //Vertical Flip
            printf("VF ");
            vertical_flip();
            break;
        case 0b01:
            //Horizontal Flip
            printf("HF ");
            horizontal_flip();
            break;
    }
}

void print_maze(){
    if(state.current_side == 0){
        printf("\nSIDE A\n");
        for(int i = 0; i < SIZE; i++){
            for(int j = 0; j < SIZE; j++){
                printf("%c",state.sides[0][i][j]);
            }
            printf("\n");
        }
        return;
    }


    printf("\nSIDE B\n");
    for(int i = 0; i < SIZE; i++){
        for(int j = 0; j < SIZE; j++){
            printf("%c",state.sides[1][i][j]);
        }
        printf("\n");
    }
}

void simulate(char* buf){
    print_maze();
    printf("Side = %d, pos = %d, %d\n",state.current_side,state.x,state.y);
    for(int i = 0; i < 32; i++){ //for every char
        if(i > 0 && i % 4 == 0){ //every 16 moves check checkpoint
            check_checkpoint(i);
        }
        char c = buf[i];
        for(int j = 0; j < 4; j++){ //for every command
            //grab move bits from char
            char move = (c >> 2*(3-j) ) & 0b11;

            //update orientation and position
            do_command(move);

            //tick gravity until you hit a wall
            state.sides[state.current_side][state.x][state.y] = 'X';
            while(1){
                int nextx = state.x + 1;
                if(state.sides[state.current_side][nextx][state.y] == '#'){
                    break;
                }
                state.x++;
                state.sides[state.current_side][state.x][state.y] = 'X';
            }
            int moven = i*4+j;
            printf("Move = %d,Side = %d, pos = %d, %d\n",moven,state.current_side,state.x,state.y);
            print_maze();
        }
    } //for every char

    //check ending position
    int err = 0;
    if(state.current_side != END[0]){
        err = 1;
    }
    if(state.x != END[1]){
        err = 1;
    }
    if(state.y != END[2]){
        err = 1;
    }
    if(err){
        puts("You're no DJ... You were close tho...");
        exit(1);
    }
}

int main(){
    char buf[40];
    fgets(buf, 33, stdin);
    buf[32] = '\0';
    if(strlen(buf) != 32){
        puts("You haven't even looked at the binary have you...");
        exit(1);
    }
    simulate(buf);
    puts("That's a sick mix you just played! You win!");
    return 0;
}