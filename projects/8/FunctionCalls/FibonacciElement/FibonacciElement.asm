// Bootstrap code
@256            // Initialize SP=256
D=A
@SP
M=D
// call Sys.init 0
@Bootstrap$ret.0    // push return address
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL            // push LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG            // push ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS           // push THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT           // push THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP             // ARG = SP - 5 - num_args
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
@SP             // LCL = SP
D=M
@LCL
M=D
@Sys.init    // goto function
0;JMP
(Bootstrap$ret.0)    // return label
// function Main.fibonacci 0
(Main.fibonacci)
// push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// Comparison lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@LT_1_TRUE
D;JLT
@SP
A=M-1
M=0
@LT_1_END
0;JMP
(LT_1_TRUE)
@SP
A=M-1
M=-1
(LT_1_END)
@SP
AM=M-1
D=M
@Main.fibonacci$N_LT_2
D;JNE
@Main.fibonacci$N_GE_2
0;JMP
(Main.fibonacci$N_LT_2)
// push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// return
@LCL            // FRAME = LCL
D=M
@R13            // R13 = FRAME
M=D
@5              // RET = *(FRAME-5)
A=D-A
D=M
@R14            // R14 = RET
M=D
@SP             // *ARG = pop()
AM=M-1
D=M
@ARG
A=M
M=D
@ARG            // SP = ARG + 1
D=M+1
@SP
M=D
@R13            // THAT = *(FRAME-1)
AM=M-1
D=M
@THAT
M=D
@R13            // THIS = *(FRAME-2)
AM=M-1
D=M
@THIS
M=D
@R13            // ARG = *(FRAME-3)
AM=M-1
D=M
@ARG
M=D
@R13            // LCL = *(FRAME-4)
AM=M-1
D=M
@LCL
M=D
@R14            // goto RET
A=M
0;JMP
(Main.fibonacci$N_GE_2)
// push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// Binary operation -
@SP
AM=M-1
D=M
A=A-1
M=M-D
// call Main.fibonacci 1
@Main.fibonacci$ret.2    // push return address
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL            // push LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG            // push ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS           // push THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT           // push THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP             // ARG = SP - 5 - num_args
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
@SP             // LCL = SP
D=M
@LCL
M=D
@Main.fibonacci    // goto function
0;JMP
(Main.fibonacci$ret.2)    // return label
// push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// Binary operation -
@SP
AM=M-1
D=M
A=A-1
M=M-D
// call Main.fibonacci 1
@Main.fibonacci$ret.3    // push return address
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL            // push LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG            // push ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS           // push THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT           // push THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP             // ARG = SP - 5 - num_args
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
@SP             // LCL = SP
D=M
@LCL
M=D
@Main.fibonacci    // goto function
0;JMP
(Main.fibonacci$ret.3)    // return label
// Binary operation +
@SP
AM=M-1
D=M
A=A-1
M=M+D
// return
@LCL            // FRAME = LCL
D=M
@R13            // R13 = FRAME
M=D
@5              // RET = *(FRAME-5)
A=D-A
D=M
@R14            // R14 = RET
M=D
@SP             // *ARG = pop()
AM=M-1
D=M
@ARG
A=M
M=D
@ARG            // SP = ARG + 1
D=M+1
@SP
M=D
@R13            // THAT = *(FRAME-1)
AM=M-1
D=M
@THAT
M=D
@R13            // THIS = *(FRAME-2)
AM=M-1
D=M
@THIS
M=D
@R13            // ARG = *(FRAME-3)
AM=M-1
D=M
@ARG
M=D
@R13            // LCL = *(FRAME-4)
AM=M-1
D=M
@LCL
M=D
@R14            // goto RET
A=M
0;JMP
// function Sys.init 0
(Sys.init)
// push constant 4
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Main.fibonacci 1
@Sys.init$ret.4    // push return address
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL            // push LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG            // push ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS           // push THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT           // push THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP             // ARG = SP - 5 - num_args
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
@SP             // LCL = SP
D=M
@LCL
M=D
@Main.fibonacci    // goto function
0;JMP
(Sys.init$ret.4)    // return label
(Sys.init$END)
@Sys.init$END
0;JMP
