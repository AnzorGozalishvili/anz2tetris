# Boolean Arithmetic

Implementation of arithmetic chips using the basic logic gates from Project 1, culminating in the construction of an Arithmetic Logic Unit (ALU).

## Chip Specifications

### Half Adder
| Inputs | Outputs | Description                    |
|--------|---------|--------------------------------|
| a      | sum     | Least significant bit of a+b   |
| b      | carry   | Most significant bit of a+b    |

### Full Adder
| Inputs | Outputs | Description                    |
|--------|---------|--------------------------------|
| a      | sum     | Least significant bit          |
| b      | carry   | Carry bit                      |
| c      |         | Input carry                    |

### Add16
| Inputs  | Outputs | Description                    |
|---------|---------|--------------------------------|
| a[16]   | out[16] | 16-bit integer addition       |
| b[16]   |         | Overflow is ignored           |

### Inc16
| Inputs  | Outputs | Description                    |
|---------|---------|--------------------------------|
| in[16]  | out[16] | 16-bit increment              |

### ALU
| Inputs   | Outputs  | Description                   |
|----------|----------|-------------------------------|
| x[16]    | out[16]  | 16-bit output                |
| y[16]    | zr       | True if out=0                 |
| zx       | ng       | True if out<0                 |
| nx       |          | Zero/negate input x           |
| zy       |          | Zero/negate input y           |
| ny       |          | Computation control bits      |
| f        |          | Function select               |
| no       |          | Negate output                 |

## Implementation Examples

### Half Adder
```hdl
CHIP HalfAdder {
    IN a, b;
    OUT sum, carry;

    PARTS:
    Xor(a=a, b=b, out=sum);
    And(a=a, b=b, out=carry);
}
```

### Full Adder
```hdl
CHIP FullAdder {
    IN a, b, c;
    OUT sum, carry;

    PARTS:
    HalfAdder(a=a, b=b, sum=sumab, carry=carryab);
    HalfAdder(a=sumab, b=c, sum=sum, carry=carrybc);
    Or(a=carryab, b=carrybc, out=carry);
}
```

### ALU
```hdl
CHIP ALU {
    IN  x[16], y[16],
        zx, // zero the x input
        nx, // negate the x input
        zy, // zero the y input
        ny, // negate the y input
        f,  // compute out = x + y (if 1) or x & y (if 0)
        no; // negate the out output
    OUT out[16],
        zr, // 1 if out=0, 0 otherwise
        ng; // 1 if out<0, 0 otherwise

    PARTS:
    // Zero inputs
    Mux16(a=x, b=false, sel=zx, out=x1);
    Mux16(a=y, b=false, sel=zy, out=y1);
    
    // Negate inputs
    Not16(in=x1, out=notx);
    Not16(in=y1, out=noty);
    Mux16(a=x1, b=notx, sel=nx, out=x2);
    Mux16(a=y1, b=noty, sel=ny, out=y2);
    
    // Compute function
    And16(a=x2, b=y2, out=andxy);
    Add16(a=x2, b=y2, out=addxy);
    Mux16(a=andxy, b=addxy, sel=f, out=fxy);
    
    // Negate output
    Not16(in=fxy, out=nfxy);
    Mux16(a=fxy, b=nfxy, sel=no, out=out);
}
```

## Test Cases

### Adder Tests
```
// HalfAdder
|   a   |   b   |  sum  | carry |
|   0   |   0   |   0   |   0   |
|   0   |   1   |   1   |   0   |
|   1   |   0   |   1   |   0   |
|   1   |   1   |   0   |   1   |

// Add16
|        a         |        b         |       out        |
| 0000000000000000 | 0000000000000000 | 0000000000000000 |
| 0000000000000000 | 1111111111111111 | 1111111111111111 |
| 1111111111111111 | 1111111111111111 | 1111111111111110 |
| 1010101010101010 | 0101010101010101 | 1111111111111111 |
```

### ALU Tests
```
// Basic operations
| x | y | zx | nx | zy | ny | f | no | out | zr | ng |
| 0 | 1 | 1  | 0  | 1  | 0  | 1 | 0  | 0   | 1  | 0  | // 0
| 0 | 1 | 1  | 1  | 1  | 1  | 1 | 1  | 1   | 0  | 0  | // 1
| 0 | 1 | 1  | 1  | 1  | 0  | 1 | 0  | -1  | 0  | 1  | // -1
| 2 | 3 | 0  | 0  | 1  | 1  | 0 | 0  | 2   | 0  | 0  | // x
| 2 | 3 | 1  | 1  | 0  | 0  | 0 | 0  | 3   | 0  | 0  | // y
```

## Project Structure
```
project2/
├── HalfAdder.hdl
├── FullAdder.hdl
├── Add16.hdl
├── Inc16.hdl
└── ALU.hdl
```

## Testing Instructions
1. Open Hardware Simulator
2. Load chip file (.hdl)
3. Load test script (.tst)
4. Run test script
5. Compare output with .cmp file

## Common Issues
- Carry propagation in multi-bit addition
- ALU control bit combinations
- Two's complement representation
- Handling negative numbers
- Zero and negative flags in ALU

## ALU Function Table
| zx | nx | zy | ny | f | no | Function     |
|----|----|----|----|----|----| ------------|
| 1  | 0  | 1  | 0  | 1 | 0  | 0           |
| 1  | 1  | 1  | 1  | 1 | 1  | 1           |
| 1  | 1  | 1  | 0  | 1 | 0  | -1          |
| 0  | 0  | 1  | 1  | 0 | 0  | x           |
| 1  | 1  | 0  | 0  | 0 | 0  | y           |
| 0  | 0  | 1  | 1  | 0 | 1  | !x          |
| 1  | 1  | 0  | 0  | 0 | 1  | !y          |
| 0  | 0  | 1  | 1  | 1 | 1  | -x          |
| 1  | 1  | 0  | 0  | 1 | 1  | -y          |
| 0  | 1  | 1  | 1  | 1 | 1  | x + 1       |
| 1  | 1  | 0  | 1  | 1 | 1  | y + 1       |
| 0  | 0  | 1  | 1  | 1 | 0  | x - 1       |
| 1  | 1  | 0  | 0  | 1 | 0  | y - 1       |
| 0  | 0  | 0  | 0  | 1 | 0  | x + y       |
| 0  | 1  | 0  | 0  | 1 | 1  | x - y       |
| 0  | 0  | 0  | 1  | 1 | 1  | y - x       |
| 0  | 0  | 0  | 0  | 0 | 0  | x & y       |
| 0  | 1  | 0  | 1  | 0 | 1  | x | y       |

## Resources
- [nand2tetris Course](https://www.nand2tetris.org)
- [Boolean Arithmetic](https://www.nand2tetris.org/project02)
- [Hardware Simulator Tutorial](https://www.nand2tetris.org/software) 