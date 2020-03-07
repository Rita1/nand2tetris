@256 // Int
D=A
@SP // 256
M=D
@8 // Constant 8
D=A
@SP // 256
A=M
M=D
@SP
M=M+1 // 257
@7 // Constant 7
D=A
@SP // 257
A=M
M=D
@SP
M=M+1 // 258
@SP // Sub - 258
M=M-1 // 257
A=M
D=M
M=0
A=A-1 // 256
D=M-D
M=D
