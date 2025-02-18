// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

// Initialize R2 to 0
@R2
M=0

// Load R1 into D
@R1 
D=M

// If R1 is 0, we're done
@END
D;JEQ

// Load R0 into D 
@R0
D=M

// If R0 is 0, we're done
@END
D;JEQ

// Initialize counter to R1
@R1
D=M
@counter
M=D

// Main multiplication loop
(LOOP)
    // Add R0 to R2
    @R0
    D=M
    @R2
    M=M+D
    
    // Decrement counter
    @counter
    M=M-1
    D=M
    
    // If counter > 0, continue loop
    @LOOP
    D;JGT

(END)
    @END
    0;JMP
