%include "syscalls.asm"

%define PROT_BITS 0x572039efb49fc8cb

%macro exchange_registers 0
    xchg rax, qword [saved_rax]
    xchg rcx, qword [saved_rcx]
    xchg rdx, qword [saved_rdx]
    xchg rdi, qword [saved_rdi]
    xchg rsi, qword [saved_rsi]
    xchg r8, qword [saved_r8]
    xchg r9, qword [saved_r9]
    xchg r10, qword [saved_r10]
    xchg r11, qword [saved_r11]
    xchg r12, qword [saved_r12]
    xchg r13, qword [saved_r13]
    xchg r14, qword [saved_r14]
%endmacro

%macro save_registers 0
    exchange_registers
    push rax
    mov rax, qword [saved_flags]
    push rax
    popfq
    pop rax
%endmacro

%macro restore_registers 0
    push rax
    pushfq
    pop rax
    mov qword [saved_flags], rax
    pop rax
    exchange_registers
%endmacro

global _start

section .text
_start:
    mmap 0, 0x1000 * 33, PROT_NONE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0
    mov rbx, rax  ; rbx: mmap_base

    ; Applying protections based on PROT_BITS.
    mov r12, PROT_BITS  ; r12: prot_bits
    mov r13, rbx ; r13: mmap_page
prot_loop:
    xor r14, r14  ; r14: prot
    mov r15, r12  ; r15: prot_bit
    and r15, 0x01
    jz prot_loop_no_read
    or r14, PROT_READ
prot_loop_no_read:
    shr r12, 1
    mov r15, r12
    and r15, 0x01
    jz prot_loop_no_write
    or r14, PROT_WRITE
prot_loop_no_write:
    mprotect r13, 0x1000, r14
    add r13, 0x1000
    shr r12, 1
    jnz prot_loop

    ; mmap_base + 0x1000 * 32 is the extracted program base.
    lea r12, qword [rbx + 0x1000 * 32]
    mprotect r12, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC

    rt_sigaction SIGSEGV, action, 0, 8

    ; while True:
    ;     bits_to_extract = structure[structure_pointer]
    ;
    ;     if bits_to_extract == 0:
    ;         break
    ;
    ;     structure_pointer += 1
    ;     while bits_to_extract != 0:
    ;         call_target = structure[structure_pointer]
    ;         success = False
    ;         try:
    ;             call_target()
    ;             success = True
    ;         except:
    ;             pass
    ;
    ;         extracted_byte = extract_base[(bits_to_extract - 1) // 8]
    ;         extracted_byte <<= 1
    ;         if success:
    ;             extracted_byte += 1
    ;
    ;         extract_base[(bits_to_extract - 1) // 8] = extracted_byte
    ;
    ;         structure_pointer += 1
    ;         bits_to_extract -= 1
    ;   
    ;     extract_base()
    ;     structure_pointer += 1
    mov r12, structure_base  ; r12: structure_pointer
extract_loop_1:
    mov r13, qword [r12]  ; r13: bits_to_extract
    test r13, r13
    jz end
    add r12, 8
extract_loop_2:
    dec r13
    mov r14, qword [r12]  ; r14: call_target
    add r12, 8
    xor rax, rax  ; rax: success
    call r14
    inc rax
extract_loop_recover:
    mov r14, r13  ; r14: extract_offset
    shr r14, 3
    lea r15, qword [rbx + 0x1000 * 32]  ; r15: extract_base
    mov cl, byte [r15 + r14]  ; cl: extracted_byte
    shl rcx, 1
    add rcx, rax
    mov byte [r15 + r14], cl
    test r13, r13
    jnz extract_loop_2
    save_registers
    call r15
    restore_registers
    jmp extract_loop_1

end:
    exit 0

recover:
    ret

recover_recover:
    ; Super hacky. Overwrite sigcontext.rip.
    ; SA_NODEFER may also work but would make the stack very big.
    mov qword [rsp + 168], recover_recover_recover
    rt_sigreturn

recover_recover_recover:
    ; Clean up the stack.
    add rsp, 8
    jmp extract_loop_recover

%include "structure_code.asm"

section .bss
saved_rax: resq 1
saved_rcx: resq 1
saved_rdx: resq 1
saved_rdi: resq 1
saved_rsi: resq 1
saved_r8: resq 1
saved_r9: resq 1
saved_r10: resq 1
saved_r11: resq 1
saved_r12: resq 1
saved_r13: resq 1
saved_r14: resq 1
saved_flags: resq 1

section .rodata
action:
    dq recover  ; sa_handler
    dq SA_RESTORER  ; sa_flags
    dq recover_recover  ; sa_restorer
    times 16 dq 0  ; sa_mask

%include "structure.asm"
