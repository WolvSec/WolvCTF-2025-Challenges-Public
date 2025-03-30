#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void mix_flag(char *flag, char *mixed_flag, int length) {
    for (int i = 0; i < length; i++) {
        mixed_flag[i] = flag[i] - 3;
    }

    for (int i = 0; i < length - 1; i += 2) {
				int next = length - 1 - (i+1); 
        char temp = mixed_flag[i];
        mixed_flag[i] = mixed_flag[next];
        mixed_flag[next] = temp;
    }
}

int main() {
    FILE *file = fopen("flag.txt", "r");
    if (file == NULL) {
        perror("Failed to open flag.txt");
        return 1;
    }

    char flag[100];
    fgets(flag, 100, file);
    fclose(file);

    flag[strcspn(flag, "\n")] = '\0';

    int length = strlen(flag);
    char mixed_flag[100];

    mix_flag(flag, mixed_flag, length);
    mixed_flag[length] = '\0'; 

    // Print the mixed flag
    printf("Mixed Flag: %s\n", mixed_flag);

    return 0;
}
