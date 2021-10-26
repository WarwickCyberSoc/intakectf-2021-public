#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>

// gcc vuln.c -o vuln -no-pie

void vuln() 
{
	execve("/bin/sh", NULL, NULL);
}

int main(void) 
{
    // Disable buffering.
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    uint64_t writeAddress;
    uint64_t writeValue;
	printf("Whoops, I dropped this pointer: %p\n", &writeAddress);
	
    printf("Enter write address with \"0x\": ");
    scanf("%lx", &writeAddress);

    printf("Enter write value with \"0x\": ");
    scanf("%lx", &writeValue);

	*(uint64_t*)(writeAddress) = writeValue;
	
    return 0;
}
