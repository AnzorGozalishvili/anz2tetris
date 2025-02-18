# Jack Operating System

A standard library providing essential services for Jack programs, abstracting hardware operations and providing high-level functionality.

## Memory Map
| Segment    | Address Range | Usage                |
|------------|---------------|----------------------|
| RAM[0-15]  | 0-15         | Virtual registers    |
| RAM[16-255]| 16-255       | Static variables     |
| Stack      | 256-2047     | Stack operations     |
| Heap       | 2048-16383   | Objects and arrays   |
| Screen     | 16384-24575  | Display memory       |
| Keyboard   | 24576        | Keyboard memory map  |

## Class Library

### 1. Math
Overview:
- Provides efficient mathematical operations
- Uses bit manipulation for multiplication
- Implements recursive division with overflow protection
- Binary search for square root calculation
- Maintains powers of 2 lookup table

Key Implementation:
```jack
class Math {
    static Array powersOfTwo;  // [1,2,4,8,16,32,64,...]

    function int multiply(int x, int y) {
        var int sum, shiftedX, j;
        while (j < 16) {  // Process each bit
            if (~((y & powersOfTwo[j]) = 0)) {
                let sum = sum + shiftedX;
            }
            let shiftedX = shiftedX + shiftedX;
            let j = j + 1;
        }
        return sum;
    }

    function int divide(int x, int y) {
        // Handle overflow case
        if ((y + y) < 0) { return (x > y) ? 1 : 0; }
        let q = Math.divide(x, y + y);
        return ((x - (2 * y * q)) < y) ? q + q : q + q + 1;
    }
}
```

Memory State:
```
Static segment:
[powersOfTwo]:
  [0]: 1     // 2^0
  [1]: 2     // 2^1
  [2]: 4     // 2^2
  ...
  [15]: -32768 // 2^15
```

Test Cases (MathTest):
```jack
let r[0] = 2 * 3;                  // Basic multiplication
let r[1] = r[0] * (-30);          // Negative numbers
let r[6] = (-18000) / 6;          // Large negative division
let r[7] = 32766 / (-32767);      // Edge case division
```

Results:
```
RAM[8000] = 6        // 2 * 3
RAM[8001] = -180     // 6 * (-30)
RAM[8002] = -18000   // (-180) * 100
RAM[8006] = -3000    // (-18000) / 6
RAM[8007] = 0        // 32766 / (-32767)
```

### 2. Memory
Overview:
- Manages heap memory (2048-16383)
- Implements first-fit allocation
- Maintains free block linked list
- Provides direct RAM access
- Handles block splitting and merging

Key Implementation:
```jack
class Memory {
    static Array ram;
    static Array freeList;
    static int heapBase, heapEnd;

    function void init() {
        let ram = 0;
        let heapBase = 2048;
        let heapEnd = 16384;
        let freeList = heapBase;
        let ram[heapBase] = heapEnd - heapBase - 2;
        let ram[heapBase + 1] = 0;
    }

    function int alloc(int size) {
        var Array block;
        // First-fit algorithm
        while (block != null) {
            if (block.size >= size + 2) {
                // Split block if needed
                return block + 2;
            }
        }
    }
}
```

Memory Layout:
```
Free block structure:
[size][next][data...]
 ^     ^     ^
 |     |     +-- User data starts here
 |     +-- Points to next free block
 +-- Block size (including header)

Example state:
[2048]: 14334  // Initial block size
[2049]: 0      // No next block

After allocation:
[2048]: 7      // Allocated block (size 5 + 2)
[2049]: data   // User data starts
[2055]: 14327  // Remaining free block
[2056]: 0      // Next pointer
```

Test Cases:
```jack
let block = Memory.alloc(5);   // Allocate 5 words
do Memory.poke(8000, 333);     // Direct memory access
let value = Memory.peek(8000); // Read memory
do Memory.deAlloc(block);      // Free memory
```

Results:
```
Initial heap: [2048] = 14334, [2049] = 0
After alloc:  [2048] = 7, [2055] = 14327
After poke:   [8000] = 333
After peek:   value = 333
After deAlloc: [2048] = 14334, [2049] = 0
```

### 3. Array
Overview:
- Provides dynamic array allocation
- Integrates with Memory manager
- Supports array disposal
- Enables multi-dimensional arrays
- Handles array bounds checking

