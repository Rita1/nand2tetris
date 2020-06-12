@256 // Init SP
D=A
@SP
M=D
(ABC$ABC)
@0 // temp. should be 0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0 // temp. should be 0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL // Frame temp. variable
D=M
@R14
M=D
@5 // RET = FRAME-5
D=A
@R14
A=M-D
D=M
@R15
M=D
@SP // POP last value from stack to ARGS memory location
A=M-1
D=M
@ARG
A=M
M=D
@ARG // SP = ARG + 1
D=M
@SP
M=D+1
@R14 // THAT = *(FRAME-1)
A=M-1
D=M
@THAT
M=D
@2 // THIS = *(FRAME-2)
D=A
@R14
A=M-D
D=M
@THIS
M=D
@3 // ARG = *(FRAME-3)
D=A
@R14
A=M-D
D=M
@ARG
M=D
@4 // LCL = *(FRAME-4)
D=A
@R14
A=M-D
D=M
@LCL
M=D
@R15 // GOTO RET
A=M
