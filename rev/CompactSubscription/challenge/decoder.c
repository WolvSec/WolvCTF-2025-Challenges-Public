#include <stdio.h>
#include <string.h>

typedef unsigned int uint;
#define CHANNEL_0_CHECKSUM 0x12ac0256
#define CHANNEL_1_CHECKSUM 0x59a9d62b
#define CHANNEL_2_CHECKSUM 0x410ff20b
#define CHANNEL_3_CHECKSUM 0x2a318621

unsigned char active_subscription[16];

unsigned char hex_to_nibble(char h){
    if(h >= '0' && h <= '9'){
        return h-'0';
    }
    else if(h >= 'a' && h <= 'f'){
        return h - 'a' + 10;
    }
    else if(h>='A' && h <= 'F'){
        return h - 'A' + 10;
    }
    return 0xff;
}

void hex_to_bytes(char* hex, unsigned char * bytes){
    while(*hex != '\0'){
        
        unsigned char value = hex_to_nibble(*hex++) * 0x10;
        value += hex_to_nibble(*hex++);
        if(value == 0xff){
            return;
        }
        *bytes++ = value;
    }
}

uint check_result(uint val, uint compare){
    printf("bytes: %08x\n", val);
    uint result = 0;
    
    for (int i = 0; i < 4; i++) {
        uint group = (val >> (i * 8)) & 0xFF;
        uint transformed = 0;
        for (int j = 0; j < 8; j++) {
            transformed |= ((group >> j) & 1) << ((j + 2) % 8);
        }

        
        // Place transformed group back
        result |= (transformed << (i * 8));
    }
    printf("result: %08x\n", result);
    
    return result == compare;   
}
int subscribe(){
    char subscription[36];
    printf("Subscription?\n");
    fgets(subscription, sizeof(subscription), stdin);
    unsigned char decoded_subscription[17];
    hex_to_bytes(subscription, decoded_subscription);
    unsigned char channel = decoded_subscription[0];
    memcpy(active_subscription, decoded_subscription + 1, 16);
    unsigned char bytes[4];
    for(int i = 0; i < 4; i++){
        bytes[i] = decoded_subscription[1+i * 4 + channel];
    }
    
    switch(channel){
        case 0:{
            return check_result(*(uint*)(bytes), CHANNEL_0_CHECKSUM);
        }
        case 1:{
            return check_result(*(uint*)(bytes), CHANNEL_1_CHECKSUM);
        }
        case 2:{
            return check_result(*(uint*)(bytes), CHANNEL_2_CHECKSUM);
        }
        case 3:{
            return check_result(*(uint*)(bytes), CHANNEL_3_CHECKSUM);
        }
        default:{
            return 0;
        }
    }
    return 1;
}


void decode(){
    char message[12];
    printf("Message?\n");
    fgets(message, sizeof(message), stdin);
    unsigned char decoded_message[5];
    hex_to_bytes(message, decoded_message);
    unsigned char channel = decoded_message[0];

    char result[5];
    for(int i = 0; i < 4; i++){
        result[i] = active_subscription[i * 4 + channel] ^ decoded_message[1 + i];
    }
    result[4] = '\0';
    
    printf("message: %s\n", result);
}


int main(){

    while(1){
        printf("Do what?\n1. Subscribe\n2. Decode\n");
        char option[3];
        fgets(option, sizeof(option), stdin);
        if(option[0] == '1'){
            if(subscribe()){
                printf("subscription complete\n");
            }
            else{
                printf("subscription failed\n");
            }
        }
        else if(option[0] == '2'){
            decode();
        }
        else{
            printf("That's not an option.\n");
        }
    }
    
    
}