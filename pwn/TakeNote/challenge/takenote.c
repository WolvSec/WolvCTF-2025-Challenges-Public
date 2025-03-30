#import <stdlib.h>
#import <stdio.h>

#define NOTE_SIZE 16

void banner(){
    puts(
"*----------------------*\n"
"|  ___            ___  |\n" 
"|   |   /\\  |__/ |__   |\n"
"|   |  /~~\\ |  \\ |___  |\n"
"|                      |\n"
"|        __  ___  ___  |\n"
"|  |\\ | /  \\  |  |__   |\n"
"|  | \\| \\__/  |  |___  |\n"
"|                      |\n"
"*----------------------*\n"

    );

}

void menu(){
    puts("What do you want to do?\n");
    puts("1. Write a Note\n");
    puts("2. Read a Note\n");
    puts("3. Exit\n");
}

int run(){
    banner();
    puts("\nWelcome to my special note taking software!\n");
    puts("Here you will be able to take all the notes you want!\n");
    puts("How many notes do you need to write?\n");
    char N[3];
    fgets(N,3,stdin);
    int n_notes = atoi(N);

    char * notes = malloc((n_notes+1)*NOTE_SIZE);
    int * valid = malloc(n_notes);
    for(int i = 0; i < n_notes; i++){
        valid[i] = 0;
    }

    while(1){
        menu();
        int choice;
        scanf("%d",&choice);
        getchar();

        switch(choice){
            int note_index;

            case 1:
                printf("Which note do you want to write to? [0 - %d]\n", n_notes-1);
                scanf("%d",&note_index);
                getchar();
                if(note_index < 0 || note_index >= n_notes){
                    puts("Nice try buddy *-*\n");
                    exit(1);
                }
                char input [2*NOTE_SIZE+1];
                fgets(input, sizeof(input), stdin);
                strncpy(notes + note_index*NOTE_SIZE, input, NOTE_SIZE+1);
                valid[note_index] = 1;
                break;

                
            case 2:
                puts("Which note do you want to print?\n");
                scanf("%d",&note_index);
                getchar();
                if(note_index < 0 || note_index >= n_notes){
                    puts("Nice try buddy *-*\n");
                    exit(1);
                }
                if(!valid[note_index]){
                    puts("You haven't written that note yet >:(\n");
                    exit(1);
                }
                puts("Your note reads:\n");
                printf(notes+note_index*NOTE_SIZE);
                break;
            
            case 3:
                puts("Thank you for taking notes with us!\n");
                exit(0);

            default:
                puts("Uhm, that's not an option. You might want to look at this: https://www.youtube.com/watch?v=uHgt8giw1LY\n");
                exit(0);
        }
    }

    free(notes);
    free(valid);
    return 0;
}

int main(){
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    return run();
}