Key Implementation:
```jack
class Array {
    function Array new(int size) {
        if (size < 0) {
            do Sys.error(2);
            return null;
        }
        return Memory.alloc(size);
    }

    method void dispose() {
        do Memory.deAlloc(this);
        return;
    }
}
```

Memory Layout:
```
Single array:
[base]: size    // Block size (header)
[base+1]: next  // Next block pointer
[base+2...]: data  // Array elements

2D array example:
[base+2]: ptr1  // Points to first row
[base+3]: ptr2  // Points to second row
[ptr1]: data    // First row data
[ptr2]: data    // Second row data
```

Test Cases:
```jack
// From ArrayTest
let arr = Array.new(3);
let arr[0] = 42;
let arr[1] = arr[0] * 2;
do arr.dispose();
```

Results:
```
After new(3):
[2048]: 5     // Size (3 + 2 header words)
[2049]: null  // Next block
[2050]: 42    // arr[0]
[2051]: 84    // arr[1]
[2052]: 0     // arr[2]
```

### 4. String
Overview:
- Implements variable-length string handling
- Provides character-level manipulation
- Supports string-integer conversion
- Manages dynamic string length
- Handles string bounds checking

Key Implementation:
```jack
class String {
    field Array str;      // Character array
    field int length;     // Current length
    field int maxLength;  // Maximum length

    constructor String new(int maxLen) {
        if (maxLen < 0) {
            do Sys.error(14);
            return null;
        }
        let maxLength = maxLen;
        let length = 0;
        if (maxLen > 0) {
            let str = Array.new(maxLen);
        }
        return this;
    }

    method void appendChar(char c) {
        if (length = maxLength) {
            do Sys.error(17);
        }
        let str[length] = c;
        let length = length + 1;
        return;
    }

    method int intValue() {
        var int val, i, d;
        var boolean neg;
        
        let val = 0;
        let i = 0;
        let neg = false;
        
        if ((length > 0) & (str[0] = 45)) {  // Check for '-'
            let neg = true;
            let i = 1;
        }
        
        while (i < length) {
            let d = str[i] - 48;  // Convert ASCII to integer
            if ((d < 0) | (d > 9)) { break; }
            let val = (val * 10) + d;
            let i = i + 1;
        }
        return neg ? -val : val;
    }
}
```

Memory Layout:
```
String object structure:
[base]: length     // Current string length
[base+1]: maxLen   // Maximum allowed length
[base+2]: ptr      // Points to character array

Example for "Hello":
[heap]: String object
  [0]: 5           // length
  [1]: 10          // maxLength
  [2]: ptr         // Points to char array
[ptr]: 72          // 'H'
[ptr+1]: 101       // 'e'
[ptr+2]: 108       // 'l'
[ptr+3]: 108       // 'l'
[ptr+4]: 111       // 'o'
```

Test Cases (from StringTest):
```jack
// String creation and manipulation
let s = String.new(6);
do s.appendChar(72);   // 'H'
do s.appendChar(105);  // 'i'
do s.appendChar(33);   // '!'

// Number conversion
let s = String.new(5);
do s.setInt(-123);     // Convert number to string
let val = s.intValue() // Convert back to number
```

Results:
```
String "Hi!":
length = 3
maxLength = 6
str = [72, 105, 33]

Number conversion:
"-123" -> -123
"12345" -> 12345
"0" -> 0
"-32767" -> -32767
```

Error Cases:
```
appendChar on full string: Error 17
new with negative length: Error 14
setCharAt out of bounds: Error 16
eraseLastChar on empty: Error 18
```

### 5. Screen
Overview:
- Manages 256x512 pixel black and white display
- Uses word-aligned memory access for efficiency
- Provides primitive and complex drawing operations
- Maps directly to memory (16384-24575)
- Implements Bresenham's line algorithm

