// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

// Initialize variables
@SCREEN
D=A
@screenptr
M=D      // screenptr = SCREEN base address

@8192    // Number of 16-bit words in screen (256 rows * 512/16 words per row)
D=A
@count
M=D      // count = 8192

(LOOP)
    // Check keyboard
    @KBD
    D=M
    
    // If key pressed, set color to black (-1), else white (0)
    @color
    M=0
    @SETCOLOR
    D;JEQ
    @color
    M=-1
    
(SETCOLOR)
    // Reset screen pointer and counter for each iteration
    @SCREEN
    D=A
    @screenptr
    M=D
    
    @8192
    D=A
    @count
    M=D
    
(FILLSCREEN)
    // Fill current word with color
    @color
    D=M
    @screenptr
    A=M
    M=D
    
    // Increment screen pointer
    @screenptr
    M=M+1
    
    // Decrement counter
    @count
    M=M-1
    D=M
    
    // If counter > 0, continue filling
    @FILLSCREEN
    D;JGT
    
    // Return to main loop
    @LOOP
    0;JMP
