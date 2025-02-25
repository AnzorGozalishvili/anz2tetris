# Compiler II: Code Generation

Implementation of the second part of the Jack compiler, translating the parsed code into VM commands that can be executed by the VM Emulator.

## Compiler Specifications

### Symbol Table
| Kind      | Description                          | Index Range    |
|-----------|--------------------------------------|----------------|
| STATIC    | Class-level static variables         | 0...           |
| FIELD     | Class-level instance variables       | 0...           |
| ARG       | Method/function arguments            | 0...           |
| VAR       | Subroutine local variables          | 0...           |

### VM Commands Generated
| Category   | Commands                            | Example           |
|------------|-------------------------------------|-------------------|
| Memory     | push, pop                          | push local 0      |
| Arithmetic | add, sub, neg, eq, gt, lt          | add              |
| Flow       | label, goto, if-goto               | label WHILE_EXP0 |
| Function   | function, call, return             | function Main.main 2 |

## Implementation Examples

### Symbol Table
```python
class SymbolTable:
    def __init__(self):
        self.class_table = {}    # Class-level scope
        self.subroutine_table = {}  # Subroutine-level scope
        self.index_counters = {
            'STATIC': 0, 'FIELD': 0,
            'ARG': 0, 'VAR': 0
        }

    def define(self, name, type, kind):
        table = (self.class_table if kind in ['STATIC', 'FIELD']
                else self.subroutine_table)
        table[name] = {
            'type': type,
            'kind': kind,
            'index': self.index_counters[kind]
        }
        self.index_counters[kind] += 1

    def var_count(self, kind):
        return self.index_counters[kind]

    def kind_of(self, name):
        if name in self.subroutine_table:
            return self.subroutine_table[name]['kind']
        if name in self.class_table:
            return self.class_table[name]['kind']
        return None
```

### Code Generation
```python
class VMWriter:
    def __init__(self, output_file):
        self.output = output_file

    def write_push(self, segment, index):
        self.output.write(f"push {segment} {index}\n")

    def write_pop(self, segment, index):
        self.output.write(f"pop {segment} {index}\n")

    def write_arithmetic(self, command):
        self.output.write(f"{command}\n")

    def write_label(self, label):
        self.output.write(f"label {label}\n")

    def write_goto(self, label):
        self.output.write(f"goto {label}\n")

    def write_function(self, name, locals):
        self.output.write(f"function {name} {locals}\n")
```

## Test Cases

### Expression Compilation
```
// Input: Jack code
let sum = a + (b * c);

// Output: VM code
push local 1    // a
push local 2    // b
push local 3    // c
call Math.multiply 2
add
pop local 0     // sum
```

### If Statement
```
// Input: Jack code
if (x < 0) {
    let x = -x;
}

// Output: VM code
push local 0    // x
push constant 0
lt
not
if-goto IF_END0
push local 0    // x
neg
pop local 0     // x
label IF_END0
```

### Method Call
```
// Input: Jack code
method void draw() {
    do screen.setColor(true);
    do screen.drawRectangle(x, y, x+width, y+height);
    return;
}

// Output: VM code
function Square.draw 0
push argument 0
pop pointer 0
push constant 0
not
call Screen.setColor 1
push argument 0
push this 0     // x
push this 1     // y
push this 0     // x
push this 2     // width
add
push this 1     // y
push this 3     // height
add
call Screen.drawRectangle 4
push constant 0
return
```

## Project Structure
```
project11/
├── JackCompiler/
│   ├── JackCompiler.py
│   ├── CompilationEngine.py
│   ├── SymbolTable.py
│   └── VMWriter.py
├── Seven/
│   ├── Main.jack
│   └── Main.vm
├── ConvertToBin/
│   ├── Main.jack
│   └── Main.vm
└── Square/
    ├── Main.jack
    ├── Square.jack
    ├── SquareGame.jack
    └── *.vm
```

## Testing Instructions
1. Run compiler on .jack files
2. Compare output .vm with provided solution
3. Run generated code in VM Emulator
4. Verify program behavior

## Common Issues
- Array access handling
- Object initialization
- Method call vs function call
- Expression evaluation order
- Variable scope resolution

## Code Generation Patterns

### Constructor
```
// Jack code
constructor Square new(int Ax, int Ay, int Asize) {
    let x = Ax;
    let y = Ay;
    let size = Asize;
    return this;
}

// VM code
function Square.new 0
push constant 3    // Object size
call Memory.alloc 1
pop pointer 0
push argument 0
pop this 0
push argument 1
pop this 1
push argument 2
pop this 2
push pointer 0
return
```

### Object Method
```
// Jack code
method void incSize() {
    if (size < 100) {
        let size = size + 2;
    }
    return;
}

// VM code
function Square.incSize 0
push argument 0
pop pointer 0
push this 2
push constant 100
lt
if-goto IF_TRUE0
goto IF_FALSE0
label IF_TRUE0
push this 2
push constant 2
add
pop this 2
label IF_FALSE0
push constant 0
return
```

## Resources
- [nand2tetris Course](https://www.nand2tetris.org)
- [Compiler Specification](https://www.nand2tetris.org/project11)
- [VM Specification](https://www.nand2tetris.org/project08) 