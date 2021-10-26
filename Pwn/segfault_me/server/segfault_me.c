#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// gcc segfault_me.c -o segfault_me -fno-stack-protector

void segfault_sigaction(int signal, siginfo_t *si, void *arg)
{
    printf("Segmentation fault\n\n");
    printf("Nice job! You've segfaulted this binary, meaning you've likely overrun the allocated buffer and redirected the code flow to an invalid instruction.\n");
    printf("Time to start learning binary exploitation! WMG{SeGFauLtS?!_Uh_0H_Tim3_T0_DeBuG!}\n");
    exit(0);
}

int main(void)
{
    // Disable buffering.
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    int *foo = NULL;
    struct sigaction sa;

    memset(&sa, 0, sizeof(struct sigaction));
    sigemptyset(&sa.sa_mask);
    sa.sa_sigaction = segfault_sigaction;
    sa.sa_flags   = SA_SIGINFO;

    sigaction(SIGSEGV, &sa, NULL);

    printf("What's your name, good fellow?\n");
    char name[30];

    gets(&name);

    printf("Nice to meet you %s\n", name);

    return 0;
}