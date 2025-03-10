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
// function Sys.init 0
(Sys.init)
// push constant 4000
@4000
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 0
@SP
AM=M-1
D=M
@3
M=D
// push constant 5000
@5000
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1
@SP
AM=M-1
D=M
@4
M=D
// call Sys.main 0
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
@0
D=D-A
@ARG
M=D
@SP             // LCL = SP
D=M
@LCL
M=D
@Sys.main    // goto function
0;JMP
(Sys.init$ret.1)    // return label
// pop temp 1
@5
D=A
@1
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
(Sys.init$LOOP)
@Sys.init$LOOP
0;JMP
// function Sys.main 5
(Sys.main)
@0    // push 0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0    // push 0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0    // push 0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0    // push 0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0    // push 0
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 4001
@4001
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 0
@SP
AM=M-1
D=M
@3
M=D
// push constant 5001
@5001
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1
@SP
AM=M-1
D=M
@4
M=D
// push constant 200
@200
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop local 1
@LCL
D=M
@1
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// push constant 40
@40
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop local 2
@LCL
D=M
@2
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop local 3
@LCL
D=M
@3
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// push constant 123
@123
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Sys.add12 1
@Sys.main$ret.2    // push return address
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
@Sys.add12    // goto function
0;JMP
(Sys.main$ret.2)    // return label
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
// push local 0
@LCL
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// push local 1
@LCL
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// push local 2
@LCL
D=M
@2
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// push local 3
@LCL
D=M
@3
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// push local 4
@LCL
D=M
@4
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// Binary operation +
@SP
AM=M-1
D=M
A=A-1
M=M+D
// Binary operation +
@SP
AM=M-1
D=M
A=A-1
M=M+D
// Binary operation +
@SP
AM=M-1
D=M
A=A-1
M=M+D
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
// function Sys.add12 0
(Sys.add12)
// push constant 4002
@4002
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 0
@SP
AM=M-1
D=M
@3
M=D
// push constant 5002
@5002
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1
@SP
AM=M-1
D=M
@4
M=D
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
// push constant 12
@12
D=A
@SP
A=M
M=D
@SP
M=M+1
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
