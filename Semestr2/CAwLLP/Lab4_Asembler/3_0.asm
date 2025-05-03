bits    64
default rel

global  main

extern  printf
extern  scanf

section .data
    out_format  db  'your copied string is %s', 10,0
    out_format2  db  'your original string was %s', 10,0
    in_format   db  'please input your string',10,0
    scan_format db  '%s',0
section .bss
    instring    resb 4096
    outstring   resb 4096
section .text
    main:  
        sub rsp,8; call printf and print message
        lea rdi, [in_format]
        mov al,0
        call printf wrt ..plt
        add rsp,8
        mov rax,0

        sub rsp,8 ;string to copy
        lea rdi,[scan_format]
        lea rsi,[instring]
        mov al,0
        call scanf wrt ..plt
        add rsp,8
        mov rax,0
        
        mov ecx,0 ;count the num of chars copied
        lea rdi,[outstring] ;destination string
        lea rsi,[instring]
        
        loop:
            mov rax,[rsi]
            cmp rax,0
            je  print_new_string 
            movsq   ;8 characters from address in rsi are moved to rdi
            add ecx,1
            cmp ecx, 512    ;we have 4096 chars in buffer and we can only move 8 at once (4096/8 = 512 operations to do)
            jl  loop

        print_new_string: ;content of memory we copied to
            mov rax,0
            sub rsp,8
            lea rdi,[out_format]
            lea rsi,[outstring]
            call printf wrt ..plt
            add rsp,8

        print_old_string: ;content of memory we copied from
            mov rax,0
            sub rsp,8
            lea rdi,[out_format2]
            lea rsi,[instring]
            call printf wrt ..plt
            add rsp,8

        exit:
            mov rax,60
            mov rdi,0
            syscall