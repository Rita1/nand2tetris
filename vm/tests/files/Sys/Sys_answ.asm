@256 // SP
D=A
@SP
M=D
@Sys.init$Sys.init // Save return address
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
M=M-D
@SP // Rep LCL
D=M
@LCL
M=D
@Sys.init$Sys.init // Goto function
0;JMP
(Sys.init$Sys.init)
(Sys.init$WHILE)
@Sys.init$WHILE
0;JMP
