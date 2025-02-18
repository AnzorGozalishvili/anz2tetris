# Jack Compiler

A compiler that translates Jack programs into VM code. This is the final stage of the Jack compilation process, converting high-level Jack code into VM commands that can be executed by the VM Emulator.

## Setup

### Requirements
- Python 3.6 or higher
- nand2tetris VM Emulator (for running compiled code)

### Installation
```bash
# Make the compiler executable
chmod +x JackCompiler.py

# Create symbolic link
ln -sf JackCompiler.py JackCompiler
```

## Components

### 1. JackCompiler (Main Driver)
- Entry point for compilation process
- Handles file/directory input
- Coordinates the compilation pipeline
- Generates .vm output files

### 2. JackTokenizer
- Performs lexical analysis
- Breaks input into atomic tokens:
  - Keywords (class, if, while, etc.)
  - Symbols ({, }, (, ), etc.)
  - Identifiers (variable/class names)
  - Integer constants
  - String constants

### 3. SymbolTable
- Manages variable scoping and tracking
- Maintains two separate symbol tables:
  - Class-level scope (static/field variables)
  - Subroutine-level scope (argument/local variables)
- Tracks variable properties:
  - Name
  - Type
  - Kind (STATIC, FIELD, ARG, VAR)
  - Index

### 4. VMWriter
- Generates VM commands
- Handles:
  - Memory segments (local, argument, this, that)
  - Arithmetic operations
  - Function declarations
  - Function calls
  - Control flow (labels, goto)

### 5. CompilationEngine
Core compiler that:
- Implements recursive descent parsing
- Manages symbol tables
- Generates VM code for:
  - Class and subroutine declarations
  - Variable declarations
  - Statements (let, if, while, do, return)
  - Expressions and operators
  - Array access
  - Method/function calls
  - Object construction

## Usage

```bash
python JackCompiler.py <input>
```

Where `<input>` can be:
- A single .jack file
- A directory containing .jack files

The compiler will generate corresponding .vm files in the same directory.

## Memory Segment Mapping
| Jack Variable | VM Segment |
|--------------|------------|
| static       | static     |
| field        | this       |
| argument     | argument   |
| local        | local      |
| array[i]     | that       |

## Troubleshooting

Common errors and solutions:

1. Syntax Errors
   - "Expected X, got Y": Check Jack syntax at the indicated location
   - "Undefined variable": Ensure variables are declared before use
   - "Invalid subroutine call": Verify method/function exists in class

2. Runtime Errors
   - Array index out of bounds: Check array access logic
   - Null pointer: Ensure objects are constructed before use
   - Stack overflow: Check for infinite recursion

## Testing
Test with provided Jack programs:
- Average: Basic arithmetic and array handling
- ComplexArrays: Array manipulation
- ConvertToBin: Binary operations
- Pong: Interactive game
- Seven: Simple constant
- Square: Interactive graphics

## Known Limitations
- No optimization of generated VM code
- Limited error recovery
- No source-level debugging support

## Resources
- [nand2tetris Course](https://www.nand2tetris.org)
- [Jack Language Specification](https://www.nand2tetris.org/project09)
- [VM Specification](https://www.nand2tetris.org/project07)

## Version
1.0.0 - Initial release for nand2tetris Project 11

## License
MIT License - See LICENSE file for details

## Examples

### 1. Basic Function
```jack
// Main.jack
class Main {
   function void main() {
      do Output.printInt(42);
      return;
   }
}
```

Generated VM code:
```vm
function Main.main 0    // function name and number of local variables
push constant 42       // push argument value
call Output.printInt 1 // call function with 1 argument
push constant 0       // push return value for void function
return               // return from function
```

### 2. Object Construction and Methods
```jack
class Point {
    field int x, y;
    
    constructor Point new(int ax, int ay) {
        let x = ax;
        let y = ay;
        return this;
    }
    
    method int getX() {
        return x;
    }
}
```

Generated VM code:
```vm
function Point.new 0     // Constructor
push constant 2         // Size of object (2 fields)
call Memory.alloc 1     // Allocate memory
pop pointer 0          // Set this pointer
push argument 0        // First argument (ax)
pop this 0            // Store in field x
push argument 1       // Second argument (ay)
pop this 1           // Store in field y
push pointer 0       // Push this (return value)
return

function Point.getX 0   // Method
push argument 0        // Push this (argument 0 for methods)
pop pointer 0         // Set this pointer
push this 0          // Push field x
return
```

### 3. Array Handling
```jack
class Main {
    function void main() {
        var Array a;
        let a = Array.new(3);
        let a[0] = 10;
        let a[1] = 20;
        let a[2] = 30;
        return;
    }
}
```

Generated VM code:
```vm
function Main.main 1    // 1 local variable
push constant 3        // Array size
call Array.new 1       // Create array
pop local 0           // Store array base address

push local 0          // Array base address
push constant 0       // Index
add                  // Calculate target address
push constant 10     // Value
pop temp 0          // Save value
pop pointer 1       // Set that pointer
push temp 0         // Restore value
pop that 0         // Store in array

// Similar pattern for other array assignments
```

These examples demonstrate:
- Function and method compilation
- Object construction and field access
- Array allocation and manipulation
- Memory segment usage
- Stack operations