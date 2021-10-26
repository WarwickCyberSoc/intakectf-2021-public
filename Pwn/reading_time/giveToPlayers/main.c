// gcc -fstack-protector-all -fPIE -Wl,-z,relro,-z,now main.c
#include <stdio.h>
 
void clear(void){
    int c;
while ((c = getchar()) != '\n' && c != EOF) { }

}


int main(int argc, char* argv[])
{


    printf("Welcome to the encoder!!\n");
    //obviously this isn't the correct flag
    char flag[]="WMG{f4ke_flag_4_testing!!}";
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