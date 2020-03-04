// Int
@256
D=A
@SP
M=D
@7 // Constant 7
D=A
@SP
A=M
M=D
@SP
M=M+1
@8 // Constant 8
@SP
A=M
M=D
@SP
M=M+1
// Add
@SP
A=M
D=M
M=0
@SP
A=M-1
D=D+M
M=D
@SP // Update pointer
D=M-1
M=D

