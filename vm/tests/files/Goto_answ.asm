@256
D=A
@SP
M=D
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
(Null$LOOP_START) // Label
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP //Start if GOTO
M=M-1
A=M
D=M
@Null$LOOP_START
D;JNE
@Null$LOOP_START // Goto
0;JMP

