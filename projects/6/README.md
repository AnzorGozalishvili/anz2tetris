# Assembler

Implementation of an assembler that translates Hack assembly programs into binary code that can be executed on the Hack hardware platform.

## Assembler Specifications

### Input Format
- Assembly language (.asm) files
- One instruction per line
- Comments start with //
- Whitespace is ignored
- Labels enclosed in parentheses
- Variables start with letter/underscore

### Output Format
- Binary code (.hack) files
- 16-bit instructions per line
- No whitespace or comments
- A-instructions: 0vvvvvvvvvvvvvvv
- C-instructions: 111accccccdddjjj

## Instruction Translation

### A-Instructions
| Assembly | Binary | Description            |
|----------|--------|------------------------|
| @value   | 0xxx   | Decimal or symbol     |
| @symbol  | 0xxx   | Predefined or variable|
| @R0      | 0000   | Register 0            |
| @SCREEN  | 16384  | Screen memory map     |

### C-Instructions
| Assembly   | Binary | Description          |
|------------|--------|----------------------|
| dest=comp  | 111... | Computation         |
| comp;jump  | 111... | Conditional jump    |
| 0;JMP      | 111... | Unconditional jump  |

## Implementation Examples

### Symbol Table
```python
class SymbolTable:
    def __init__(self):
        self.table = {
            'SP': 0, 'LCL': 1, 'ARG': 2,
            'THIS': 3, 'THAT': 4,
            'R0': 0, 'R1': 1, ..., 'R15': 15,
            'SCREEN': 16384, 'KBD': 24576
        }
        self.next_variable = 16

    def add_entry(self, symbol, address):
        self.table[symbol] = address

    def contains(self, symbol):
        return symbol in self.table

    def get_address(self, symbol):
        return self.table[symbol]
```

### Parser
```python
class Parser:
    def __init__(self, input_file):
        self.commands = []
        self.current = -1
        
        # Remove comments and whitespace
        for line in input_file:
            line = line.split('//')[0].strip()
            if line:
                self.commands.append(line)

    def has_more_commands(self):
        return self.current < len(self.commands) - 1

    def advance(self):
        self.current += 1
        return self.commands[self.current]

    def command_type(self):
        if self.commands[self.current].startswith('@'):
            return 'A_COMMAND'
        elif self.commands[self.current].startswith('('):
            return 'L_COMMAND'
        else:
            return 'C_COMMAND'
```

### Code Generator
```python
class Code:
    def __init__(self):
        self.comp_table = {
            '0': '0101010', '1': '0111111',
            'D': '0001100', 'A': '0110000',
            'M': '1110000', '-1': '0111010',
            # ... more computation codes
        }
        self.dest_table = {
            '': '000', 'M': '001', 'D': '010',
            'MD': '011', 'A': '100', 'AM': '101',
            'AD': '110', 'AMD': '111'
        }
        self.jump_table = {
            '': '000', 'JGT': '001', 'JEQ': '010',
            'JGE': '011', 'JLT': '100', 'JNE': '101',
            'JLE': '110', 'JMP': '111'
        }

    def generate(self, command):
        if command.startswith('@'):
            return self.gen_a_instruction(command[1:])
        else:
            return self.gen_c_instruction(command)
```

## Test Cases

### Basic Instructions
```
// Input: Add.asm
@2
D=A
@3
D=D+A
@0
M=D

// Output: Add.hack
0000000000000010
1110110000010000
0000000000000011
1110000010010000
0000000000000000
1110001100001000
```

### Variables and Labels
```
// Input: Max.asm
   @R0
   D=M
   @R1
   D=D-M
   @OUTPUT_FIRST
   D;JGT
   @R1
   D=M
   @OUTPUT_D
   0;JMP
(OUTPUT_FIRST)
   @R0
   D=M
(OUTPUT_D)
   @R2
   M=D

// Output: Max.hack
0000000000000000
1111110000010000
0000000000000001
1111010011010000
0000000000001010
1110001100000001
0000000000000001
1111110000010000
0000000000001100
1110101010000111
0000000000000000
1111110000010000
0000000000000010
1110001100001000
```

## Project Structure
```
project6/
├── assembler
│   ├── main.py
│   ├── parser.py
│   ├── code.py
│   └── symbol_table.py
├── add/
│   ├── Add.asm
│   └── Add.hack
└── max/
    ├── Max.asm
    └── Max.hack
```

## Testing Instructions
1. Run assembler on .asm file
2. Compare output .hack with provided solution
3. Load .hack file into CPU Emulator
4. Verify program behavior

## Common Issues
- Symbol table initialization
- Label vs variable handling
- Binary conversion accuracy
- Comment and whitespace handling
- File I/O management

## Translation Tables

### Computation Bits
| comp   | c1c2c3c4c5c6 | Description |
|--------|--------------|-------------|
| 0      | 0101010     | Zero        |
| 1      | 0111111     | One         |
| -1     | 0111010     | Minus one   |
| D      | 0001100     | D register  |
| A      | 0110000     | A register  |
| !D     | 0001101     | Not D       |
| !A     | 0110001     | Not A       |
| -D     | 0001111     | Negate D    |
| -A     | 0110011     | Negate A    |
| D+1    | 0011111     | D plus 1    |
| A+1    | 0110111     | A plus 1    |
| D-1    | 0001110     | D minus 1   |
| A-1    | 0110010     | A minus 1   |
| D+A    | 0000010     | D plus A    |
| D-A    | 0010011     | D minus A   |
| A-D    | 0000111     | A minus D   |
| D&A    | 0000000     | D AND A     |
| D|A    | 0010101     | D OR A      |

## Resources
- [nand2tetris Course](https://www.nand2tetris.org)
- [Assembler Specification](https://www.nand2tetris.org/project06)
- [Assembly Language](https://www.nand2tetris.org/project04) 