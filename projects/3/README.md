# Sequential Logic

Implementation of sequential chips using D Flip-Flops, including registers, memory units, and a program counter.

## Chip Specifications

### DFF (Data Flip-Flop)
| Inputs | Outputs | Description                    |
|--------|---------|--------------------------------|
| in     | out     | Outputs previous input         |
|        |         | Updates on clock edge          |

### Bit
| Inputs | Outputs | Description                    |
|--------|---------|--------------------------------|
| in     | out     | 1-bit register                 |
| load   |         | Write control                  |

### Register
| Inputs  | Outputs | Description                    |
|---------|---------|--------------------------------|
| in[16]  | out[16] | 16-bit register               |
| load    |         | Write control                  |

### RAM8
| Inputs  | Outputs | Description                    |
|---------|---------|--------------------------------|
| in[16]  | out[16] | 8-register memory             |
| load    |         | Write control                  |
| address[3] |      | Register selection            |

### RAM64
| Inputs  | Outputs | Description                    |
|---------|---------|--------------------------------|
| in[16]  | out[16] | 64-register memory            |
| load    |         | Write control                  |
| address[6] |      | Register selection            |

### PC (Program Counter)
| Inputs  | Outputs | Description                    |
|---------|---------|--------------------------------|
| in[16]  | out[16] | Counter value                  |
| load    |         | Load new value                 |
| inc     |         | Increment counter              |
| reset   |         | Reset to zero                  |

## Implementation Examples

### Bit
```hdl
CHIP Bit {
    IN in, load;
    OUT out;

    PARTS:
    Mux(a=dffout, b=in, sel=load, out=muxout);
    DFF(in=muxout, out=dffout);
    Or(a=dffout, b=dffout, out=out);  // Non-looping feedback
}
```

### Register
```hdl
CHIP Register {
    IN in[16], load;
    OUT out[16];

    PARTS:
    Bit(in=in[0], load=load, out=out[0]);
    Bit(in=in[1], load=load, out=out[1]);
    // ... repeat for all 16 bits
    Bit(in=in[15], load=load, out=out[15]);
}
```

### RAM8
```hdl
CHIP RAM8 {
    IN in[16], load, address[3];
    OUT out[16];

    PARTS:
    DMux8Way(in=load, sel=address,
        a=load0, b=load1, c=load2, d=load3,
        e=load4, f=load5, g=load6, h=load7);

    Register(in=in, load=load0, out=reg0);
    Register(in=in, load=load1, out=reg1);
    // ... repeat for all 8 registers
    Register(in=in, load=load7, out=reg7);

    Mux8Way16(
        a=reg0, b=reg1, c=reg2, d=reg3,
        e=reg4, f=reg5, g=reg6, h=reg7,
        sel=address, out=out);
}
```

## Test Cases

### Register Tests
```
// Basic register operation
| time | in  | load | out |
| 0+   | 0   | 0    | 0   |
| 1    | 0   | 0    | 0   |
| 1+   | -32123 | 1 | 0   |
| 2    | -32123 | 1 | -32123 |
| 2+   | 11111 | 0  | -32123 |
| 3    | 11111 | 0  | -32123 |
```

### RAM Tests
```
// RAM8 operation
| time | in  | load | address | out |
| 0+   | 0   | 0    | 0       | 0   |
| 1    | 11  | 1    | 0       | 0   |
| 1+   | 11  | 1    | 0       | 11  |
| 2    | 22  | 1    | 1       | 11  |
| 2+   | 22  | 1    | 1       | 22  |
```

### PC Tests
```
// Program counter operations
| time | in  | reset | load | inc | out |
| 0+   | 0   | 0     | 0    | 0   | 0   |
| 1    | 0   | 0     | 0    | 1   | 0   |
| 1+   | 0   | 0     | 0    | 1   | 1   |
| 2    | -32123 | 0  | 1    | 1   | 1   |
| 2+   | -32123 | 0  | 1    | 1   | -32123 |
```

## Project Structure
```
project3/
├── Bit.hdl
├── Register.hdl
├── RAM8.hdl
├── RAM64.hdl
├── RAM512.hdl
├── RAM4K.hdl
├── RAM16K.hdl
└── PC.hdl
```

## Testing Instructions
1. Open Hardware Simulator
2. Load chip file (.hdl)
3. Load test script (.tst)
4. Run test script
5. Compare output with .cmp file

## Common Issues
- DFF feedback loops
- Register load timing
- RAM addressing logic
- PC control priority
- Clock edge synchronization

## Memory Hierarchy
```
Memory Organization:
RAM16K
  └── 4 RAM4K units
       └── 8 RAM512 units
            └── 8 RAM64 units
                 └── 8 RAM8 units
                      └── 8 Registers
                           └── 16 Bits
                                └── DFF
```

## PC Control Priority
1. reset (highest)
2. load
3. inc (lowest)

## Resources
- [nand2tetris Course](https://www.nand2tetris.org)
- [Sequential Logic](https://www.nand2tetris.org/project03)
- [Hardware Simulator Tutorial](https://www.nand2tetris.org/software) 