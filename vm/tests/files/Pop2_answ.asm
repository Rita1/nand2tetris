@256
D=A
@SP
M=D
@10
D=A
@SP
A=M
M=D
@SP
M=M+1
@0 // Pop args 0
D=A
@ARG
D=M+D
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
@20 // push constant 20
D=A
@SP
A=M
M=D
@SP
M=M+1
@1 // POP args 1
D=A
@ARG
D=M+D
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
@1 // PUSH args 1
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
