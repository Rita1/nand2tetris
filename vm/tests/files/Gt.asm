@256
D=A
@SP
M=D
@3
D=A
@SP
A=M
M=D
@SP
M=M+1
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
M=0
A=A-1
D=D-M
@GT0_0
D;JLT
@GT0_1
0;JMP
(GT0_0)
@SP
A=M-1
M=-1
@GT0_2
0;JMP
(GT0_1)
@SP
A=M-1
M=0
(GT0_2)
@SP
