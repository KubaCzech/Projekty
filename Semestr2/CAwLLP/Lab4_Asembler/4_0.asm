bits    64
default rel

global  main

extern  printf
extern  scanf

section .data
    out_format  db  'sqrt(%.3lf) = %lf', 10,0
    scan_format db  '%lf',0

    step        dq  0.125
    zero        dq  0.0
section .bss
    value       resq 1
section .text
    main:
        mov rax,0;end value
        lea rdi,[scan_format]
        lea rsi, [value]
        sub rsp,8 ;get int
        mov al,0
        call scanf wrt ..plt
        add rsp,8

        movlpd xmm14,[zero]
    
        loop:
            movlpd  xmm15, [value]
            cmpltsd xmm15,xmm14
            movq    rax,xmm15
            cmp     rax,0
            jne      exit

            movsd  xmm0,xmm14
            sqrtsd  xmm1,xmm14


            sub rsp, 8;print element
            lea rdi, [out_format]
            mov al, 2
            call printf wrt ..plt
            add rsp,8
            mov rax, 0


            movlpd  xmm1,[step]
            addsd   xmm14,xmm1
            jmp loop

        
        exit:
            mov rax,60
            mov rdi,0
            syscall