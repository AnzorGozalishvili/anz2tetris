# Computer Architecture

Implementation of the Hack computer platform, including CPU, Memory, and Computer chips, completing the hardware hierarchy of the nand2tetris computer system.

## Chip Specifications

### Memory
| Inputs     | Outputs | Description                    |
|------------|---------|--------------------------------|
| in[16]     | out[16] | Memory value at address       |
| load       |         | Write enable                   |
| address[15]|         | Memory address                 |

### CPU
| Inputs     | Outputs   | Description                  |
|------------|-----------|------------------------------|
| inM[16]    | outM[16]  | M value output              |
| instruction[16] | writeM | Memory write flag          |
| reset      | addressM[15] | Memory address           |
|            | pc[15]    | Program counter             |

### Computer
| Inputs  | Outputs | Description                    |
|---------|---------|--------------------------------|
| reset   | -       | Reset signal                   |

## Memory Map
```
Address Space:
0-16383     (0x0000-0x3FFF): Data Memory (RAM)
16384-24575 (0x4000-0x5FFF): Screen Memory Map
24576       (0x6000):        Keyboard Memory Map
32768-65535 (0x8000-0xFFFF): Instruction Memory (ROM)
```

## Implementation Examples

### CPU
```hdl
CHIP CPU {
    IN  inM[16],         // M value input
        instruction[16], // Instruction for execution
        reset;          // Reset signal
    OUT outM[16],       // M value output
        writeM,         // Write to M? 
        addressM[15],   // Address in data memory
        pc[15];         // Program counter

    PARTS:
    // Decode instruction
    // A-instruction: @value
    // C-instruction: dest=comp;jump
    
    // ALU control and computation
    ALU(x=xIn, y=yIn,
        zx=instruction[11],
        nx=instruction[10],
        zy=instruction[9],
        ny=instruction[8],
        f=instruction[7],
        no=instruction[6],
        out=aluOut,
        zr=zeroOut,
        ng=negOut);

    // Program counter logic
    PC(in=aRegOut,
       load=pcLoad,
       inc=true,
       reset=reset,
       out[0..14]=pc);
}
```

### Memory
```hdl
CHIP Memory {
    IN in[16], load, address[15];
    OUT out[16];

    PARTS:
    // Memory address space demux
    DMux4Way(in=load, sel=address[13..14],
            a=ramLoad, b=ramLoad,
            c=screenLoad, d=kbdLoad);

    // RAM16K for data memory
    RAM16K(in=in, load=ramLoad,
           address=address[0..13], out=ramOut);

    // Screen memory mapping
    Screen(in=in, load=screenLoad,
           address=address[0..12], out=screenOut);

    // Keyboard memory mapping
    Keyboard(out=kbdOut);

    // Output multiplexing
    Mux4Way16(a=ramOut, b=ramOut,
              c=screenOut, d=kbdOut,
              sel=address[13..14], out=out);
}
```

## Test Cases

### CPU Tests
```
// Test A-instruction
| time | inM  | instruction | reset | outM | writeM | addressM | pc  |
| 0    | 0    | 0000000000000010 | 0     | 0    | 0      | 0       | 0   |
| 1    | 0    | 0000000000000010 | 0     | 0    | 0      | 2       | 1   |

// Test C-instruction
| 0    | 9    | 1111110000010000 | 0     | 0    | 0      | 0       | 0   |
| 1    | 9    | 1111110000010000 | 0     | 9    | 0      | 0       | 1   |
```

### Memory Tests
```
// RAM access
| time | in   | load | address | out |
| 0    | 0    | 0    | 0       | 0   |
| 1    | 4444 | 1    | 0       | 0   |
| 2    | 4444 | 0    | 0       | 4444|

// Screen access
| 0    | -1   | 1    | 16384   | 0   |
| 1    | -1   | 0    | 16384   | -1  |
```

## Project Structure
```
project5/
├── CPU.hdl
├── Memory.hdl
└── Computer.hdl
```

## Testing Instructions
1. Open Hardware Simulator
2. Load chip file (.hdl)
3. Load test script (.tst)
4. Run script
5. Compare with .cmp file

## Common Issues
- Instruction decoding logic
- ALU control signals
- Program counter updates
- Memory address space mapping
- Reset signal handling

## CPU Instruction Format

### A-instruction (16 bits)
```
0vvvvvvvvvvvvvvv
│└───────────────┘
│      value
└ opcode (0)
```

### C-instruction (16 bits)
```
111a cccc ccdd djjj
│││└─────┘│└──┘│└─┘
│││  comp │dest│jump
││└ a-bit
│└─ unused
└── opcode (1)
```

## Control Signals
| Signal | Description           |
|--------|-----------------------|
| writeM | Write to memory      |
| loadA  | Load A register      |
| loadD  | Load D register      |
| pcLoad | Load program counter |
| pcInc  | Increment PC         |

## Resources
- [nand2tetris Course](https://www.nand2tetris.org)
- [Computer Architecture](https://www.nand2tetris.org/project05)
- [Hardware Simulator Tutorial](https://www.nand2tetris.org/software) 