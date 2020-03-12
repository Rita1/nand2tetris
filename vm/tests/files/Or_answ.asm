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
@1 // Constant 3
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
M=D|M
