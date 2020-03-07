//
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
@SP // Eq - 258
M=M-1 // 257
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
@4 // Constant 3
D=A
@SP // 256
A=M
M=D
@SP
M=M+1 // 257
@4 // Constant 3
D=A
@SP
A=M
M=D
@SP 
M=M+1 // 258
@SP // Eq - 258
M=M-1 // 257
A=M
D=M
M=0
A=A-1
D=D-M
@EQ1_0
D;JEQ
@EQ1_1
0;JMP
(EQ1_0)
@SP
A=M-1
M=0
@EQ1_2
0;JMP
(EQ1_1)
@SP
A=M-1
M=-1
(EQ1_2)
@SP