Key Implementation:
```jack
class Screen {
    static boolean color;    // Current drawing color
    static Array screen;     // Screen memory map
    static Array twoToThe;   // Powers of 2 for bit operations

    function void init() {
        let screen = 16384;  // Base address of screen memory
        let color = true;    // Default color is black
        return;
    }

    function void drawPixel(int x, int y) {
        var int address, mask;
        
        if ((x < 0) | (x > 511) | (y < 0) | (y > 255)) {
            do Sys.error(7);
        }
        
        let address = (y * 32) + (x / 16);  // Word-aligned address
        let mask = twoToThe[x & 15];        // Bit position in word
        
        if (color) {
            let screen[address] = screen[address] | mask;    // Set bit
        } else {
            let screen[address] = screen[address] & ~mask;   // Clear bit
        }
        return;
    }

    function void drawLine(int x1, int y1, int x2, int y2) {
        var int dx, dy, diff;
        let dx = x2 - x1;
        let dy = y2 - y1;
        let diff = 0;
        
        while ((~(x1 > x2)) & (~(y1 > y2))) {
            do Screen.drawPixel(x1, y1);
            if (diff < 0) {
                let x1 = x1 + 1;
                let diff = diff + dy;
            } else {
                let y1 = y1 + 1;
                let diff = diff - dx;
            }
        }
        return;
    }
}
```

Memory Layout:
```
Screen memory map (16384-24575):
[16384]: First 16 pixels of row 0
[16385]: Next 16 pixels of row 0
...
[16416]: First 16 pixels of row 1
...

Bit mapping example:
Word at 16384: 0000000000000001  // Pixel (0,0) set
Word at 16385: 0000000000000010  // Pixel (17,0) set
```

Test Cases:
```jack
// Basic drawing operations
do Screen.setColor(true);              // Set black
do Screen.drawPixel(100, 100);        // Single pixel
do Screen.drawLine(0, 0, 100, 100);   // Diagonal line
do Screen.drawRectangle(50, 50, 100, 100); // Rectangle

// Complex shape
do Screen.drawCircle(150, 150, 50);   // Circle
```

Results:
```
After drawPixel(2,0):
[16384] = 4      // Binary: 0000000000000100

After horizontal line at y=0:
[16384] = -1     // Binary: 1111111111111111
[16385] = -1     // All bits set in word

After vertical line at x=0:
[16384] = 1      // First pixel in first word
[16416] = 1      // First pixel in second row
[16448] = 1      // First pixel in third row
```

### 6. Output
Overview:
- Manages 23x64 character display
- Implements bitmap font rendering
- Handles cursor positioning and wrapping
- Supports string and integer output
- Manages screen scrolling

Key Implementation:
```jack
class Output {
    static Array screen;     // Screen memory map
    static Array charMaps;   // Character bitmap data
    static int cursorX, cursorY;  // Cursor position

    function void moveCursor(int i, int j) {
        if ((i < 0) | (i > 22) | (j < 0) | (j > 63)) {
            do Sys.error(20);
        }
        let cursorX = j;
        let cursorY = i;
        return;
    }

    function void printChar(char c) {
        var Array map;
        var int addr;
        
        if (c = String.newLine()) {
            do Output.println();
            return;
        }
        
        let map = Output.getMap(c);
        let addr = Output.getCursorAddr();
        
        // Draw character bitmap (11 rows)
        do Output.drawChar(addr, map);
        do Output.moveCursor(cursorY, cursorX + 1);
        return;
    }
}
```

Memory Layout:
```
Screen organization:
23 rows x 64 columns of characters
Each character: 8x11 pixels

Character bitmap:
[0]: 0  // First row of character
[1]: 60 // Second row (e.g., 00111100)
...
[10]: 0 // Last row

Screen memory for character at (0,0):
[16384]: First row of pixels
[16416]: Second row (32 words per row)
...
[16704]: Last row
```

Test Cases:
```jack
// Basic output
do Output.moveCursor(0, 0);
do Output.printChar(65);     // Print 'A'
do Output.printString("Hi"); // Print string
do Output.println();        // New line
do Output.printInt(12345);  // Print number
```

Results:
```
Cursor movement:
(0,0) -> (0,1) -> (0,2) -> (1,0)

Screen memory after 'A':
[16384] = 384   // 0000000110000000
[16416] = 576   // 0000001001000000
[16448] = 1056  // 0000010000100000
[16480] = 960   // 0000001111000000
```

### 7. Keyboard
Overview:
- Provides keyboard input handling
- Implements blocking and non-blocking reads
- Supports line and integer input
- Handles special keys (newline, backspace)
- Maps directly to memory location 24576

