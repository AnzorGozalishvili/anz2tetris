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
// function Class1.set 0
(Class1.set)
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
// pop static 0
@SP
AM=M-1
D=M
@Class1.0
M=D
// push argument 1
@ARG
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop static 1
@SP
AM=M-1
D=M
@Class1.1
M=D
// push constant 0
@0
D=A
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
// function Class1.get 0
(Class1.get)
// push static 0
@Class1.0
D=M
@SP
A=M
M=D
@SP
M=M+1
// push static 1
@Class1.1
D=M
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
// push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Class1.set 2
@Sys.init$ret.1    // push return address
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
@2
D=D-A
@ARG
M=D
@SP             // LCL = SP
D=M
@LCL
M=D
@Class1.set    // goto function
0;JMP
(Sys.init$ret.1)    // return label
// pop temp 0
@5
D=A
@0
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// push constant 23
@23
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 15
@15
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Class2.set 2
@Sys.init$ret.2    // push return address
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
@2
D=D-A
@ARG
M=D
@SP             // LCL = SP
D=M
@LCL
M=D
@Class2.set    // goto function
0;JMP
(Sys.init$ret.2)    // return label
// pop temp 0
@5
D=A
@0
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// call Class1.get 0
@Sys.init$ret.3    // push return address
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
@Class1.get    // goto function
0;JMP
(Sys.init$ret.3)    // return label
// call Class2.get 0
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
@0
D=D-A
@ARG
M=D
@SP             // LCL = SP
D=M
@LCL
M=D
@Class2.get    // goto function
0;JMP
(Sys.init$ret.4)    // return label
(Sys.init$END)
@Sys.init$END
0;JMP
// function Class2.set 0
(Class2.set)
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
// pop static 0
@SP
AM=M-1
D=M
@Class2.0
M=D
// push argument 1
@ARG
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop static 1
@SP
AM=M-1
D=M
@Class2.1
M=D
// push constant 0
@0
D=A
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
// function Class2.get 0
(Class2.get)
// push static 0
@Class2.0
D=M
@SP
A=M
M=D
@SP
M=M+1
// push static 1
@Class2.1
D=M
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
