# High-Level Language (Jack)

Introduction to the Jack programming language, a simple object-based language with Java-like syntax, designed for learning the fundamentals of high-level programming.

## Language Specifications

### Basic Types
| Type      | Description                          | Example           |
|-----------|--------------------------------------|-------------------|
| int       | 16-bit integer                      | var int x = 5;    |
| boolean   | true/false                          | var boolean b;    |
| char      | Unicode character                   | var char c = 'A'; |
| String    | String object                       | var String s;     |
| Array     | Array object                        | var Array a;      |

### Class Structure
```jack
class Example {
    // Class-level variables (fields)
    field int x, y;
    static boolean debug;

    // Constructor
    constructor Example new(int ax, int ay) {
        let x = ax;
        let y = ay;
        return this;
    }

    // Methods
    method void print() {
        do Output.printInt(x);
        do Output.printInt(y);
        return;
    }
}
```

### Control Structures
```jack
// If statement
if (x < 0) {
    let x = -x;
}
else {
    let x = x + 1;
}

// While loop
while (count > 0) {
    let sum = sum + count;
    let count = count - 1;
}

// Do statement
do screen.drawRectangle(x, y, x+width, y+height);
```

## Example Programs

### Simple Game
```jack
class Game {
    field Square square;
    field int direction;

    constructor Game new() {
        let square = Square.new(0, 0, 30);
        let direction = 0;
        return this;
    }

    method void run() {
        var char key;
        var boolean exit;
        
        let exit = false;
        
        while (~exit) {
            let key = Keyboard.keyPressed();
            
            if (key = 81) { // q key
                let exit = true;
            }
            if (key = 131) { // up arrow
                do square.moveUp();
            }
            do Sys.wait(50);
        }
        return;
    }
}
```

### Array Manipulation
```jack
class Sort {
    function void bubbleSort(Array arr, int length) {
        var int i, j, temp;
        var boolean swapped;
        
        let i = 0;
        while (i < (length - 1)) {
            let swapped = false;
            let j = 0;
            while (j < (length - i - 1)) {
                if (arr[j] > arr[j + 1]) {
                    let temp = arr[j];
                    let arr[j] = arr[j + 1];
                    let arr[j + 1] = temp;
                    let swapped = true;
                }
                let j = j + 1;
            }
            if (~swapped) {
                return;
            }
            let i = i + 1;
        }
        return;
    }
}
```

## Project Structure
```
project9/
├── Example/
│   ├── Main.jack
│   └── Game.jack
├── Square/
│   ├── Main.jack
│   ├── Square.jack
│   └── SquareGame.jack
└── Average/
    ├── Main.jack
    └── Average.jack
```

## Language Features

### Object Orientation
- Classes and objects
- Method calls
- Constructor/method definitions
- this keyword
- Object instantiation

### Memory Management
- Constructor allocation
- Object disposal
- Array allocation
- Local variables
- Static/field variables

### Standard Library
| Class     | Purpose                             |
|-----------|-------------------------------------|
| Math      | Mathematical operations             |
| String    | String manipulation                 |
| Array     | Array operations                    |
| Output    | Screen output                       |
| Screen    | Graphics operations                 |
| Keyboard  | Keyboard input                      |
| Memory    | Memory operations                   |
| Sys      | System services                     |

## Common Patterns

### Constructor Pattern
```jack
class Point {
    field int x, y;

    constructor Point new(int ax, int ay) {
        let x = ax;
        let y = ay;
        return this;
    }

    method void dispose() {
        do Memory.deAlloc(this);
        return;
    }
}
```

### Main Program Pattern
```jack
class Main {
    function void main() {
        var Game game;
        let game = Game.new();
        do game.run();
        do game.dispose();
        return;
    }
}
```

## Testing Instructions
1. Write Jack program (.jack files)
2. Compile with Jack compiler
3. Run on VM emulator
4. Verify program behavior

## Common Issues
- Missing return statements
- Array bounds checking
- Object disposal
- Type mismatches
- Scope understanding

## Best Practices
- Initialize variables
- Dispose objects properly
- Use meaningful names
- Comment complex logic
- Break down large methods

## Resources
- [nand2tetris Course](https://www.nand2tetris.org)
- [Jack Language Specification](https://www.nand2tetris.org/project09)
- [Jack OS API](https://www.nand2tetris.org/project12) 