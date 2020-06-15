@256 // SP
D=A
@SP
M=D
@Sys.init$0 // Save return address
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@5 //Reposition args - n - 5
D=A
@SP
D=M-D
@ARG
M=D
@SP // Rep LCL
D=M
@LCL
M=D
@Sys.init$Sys.init // Jump to function
0;JMP
(Sys.init$0) // return point
(Sys.init$Sys.init)
(Sys.init$WHILE)
@Sys.init$WHILE
