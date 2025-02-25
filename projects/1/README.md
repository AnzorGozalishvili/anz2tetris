# Boolean Logic

Implementation of fundamental logic gates using the NAND gate as the basic building block.

## Gate Specifications

### Basic Gates
| Gate    | Inputs | Output | Description                    |
|---------|--------|--------|--------------------------------|
| Not     | 1      | 1      | Inverts input                  |
| And     | 2      | 1      | True if both inputs true       |
| Or      | 2      | 1      | True if any input true         |
| Xor     | 2      | 1      | True if inputs are different   |
| Mux     | 3      | 1      | Selects between two inputs     |
| DMux    | 2      | 2      | Distributes input to two outputs|

### Multi-Bit Gates
| Gate      | Inputs  | Output | Description                  |
|-----------|---------|--------|------------------------------|
| Not16     | 16      | 16     | 16-bit Not                  |
| And16     | 2x16    | 16     | 16-bit And                  |
| Or16      | 2x16    | 16     | 16-bit Or                   |
| Mux16     | 3x16    | 16     | 16-bit multiplexor          |

### Multi-Way Gates
| Gate      | Inputs  | Output | Description                  |
|-----------|---------|--------|------------------------------|
| Or8Way    | 8       | 1      | 8-way Or                    |
| Mux4Way16 | 4x16    | 16     | 4-way 16-bit multiplexor    |
| Mux8Way16 | 8x16    | 16     | 8-way 16-bit multiplexor    |
| DMux4Way  | 3       | 4      | 4-way demultiplexor         |
| DMux8Way  | 4       | 8      | 8-way demultiplexor         |

## Implementation Examples

### Not Gate
```hdl
CHIP Not {
    IN in;
    OUT out;

    PARTS:
    NAND(a=in, b=in, out=out);
}
```

### And Gate
```hdl
CHIP And {
    IN a, b;
    OUT out;

    PARTS:
    NAND(a=a, b=b, out=nandout);
    Not(in=nandout, out=out);
}
```

### Mux Gate
```hdl
CHIP Mux {
    IN a, b, sel;
    OUT out;

    PARTS:
    Not(in=sel, out=notsel);
    And(a=a, b=notsel, out=aAndNotsel);
    And(a=b, b=sel, out=bAndSel);
    Or(a=aAndNotSel, b=bAndSel, out=out);
}
```

## Test Cases

### Basic Gate Tests
```
// Not gate
|  in   |  out  |
|   0   |   1   |
|   1   |   0   |

// And gate
|   a   |   b   |  out  |
|   0   |   0   |   0   |
|   0   |   1   |   0   |
|   1   |   0   |   0   |
|   1   |   1   |   1   |

// Mux gate
|   a   |   b   |  sel  |  out  |
|   0   |   0   |   0   |   0   |
|   0   |   1   |   0   |   0   |
|   1   |   0   |   0   |   1   |
|   1   |   1   |   0   |   1   |
|   0   |   0   |   1   |   0   |
|   0   |   1   |   1   |   1   |
|   1   |   0   |   1   |   0   |
|   1   |   1   |   1   |   1   |
```

### Multi-Bit Tests
```
// Not16
|        in        |       out        |
| 0000000000000000 | 1111111111111111 |
| 1111111111111111 | 0000000000000000 |
| 1010101010101010 | 0101010101010101 |

// Mux16
|        a         |        b         | sel |       out        |
| 0000000000000000 | 0000000000000000 |  0  | 0000000000000000 |
| 0000000000000000 | 0000000000000000 |  1  | 0000000000000000 |
| 0000000000000000 | 0001001000110100 |  0  | 0000000000000000 |
| 0000000000000000 | 0001001000110100 |  1  | 0001001000110100 |
```

## Project Structure
```
project1/
├── And.hdl
├── And16.hdl
├── DMux.hdl
├── DMux4Way.hdl
├── DMux8Way.hdl
├── Mux.hdl
├── Mux16.hdl
├── Mux4Way16.hdl
├── Mux8Way16.hdl
├── Not.hdl
├── Not16.hdl
├── Or.hdl
├── Or16.hdl
└── Or8Way.hdl
```

## Testing Instructions
1. Open Hardware Simulator
2. Load chip file (.hdl)
3. Load test script (.tst)
4. Run test script
5. Compare output with .cmp file

## Common Issues
- NAND gate connections must be precise
- Multi-bit buses require correct indexing
- Gate naming must match specification exactly
- Input/output pin counts must match spec

## Resources
- [nand2tetris Course](https://www.nand2tetris.org)
- [Boolean Algebra](https://www.nand2tetris.org/project01)
- [Hardware Simulator Tutorial](https://www.nand2tetris.org/software) 