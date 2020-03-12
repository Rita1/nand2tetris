@256 // Int
D=A
@SP // 256
M=D
@7 // Constant 7
D=A
@SP // 256
A=M
M=D
@SP
M=M+1 // 257
@4 // Constant 8
D=A
@SP // 257
A=M
M=D
@SP 
M=M+1 // 258
@SP // Neg - 258
A=M-1 // 257
D=M
@SP // 258
D=A-D
A=M-1 // 257
M=D
