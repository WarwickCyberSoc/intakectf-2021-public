// gcc -fstack-protector-all -fPIE -Wl,-z,relro,-z,now main.c
#include <stdio.h>
 
void clear(void){
    int c;
while ((c = getchar()) != '\n' && c != EOF) { }

}


int main(int argc, char* argv[])
{
    // Disable buffering - some socat issue - oshawk <3
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    printf("Welcome to the encoder!!\n");
    char flag[]="WMG{ju5t_r34d_Th3_fl@g!!!}";
    // char flag[]="WMG{f4ke_flag_4_testing!!}";
    char rot13[]="nopqrstuvwxyzabcdefghijklm";

	int index = 0;
    int characterRead=0;

	while (1) {

        printf("Enter a character and I'll tell you the encoded character: ");
		scanf("%c", &index);
        characterRead=index-97;
     
		printf("Okay, here you go: %c\n",rot13[characterRead]);
        clear();
	}
	return 0;
}