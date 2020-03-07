//
@256
D=A
@SP // 256
M=D
@0 // Constant 3
D=A
@SP // 256
A=M
M=D
@SP
M=M+1 // 257
@0 // Constant 3
D=A
@SP // 257
A=M
M=D
@SP 
M=M+1 // 258
@SP // Or - 258
M=M-1 // 257
A=M
D=M
M=0
A=A-1
D=D+M
@OR0_0
D;JEQ
@OR0_1
0;JMP
(OR0_0)
@SP
A=M-1
M=0
@OR0_2
0;JMP
(OR0_1)
@SP
A=M-1
M=1
(OR0_2)
@SP
