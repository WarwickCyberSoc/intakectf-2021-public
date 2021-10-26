// gcc vuln.c -o vuln -g -fno-stack-protector -no-pie

#include <stdio.h>
#include <stdlib.h>

char target[] = "cat flag.txt";

void vuln(void) {
    char *hint = target;
    char buffer[16];

    printf("Enter your name: ");
    fgets(buffer, 1024, stdin);
    printf("Hello, %s", buffer);

    printf("You might want to find a way of running \"%s\".\n", hint);

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
