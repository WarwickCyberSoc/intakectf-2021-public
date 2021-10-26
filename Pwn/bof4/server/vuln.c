// gcc vuln.c -o vuln -g -fno-stack-protector -no-pie

#include <stdio.h>
#include <stdlib.h>

char target[] = "cat flag.txt";
long pointer = 0;

void increment(void) {
    pointer++;
    return;
}

void shift(void) {
    pointer <<= 1;
    return;
}

__attribute__((force_align_arg_pointer))
void win(void) {
    system((char *)pointer);
    return;
}

void vuln(void) {
    char buffer[16];

    printf("Enter your name: ");
    fgets(buffer, 1024, stdin);
    printf("Hello, %s", buffer);

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
