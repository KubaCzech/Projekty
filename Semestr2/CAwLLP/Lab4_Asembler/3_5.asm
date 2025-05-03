bits    64
default rel

global  main

extern  printf
extern  scanf

section .data
    out_format  db  '%d', 9,0
    nl          db  ' ',10,0;new line
    scan_format db  '%d',0
section .bss
    intarray    resd 100
    n           resd 1

section .text
    main:  
        mov r15,0
        lea rbx,[intarray]
        loop:
            
            cmp r15,100
            je end_of_input
            
            add r15,1
            mov rsi,rbx
            lea rdi,[scan_format]
            sub rsp,8 ;get int
            mov rax,0
            mov al,0
            call scanf wrt ..plt
            add rsp,8
            add rbx,4
            cmp rax,0;if scan worked, loop again else continue
            jne loop

        end_of_input:
        mov [n],r15;number of elements goes to n

        ;START OF SORTING
        mov rcx,0;outer loop counter
        mov rax,[n]
        dec rax
        outerloop:
            cmp rcx,rax
            jge displaying
            inc rcx
            lea rbx,[intarray]
            mov r15,1;inner loop counter
            innerloop:
                cmp r15,rax
                jge outerloop
                add r15,1
                add rbx,4
                mov r8d,[rbx-4]
                mov r9d,[rbx]
                cmp r9d,r8d
                jge innerloop
                mov [rbx-4],r9d
                mov [rbx],r8d
                jmp innerloop
        ;END OF SORTING

        displaying:
        lea rbx,[intarray]
        mov r15,[n];printloop counter
        dec r15
        printloop:;print elements (tab between)
            
            sub rsp, 8;print element
            mov rsi,[rbx]
            lea rdi, [out_format]
            mov al, 0
            call printf wrt ..plt
            add rsp,8
            mov rax, 0

            add rbx,4; go to next element in an array
            dec r15
            cmp r15,0
            jle newline
            jmp printloop
        
        newline:;print a new line
            sub rsp, 8
            lea rdi,[nl]
            mov al, 0
            call printf wrt ..plt
            add rsp,8
            mov rax, 0

        exit:
            mov rax,60
            mov rdi,0
            syscall