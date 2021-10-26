    mov qword [rbx + 0x1000 * 32 + 0x800], 0x65746e45  ; "Ente"

    mov qword [rbx + 0x1000 * 32 + 0x804], 0x6c662072  ; r fl"

    mov qword [rbx + 0x1000 * 32 + 0x808], 0x203a6761  ; "ag: "

    mov rax, 0x01  ; write

    mov rdi, 1  ; STDOUT

    lea rsi, qword [rbx + 0x1000 * 32 + 0x800]  ; "Enter flag: "

    mov rdx, 12  ; len("Enter flag: ")

    syscall  ; write(STDOUT, "Enter flag: ", len("Enter flag: "))

    mov rax, 0x00  ; read

    mov rdi, 0  ; STDIN

    lea rsi, qword [rbx + 0x1000 * 32 + 0x800]  ; flag

    mov rdx, 32  ; len(flag)

    syscall  ; read

    movaps xmm0, oword [rbx + 0x1000 * 32 + 0x800]  ; flag_1

    movaps xmm1, oword [rbx + 0x1000 * 32 + 0x810]  ; flag_2

    mov qword [rbx + 0x1000 * 32 + 0x800], flag_1_xor_1

    mov qword [rbx + 0x1000 * 32 + 0x804], flag_1_xor_2

    mov qword [rbx + 0x1000 * 32 + 0x808], flag_1_xor_3

    mov qword [rbx + 0x1000 * 32 + 0x80c], flag_1_xor_4

    mov qword [rbx + 0x1000 * 32 + 0x810], flag_2_xor_1

    mov qword [rbx + 0x1000 * 32 + 0x814], flag_2_xor_2

    mov qword [rbx + 0x1000 * 32 + 0x818], flag_2_xor_3

    mov qword [rbx + 0x1000 * 32 + 0x81c], flag_2_xor_4

    pxor xmm0, oword [rbx + 0x1000 * 32 + 0x800]

    pxor xmm1, oword [rbx + 0x1000 * 32 + 0x810]

    mov qword [rbx + 0x1000 * 32 + 0x800], flag_1_shuffle_1

    mov qword [rbx + 0x1000 * 32 + 0x804], flag_1_shuffle_2

    mov qword [rbx + 0x1000 * 32 + 0x808], flag_1_shuffle_3

    mov qword [rbx + 0x1000 * 32 + 0x80c], flag_1_shuffle_4

    mov qword [rbx + 0x1000 * 32 + 0x810], flag_2_shuffle_1

    mov qword [rbx + 0x1000 * 32 + 0x814], flag_2_shuffle_2

    mov qword [rbx + 0x1000 * 32 + 0x818], flag_2_shuffle_3

    mov qword [rbx + 0x1000 * 32 + 0x81c], flag_2_shuffle_4

    pshufb xmm0, oword [rbx + 0x1000 * 32 + 0x800]

    pshufb xmm1, oword [rbx + 0x1000 * 32 + 0x810]

    mov qword [rbx + 0x1000 * 32 + 0x800], flag_1_compare_1

    mov qword [rbx + 0x1000 * 32 + 0x804], flag_1_compare_2

    mov qword [rbx + 0x1000 * 32 + 0x808], flag_1_compare_3

    mov qword [rbx + 0x1000 * 32 + 0x80c], flag_1_compare_4

    mov qword [rbx + 0x1000 * 32 + 0x810], flag_2_compare_1

    mov qword [rbx + 0x1000 * 32 + 0x814], flag_2_compare_2

    mov qword [rbx + 0x1000 * 32 + 0x818], flag_2_compare_3

    mov qword [rbx + 0x1000 * 32 + 0x81c], flag_2_compare_4

    pxor xmm0, oword [rbx + 0x1000 * 32 + 0x800]

    pxor xmm1, oword [rbx + 0x1000 * 32 + 0x810]

    xor rax, rax

    ptest xmm0, xmm0

    jz flag_1_valid
    or r12, 1
flag_1_valid:

    ptest xmm1, xmm1

    jz flag_2_valid
    or r12, 1
flag_2_valid:

    mov qword [rbx + 0x1000 * 32 + 0x800], 0x72726f43  ; "Corr"

    mov qword [rbx + 0x1000 * 32 + 0x804], 0x21746365  ; "ect!"

    mov qword [rbx + 0x1000 * 32 + 0x808], 0x6e6f7257  ; "Wron"

    mov qword [rbx + 0x1000 * 32 + 0x80c], 0x283a2067  ; "g :("

    mov rax, 0x01  ; write

    mov rdi, 1  ; STDOUT

    lea rsi, qword [rbx + 0x1000 * 32 + 0x800 + r12 * 8]  ; status

    mov rdx, 8  ; len(status)

    syscall  ; write(STDOUT, status, len(status))

    mov qword [rbx + 0x1000 * 32 + 0x800], 0x0a  ; "\n"

    mov rax, 0x01  ; write

    mov rdi, 1  ; STDOUT

    lea rsi, qword [rbx + 0x1000 * 32 + 0x800]  ; "\n"

    mov rdx, 1  ; len("\n")

    syscall  ; write(STDOUT, "\n", len("\n"))
