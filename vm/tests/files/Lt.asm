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
@M=M+1
@4
D=A
@SP
A=M
M=D
@SP
@M=M+1
@SP
M=M-1
A=M
D=M
M=0
A=A-1
D=D-M
@EQ0_0
D;JEQ
@EQ0_1
0;JMP
(EQ0_0)
@SP
A=M-1
M=0
@EQ0_2
0;JMP
(EQ0_1)
@SP
A=M-1
M=-1
(EQ0_2)
@SP
