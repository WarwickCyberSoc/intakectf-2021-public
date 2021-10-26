#include <stdio.h>
#include <string.h>
#include <sys/random.h>
#include <unistd.h>

int strcmp_slow(char *str1, char *str2) {
    // A slow comparason to stop people brute-forcing.
    while (1) {
        sleep(1);

        if (*str1 != *str2) {
            return *str1 > *str2 ? 1 : -1;
        }

        if (*str1 == '\x00') {
            return 0;
        }

        str1++;
        str2++;
    }
}

int main(void) {
    // Disable buffering.
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    // Generate a random 8-digit code.
    char code[9];
    for (int i = 0; i < sizeof(code) - 1; i++) {
        do {
            getrandom(&code[i], sizeof(code[i]), 0);
        } while (code[i] < '0' || code[i] > '9');
    }
    code[sizeof(code) - 1] = '\x00';

    // Load the flag.
    char flag[64];
    FILE *file = fopen("flag.txt", "r");
    fgets(flag, sizeof(flag), file);
    flag[strcspn(flag, "\r\n")] = '\x00';
    fclose(file);

    char attempt[64];
    while (1) {
        printf("Enter the code: ");
        fgets(attempt, sizeof(attempt), stdin);
        attempt[strcspn(attempt, "\r\n")] = '\x00';

        if (strcmp_slow(code, attempt) == 0) {
            printf("Correct! Here is the flag: %s.\n", flag);
            break;
        } else {
            puts("Wrong :(");
        }
    }

    return 0;
}