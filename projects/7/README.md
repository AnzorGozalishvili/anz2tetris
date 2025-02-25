# VM I: Stack Arithmetic

Implementation of the first part of the VM translator, focusing on stack arithmetic and logical commands of the VM language.

## VM Specifications

### Stack Operations
| Command   | Description                          | Example    |
|-----------|--------------------------------------|------------|
| push s i  | Push segment[i] onto stack          | push local 2|
| pop s i   | Pop from stack to segment[i]        | pop temp 3  |
| add       | Add top two stack elements          | add        |
| sub       | Subtract                            | sub        |
| neg       | Negate top element                  | neg        |

### Memory Segments
| Segment   | Purpose                             | Assembly    |
|-----------|-------------------------------------|-------------|
| local     | Function local variables            | LCL        |
| argument  | Function arguments                  | ARG        |
| this      | Object fields                       | THIS       |
| that      | Array elements                      | THAT       |
| constant  | Constant values                     | @value     |
| static    | Static variables                    | @filename.i |
| temp      | Temporary variables                 | R5-R12     |
| pointer   | THIS (0) and THAT (1) base         | R3-R4      |

## Implementation Examples

### Stack Arithmetic
```python
class VMTranslator:
    def translate_add(self):
        return [
            "// add",
            "@SP",     # Stack pointer
            "AM=M-1",  # Decrement SP, M points to top
            "D=M",     # D = top value
            "A=A-1",   # Point to second value
            "M=M+D"    # Add values
        ]

    def translate_push(self, segment, index):
        if segment == "constant":
            return [
                f"// push constant {index}",
                f"@{index}",
                "D=A",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1"
            ]
```

### Logical Operations
```python
class VMTranslator:
    def translate_eq(self):
        label = self.next_label()
        return [
            "// eq",
            "@SP",
            "AM=M-1",
            "D=M",     # D = y
            "A=A-1",
            "D=M-D",   # D = x-y
            f"@TRUE.{label}",
            "D;JEQ",   # if x-y=0 goto TRUE
            "@SP",
            "A=M-1",
            "M=0",     # false
            f"@CONTINUE.{label}",
            "0;JMP",
            f"(TRUE.{label})",
            "@SP",
            "A=M-1",
            "M=-1",    # true
            f"(CONTINUE.{label})"
        ]
```

## Test Cases

### Basic Arithmetic
```
// Input: SimpleAdd.vm
push constant 7
push constant 8
add

// Output: SimpleAdd.asm
@7
D=A
@SP
A=M
M=D
@SP
M=M+1
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
M=M+D
```

### Stack Operations
```
// Input: StackTest.vm
push constant 17
push constant 17
eq
push constant 17
push constant 16
eq

// Output: StackTest.asm
// ... push 17 twice
@SP
AM=M-1
D=M
A=A-1
D=M-D
@TRUE.0
D;JEQ
@SP
A=M-1
M=0
@CONTINUE.0
0;JMP
(TRUE.0)
@SP
A=M-1
M=-1
(CONTINUE.0)
```

## Project Structure
```
project7/
├── VMTranslator
│   ├── main.py
│   ├── parser.py
│   └── code_writer.py
├── StackArithmetic/
│   ├── SimpleAdd/
│   │   ├── SimpleAdd.vm
│   │   └── SimpleAdd.asm
│   └── StackTest/
│       ├── StackTest.vm
│       └── StackTest.asm
└── MemoryAccess/
    ├── BasicTest/
    │   ├── BasicTest.vm
    │   └── BasicTest.asm
    └── PointerTest/
        ├── PointerTest.vm
        └── PointerTest.asm
```

## Testing Instructions
1. Run VM translator on .vm file
2. Compare output .asm with provided solution
3. Load .asm file into CPU Emulator
4. Run test script
5. Verify memory segments and stack state

## Common Issues
- Stack pointer management
- Segment base address handling
- Label generation uniqueness
- Comparison operation implementation
- Static variable naming

## VM Command Types

### Arithmetic/Logical
| Command | Stack Effect | Description        |
|---------|-------------|--------------------|
| add     | -1          | x + y              |
| sub     | -1          | x - y              |
| neg     | 0           | -y                 |
| eq      | -1          | x == y             |
| gt      | -1          | x > y              |
| lt      | -1          | x < y              |
| and     | -1          | x & y              |
| or      | -1          | x | y              |
| not     | 0           | !y                 |

### Memory Access
| Command     | Effect    | Description        |
|-------------|----------|--------------------|
| push s i    | +1       | *sp = seg[i]       |
| pop s i     | -1       | seg[i] = *sp       |

## Memory Mapping
```
RAM[0]    : SP  (stack pointer)
RAM[1]    : LCL (local base)
RAM[2]    : ARG (argument base)
RAM[3]    : THIS
RAM[4]    : THAT
RAM[5-12] : temp segment
RAM[13-15]: general purpose
RAM[16-255]: static variables
RAM[256-2047]: stack
```

## Resources
- [nand2tetris Course](https://www.nand2tetris.org)
- [VM Specification](https://www.nand2tetris.org/project07)
- [CPU Emulator Tutorial](https://www.nand2tetris.org/software) 