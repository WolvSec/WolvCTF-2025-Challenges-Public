#include <stdio.h>
#include <stdlib.h>

int main() {
    FILE *file = fopen("./flag.txt", "r");
    if (file == NULL) {
        perror("Error opening file");
        return 1;
    }

    char ch;
    while ((ch = fgetc(file)) != EOF) {
        putchar(ch);
    }

    fclose(file);
    return 0;
}
