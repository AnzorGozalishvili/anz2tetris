# Machine Language

Introduction to low-level programming in the Hack assembly language, focusing on both machine language concepts and basic programming constructs.

## Language Specifications

### A-Instructions
| Format    | Description                          | Example    |
|-----------|--------------------------------------|------------|
| @value    | Load value into A register          | @21       |
| @symbol   | Load symbol's address into A        | @SCREEN   |

### C-Instructions
| Format    | Description                          | Example    |
|-----------|--------------------------------------|------------|
| dest=comp | Compute and store in destination    | D=M+1     |
| comp;jump | Compute and jump if condition met   | D;JGT     |

### Predefined Symbols
| Symbol    | Value     | Description              |
|-----------|-----------|--------------------------|
| R0-R15    | 0-15      | Virtual registers        |
| SCREEN    | 16384     | Screen memory map        |
| KBD       | 24576     | Keyboard memory map      |
| SP        | 0         | Stack pointer            |
| LCL       | 1         | Local segment pointer    |
| ARG       | 2         | Argument segment pointer |
| THIS      | 3         | This segment pointer     |
| THAT      | 4         | That segment pointer     |

## Program Examples

### Basic Addition
```assembly
// Add two numbers
@2      // Load 2 into A
D=A     // D = 2
@3      // Load 3 into A
D=D+A   // D = D + 3
@0      // Select R0
M=D     // R0 = D (store result)
```

### Simple Loop
```assembly
// Sum 1 to n
    @i      // i = 1
    M=1
    @sum    // sum = 0
    M=0
(LOOP)
    @i      // if i > n goto END
    D=M
    @n
    D=D-M
    @END
    D;JGT
    @i      // sum += i
    D=M
    @sum
    M=M+D
    @i      // i++
    M=M+1
    @LOOP   // goto LOOP
    0;JMP
(END)
    @END    // infinite loop
    0;JMP
```

### Rectangle Drawing
```assembly
// Draw a 16x16 rectangle
    @SCREEN
    D=A
    @addr
    M=D     // addr = SCREEN
    @16     // n = 16
    D=A
    @n
    M=D
(LOOP)
    @n      // if n = 0 goto END
    D=M
    @END
    D;JEQ
    @addr   // RAM[addr] = -1
    A=M
    M=-1
    @32     // addr += 32
    D=A
    @addr
    M=M+D
    @n      // n--
    M=M-1
    @LOOP
    0;JMP
(END)
    @END
    0;JMP
```

## Instruction Set

### Computation Fields
| comp   | Description           |
|--------|-----------------------|
| 0      | Constant 0           |
| 1      | Constant 1           |
| -1     | Constant -1          |
| D      | D register           |
| A      | A register           |
| M      | RAM[A]               |
| !D     | Not D                |
| !A     | Not A                |
| -D     | Negate D             |
| -A     | Negate A             |
| D+1    | D plus 1             |
| A+1    | A plus 1             |
| D-1    | D minus 1            |
| A-1    | A minus 1            |
| D+A    | D plus A             |
| D-A    | D minus A            |
| A-D    | A minus D            |
| D&A    | D AND A              |
| D|A    | D OR A               |

### Jump Conditions
| jump   | Description           |
|--------|-----------------------|
| JGT    | Jump if greater than |
| JEQ    | Jump if equal        |
| JGE    | Jump if greater/equal|
| JLT    | Jump if less than    |
| JNE    | Jump if not equal    |
| JLE    | Jump if less/equal   |
| JMP    | Jump unconditionally |

## Project Structure
```
project4/
├── mult/
│   ├── Mult.asm    // Multiplication program
│   └── Mult.tst    // Test script
└── fill/
    ├── Fill.asm    // Screen interaction
    └── Fill.tst    // Test script
```

## Testing Instructions
1. Open CPU Emulator
2. Load program file (.asm)
3. Load test script (.tst)
4. Run script
5. Compare with expected output

## Common Issues
- Label naming conflicts
- Infinite loops
- Stack overflow
- Memory access violations
- Uninitialized variables

## Programming Patterns

### Variable Declaration
```assembly
// Declare variables
    @variable
    M=0     // Initialize to 0
```

### If-Then
```assembly
    @condition
    D=M
    @THEN
    D;JNE   // Jump if condition true
    // ELSE code
    @END
    0;JMP
(THEN)
    // THEN code
(END)
```

### While Loop
```assembly
(WHILE)
    @condition
    D=M
    @END
    D;JEQ   // Exit if condition false
    // Loop body
    @WHILE
    0;JMP
(END)
```

## Resources
- [nand2tetris Course](https://www.nand2tetris.org)
- [Machine Language](https://www.nand2tetris.org/project04)
- [CPU Emulator Tutorial](https://www.nand2tetris.org/software) 