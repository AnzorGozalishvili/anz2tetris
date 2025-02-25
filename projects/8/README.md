# VM II: Program Control

Implementation of the second part of the VM translator, focusing on program flow and function calling commands of the VM language.

## VM Specifications

### Program Flow
| Command     | Description                          | Example      |
|-------------|--------------------------------------|--------------|
| label l     | Define label l                      | label LOOP   |
| goto l      | Unconditional jump to label         | goto END     |
| if-goto l   | Conditional jump to label           | if-goto LOOP |

### Function Commands
| Command     | Description                          | Example           |
|-------------|--------------------------------------|-------------------|
| function f n| Declare function with n locals      | function mult 2   |
| call f m    | Call function with m arguments      | call mult 2       |
| return      | Return from function                | return            |

### Function State
| Segment   | Purpose                             | Saved by    |
|-----------|-------------------------------------|-------------|
| local     | Function's local variables          | Callee     |
| argument  | Function's parameters               | Caller     |
| this/that | Object pointers                     | Caller     |
| pointer   | THIS/THAT base addresses            | Caller     |
| temp      | Temporary storage                   | Caller     |
| static    | Static variables                    | Compiler   |

## Implementation Examples

### Function Call
```python
class VMTranslator:
    def translate_call(self, function_name, num_args):
        return_label = self.next_return_label()
        return [
            f"// call {function_name} {num_args}",
            # Push return address
            f"@{return_label}",
            "D=A",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
            # Push LCL, ARG, THIS, THAT
            "@LCL",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
            # ... similar for ARG, THIS, THAT
            # Reposition ARG
            f"@{5 + num_args}",
            "D=A",
            "@SP",
            "D=M-D",
            "@ARG",
            "M=D",
            # Reposition LCL
            "@SP",
            "D=M",
            "@LCL",
            "M=D",
            # Jump to function
            f"@{function_name}",
            "0;JMP",
            # Return label
            f"({return_label})"
        ]
```

### Function Return
```python
class VMTranslator:
    def translate_return(self):
        return [
            "// return",
            # Frame = LCL
            "@LCL",
            "D=M",
            "@R13",  # R13 = frame
            "M=D",
            # Ret = *(frame-5)
            "@5",
            "D=A",
            "@R13",
            "A=M-D",
            "D=M",
            "@R14",  # R14 = return address
            "M=D",
            # *ARG = pop()
            "@SP",
            "AM=M-1",
            "D=M",
            "@ARG",
            "A=M",
            "M=D",
            # SP = ARG + 1
            "@ARG",
            "D=M+1",
            "@SP",
            "M=D",
            # Restore caller's state
            "@R13",
            "AM=M-1",
            "D=M",
            "@THAT",
            "M=D",
            # ... similar for THIS, ARG, LCL
            # goto return address
            "@R14",
            "A=M",
            "0;JMP"
        ]
```

## Test Cases

### Basic Function
```
// Input: SimpleFunction.vm
function SimpleFunction.test 2
push local 0
push local 1
add
not
push argument 0
add
push argument 1
sub
return

// Output: SimpleFunction.asm
(SimpleFunction.test)
@SP
A=M
M=0
@SP
M=M+1
@SP
A=M
M=0
@SP
M=M+1
// ... rest of function implementation
```

### Function Call
```
// Input: FibonacciElement.vm
function Sys.init 0
push constant 4
call Main.fibonacci 1
label WHILE
goto WHILE

function Main.fibonacci 0
push argument 0
push constant 2
lt
if-goto IF_TRUE
goto IF_FALSE
label IF_TRUE
push argument 0
return
label IF_FALSE
// ... rest of fibonacci implementation
```

## Project Structure
```
project8/
├── VMTranslator/
│   ├── main.py
│   ├── parser.py
│   └── code_writer.py
├── FunctionCalls/
│   ├── SimpleFunction/
│   │   ├── SimpleFunction.vm
│   │   └── SimpleFunction.asm
│   ├── FibonacciElement/
│   │   ├── Main.vm
│   │   ├── Sys.vm
│   │   └── FibonacciElement.asm
│   └── StaticsTest/
│       ├── Class1.vm
│       ├── Class2.vm
│       └── StaticsTest.asm
└── ProgramFlow/
    ├── BasicLoop/
    │   ├── BasicLoop.vm
    │   └── BasicLoop.asm
    └── FibonacciSeries/
        ├── FibonacciSeries.vm
        └── FibonacciSeries.asm
```

## Testing Instructions
1. Run VM translator on .vm file(s)
2. Compare output .asm with solution
3. Load .asm into CPU Emulator
4. Run test script
5. Verify function calls and returns

## Common Issues
- Function frame setup/teardown
- Return address management
- Static variable handling
- Label scope and uniqueness
- Stack alignment

## Call Frame Structure
```
// Call frame layout (from SP-1 down)
arg n-1
...
arg 0
return address
saved LCL
saved ARG
saved THIS
saved THAT
local 0
...
local n-1
```

## Bootstrap Code
```assembly
// Initialize SP and call Sys.init
@256
D=A
@SP
M=D
@Sys.init
0;JMP
```

## Resources
- [nand2tetris Course](https://www.nand2tetris.org)
- [VM Specification](https://www.nand2tetris.org/project08)
- [CPU Emulator Tutorial](https://www.nand2tetris.org/software) 