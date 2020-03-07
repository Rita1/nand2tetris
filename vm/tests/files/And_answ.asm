//
@256
D=A
@SP // 256
M=D
@1 // Constant 3
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
@SP // And - 258
M=M-1 // 257
A=M
D=M
M=0
A=A-1
D=D+M
@2
D=D-A
@AND0_0
D;JEQ
@AND0_1
0;JMP
(AND0_0)
@SP
A=M-1
M=1
@AND0_2
0;JMP
(AND0_1)
@SP
A=M-1
M=0
(AND0_2)
@SP
