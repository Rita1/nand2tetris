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
@8 // Constant 8
D=A
@SP // 257
A=M
M=D
@SP 
M=M+1 // 258
@SP // Add - 258
M=M-1 // 257
A=M
D=M
M=0
A=A-1 // 256
D=D+M
M=D
