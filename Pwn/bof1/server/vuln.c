// gcc vuln.c -o vuln -g -fno-stack-protector -no-pie

#include <stdio.h>
#include <stdlib.h>

void win(void) {
    system("cat flag.txt");
    return;
}

void vuln(void) {
    long check = 0x0123456789abcdef;
    char buffer[16];

    printf("Enter your name: ");
    fgets(buffer, 1024, stdin);
    printf("Hello, %s", buffer);

    if (check != 0x0123456789abcdef) {
        win();
    }

    return;
}

int main(int argc, char *argv[]) {
    // Disable buffering.
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    vuln();
    return 0;
}
