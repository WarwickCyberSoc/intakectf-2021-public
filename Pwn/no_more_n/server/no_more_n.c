#include <stdio.h>
#include <string.h>
#include <inttypes.h>

char one[] = "w~ce\x7fxet";
char two[] = "1\"5\x0fY\x0eL\x17";
char three[] = "\x8c\xbe\x92\xe8\x81\xb5\xe9\xbd"; 

// put https://www.youtube.com/watch?v= before the middle of the flag for a secret

void nineteen_dollar_flag(uint64_t who_wants_it) {
    int i;
    char flag[17];
    
    for (i=0; i<8; i++) {
        if ( (((char*)(&who_wants_it))[i]^one[i]) != 0x11) {
            puts("no more trolls");
            return;
        }
        else {
            flag[i] = ((char*)(&who_wants_it))[i] ^ two[i];
            flag[i+8] = ((char*)(&who_wants_it))[i] ^ three[i] ^ 0xA5;
        }
    }
    flag[16] = 0;
    puts(flag);
}

void main() {

    char trolls[32];

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    //nineteen_dollar_flag(7310584018250133350);

    puts("OK, completely blind \"pwn\" challenge");
    puts("who wants it?");
    puts("yes, I'm giving it away");
    puts("remember, share share share");

    while (1) {
        puts("and trolls: ");
        fgets(trolls, sizeof(trolls), stdin);
        
        if (strchr(trolls, 'n')) {
            puts("no more 'n' allowed, you've been blocked");
            return;
        }
        
        printf(trolls);
    
    }

}







