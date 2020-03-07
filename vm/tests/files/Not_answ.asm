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
@SP // Not - 258
A=M-1
D=M
@NOT0_0
D;JEQ
@NOT0_1
0;JMP
(NOT0_0)
@SP
A=M-1
M=1
@NOT0_2
0;JMP
(NOT0_1)
@SP
A=M-1
M=0
(NOT0_2)
@SP