Key Implementation:
```jack
class Keyboard {
    static Array keyboard;

    function void init() {
        let keyboard = 24576;  // Memory map location
        return;
    }

    function char keyPressed() {
        return keyboard[0];  // Non-blocking read
    }

    function String readLine(String message) {
        var String s;
        var char c;
        
        do Output.printString(message);
        let s = String.new(50);
        
        while (true) {
            let c = Keyboard.readChar();  // Blocking read
            if (c = String.newLine()) { return s; }
            if (c = String.backSpace()) {
                do s.eraseLastChar();
            } else {
                do s.appendChar(c);
            }
        }
        return s;
    }

    function int readInt(String message) {
        var String s;
        let s = Keyboard.readLine(message);
        return s.intValue();
    }
}
```

Memory Layout:
```
Keyboard memory map:
[24576]: Current key value
  0: No key pressed
  65-90: 'A' to 'Z'
  48-57: '0' to '9'
  128: newline
  129: backspace
  130: left arrow
  131: up arrow
  132: right arrow
  133: down arrow
```

Test Cases:
```jack
// Non-blocking key detection
let key = Keyboard.keyPressed();

// Line input with prompt
let name = Keyboard.readLine("Enter name: ");

// Integer input with validation
let age = Keyboard.readInt("Enter age: ");
```

Results:
```
Key press sequence:
[24576] = 0    // Initial state
[24576] = 72   // 'H' pressed
[24576] = 0    // Key released
[24576] = 73   // 'I' pressed
[24576] = 0    // Key released
[24576] = 128  // Enter pressed
Result: "HI"

Integer input "123":
[24576] = 49   // '1' pressed
[24576] = 50   // '2' pressed
[24576] = 51   // '3' pressed
[24576] = 128  // Enter pressed
Result: 123
```

### 8. Sys
Overview:
- Coordinates OS initialization sequence
- Provides system-level services
- Handles error reporting
- Implements timing functions
- Controls program execution

Key Implementation:
```jack
class Sys {
    function void init() {
        do Memory.init();   // Initialize heap
        do Math.init();     // Setup math tables
        do Screen.init();   // Clear screen
        do Output.init();   // Setup character maps
        do Keyboard.init(); // Setup keyboard
        do Main.main();     // Start user program
        do Sys.halt();      // Stop execution
        return;
    }

    function void halt() {
        while (true) {}  // Infinite loop
        return;
    }

    function void wait(int duration) {
        var int i, j;
        
        if (duration < 0) {
            do Sys.error(1);
        }
        
        while (i < duration) {  // Approximate milliseconds
            let j = 0;
            while (j < 200) {   // Calibrated delay
                let j = j + 1;
            }
            let i = i + 1;
        }
        return;
    }

    function void error(int errorCode) {
        do Output.printString("ERR");
        do Output.printInt(errorCode);
        do Sys.halt();
        return;
    }
}
```

Memory Layout:
```
System initialization state:
[2048-16383]: Heap memory
[16384-24575]: Screen memory
[24576]: Keyboard memory

Error display at:
Screen position (0,0): "ERR"
Screen position (0,3): error code
```

Test Cases:
```jack
// System initialization
do Sys.init();  // Full OS startup

// Timing control
do Sys.wait(1000);  // Wait 1 second

// Error handling
do Sys.error(3);    // Display "ERR3" and halt
```

Results:
```
Initialization sequence:
1. Memory.init()  // RAM[2048] = 14334
2. Math.init()    // powersOfTwo array setup
3. Screen.init()  // Screen cleared
4. Output.init()  // Cursor at (0,0)
5. Keyboard.init()// Ready for input
6. Main.main()    // User program starts

Error display:
Screen shows "ERR3" at (0,0)
System halts execution
```

## Error Codes
| Code | Description              |
|------|-------------------------|
| 1    | VM error               |
| 2    | Array allocation error |
| 3    | Division by zero       |
| 4    | Math error             |
| 5    | Memory allocation error|
| 6    | Heap overflow          |
| 7    | Illegal pixel coords   |
| 8    | Font error             |

## Testing
Test with provided test programs:
- ArrayTest: Array allocation/access
- MathTest: Mathematical operations
- MemoryTest: Memory management
- StringTest: String manipulation

## Known Limitations
- Fixed memory segment sizes
- No garbage collection
- Limited error recovery
- No memory defragmentation

## Resources
- [nand2tetris Course](https://www.nand2tetris.org)
- [Jack OS API](https://www.nand2tetris.org/project12)
- [Hardware Platform](https://www.nand2tetris.org/project05) 