@256
D=A
@SP // 256
M=D
@3 // Constant 3
D=A
@SP // 256
A=M
M=D
@SP
M=M+1 // 257
@4 // Constant 3
D=A
@SP // 257
A=M
M=D
@SP 
M=M+1 // 258
@SP // LT - 258
M=M-1 // 257
A=M
D=M
M=0
A=A-1
D=D-M
@LT0_0
D;JGT
@LT0_1
0;JMP
(LT0_0)
@SP
A=M-1
M=-1
@LT0_2
0;JMP
(LT0_1)
@SP
A=M-1
M=0
(LT0_2)
@SP
