%define PROT_NONE 0x00
%define PROT_READ 0x01
%define PROT_WRITE 0x02
%define PROT_EXEC 0x04

%define MAP_PRIVATE 0x02
%define MAP_ANONYMOUS 0x20

%define SIGSEGV 11
%define SA_RESTORER 0x04000000

%macro read 3
    mov rax, 0x00
    mov rdi, %1
    mov rsi, %2
    mov rdx, %3
    syscall
%endmacro

%macro write 3
    mov rax, 0x01
    mov rdi, %1
    mov rsi, %2
    mov rdx, %3
    syscall
%endmacro

%macro mmap 6
    mov rax, 0x09
    mov rdi, %1
    mov rsi, %2
    mov rdx, %3
    mov r10, %4
    mov r8, %5
    mov r9, %6
    syscall
%endmacro

%macro mprotect 3
    mov rax, 0x0a
    mov rdi, %1
    mov rsi, %2
    mov rdx, %3
    syscall
%endmacro

%macro rt_sigaction 4
    mov rax, 0x0d
    mov rdi, %1
    mov rsi, %2
    mov rdx, %3
    mov r10, %4
    syscall
%endmacro

%macro rt_sigreturn 0
    mov rax, 0x0f
    syscall
%endmacro

%macro exit 1
    mov rax, 0x3c
    mov rdi, %1
    syscall
%endmacro

%macro wait4 4
    mov rax, 0x3d
    mov rdi, %1
    mov rsi, %2
    mov rdx, %3
    mov r10, %4
    syscall
%endmacro
