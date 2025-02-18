class Parser:
    def __init__(self, input_file):
        """
        Opens the input file and gets ready to parse it.
        Args:
            input_file (str): Path to the .asm file
        """
        self.current_instruction = None
        self.current_command_type = None
        
        # Read and clean the input file
        with open(input_file, 'r') as file:
            # Remove comments and empty lines, strip whitespace
            self.instructions = []
            for line in file:
                # Remove inline comments and trailing/leading whitespace
                line = line.split('//')[0].strip()
                # Skip empty lines and pure comment lines
                if line:
                    self.instructions.append(line)
                    
        self.instruction_count = len(self.instructions)
        self.current_instruction_idx = -1

    def has_more_instructions(self):
        """
        Returns True if there are more instructions to process.
        """
        return self.current_instruction_idx < self.instruction_count - 1

    def advance(self):
        """
        Reads the next instruction and makes it the current instruction.
        Should be called only if has_more_instructions() is true.
        """
        self.current_instruction_idx += 1
        self.current_instruction = self.instructions[self.current_instruction_idx]
        
        # Determine the instruction type
        if self.current_instruction.startswith('@'):
            self.current_command_type = 'A_COMMAND'
        elif '=' in self.current_instruction or ';' in self.current_instruction:
            self.current_command_type = 'C_COMMAND'
        elif self.current_instruction.startswith('('):
            self.current_command_type = 'L_COMMAND'

    def command_type(self):
        """
        Returns the type of the current command:
        A_COMMAND for @Xxx
        C_COMMAND for dest=comp;jump
        L_COMMAND for (Xxx)
        """
        return self.current_command_type

    def symbol(self):
        """
        Returns the symbol or decimal of the current command @Xxx or (Xxx).
        Should be called only when command_type() is A_COMMAND or L_COMMAND.
        """
        if self.current_command_type == 'A_COMMAND':
            return self.current_instruction[1:]  # Remove '@'
        elif self.current_command_type == 'L_COMMAND':
            return self.current_instruction[1:-1]  # Remove '(' and ')'
        
    def dest(self):
        """
        Returns the dest mnemonic in the current C-command (8 possibilities).
        Should be called only when command_type() is C_COMMAND.
        """
        if self.current_command_type != 'C_COMMAND':
            return None
            
        if '=' in self.current_instruction:
            return self.current_instruction.split('=')[0]
        return None

    def comp(self):
        """
        Returns the comp mnemonic in the current C-command (28 possibilities).
        Should be called only when command_type() is C_COMMAND.
        """
        if self.current_command_type != 'C_COMMAND':
            return None
            
        instruction = self.current_instruction
        if '=' in instruction:
            instruction = instruction.split('=')[1]
        if ';' in instruction:
            instruction = instruction.split(';')[0]
        return instruction

    def jump(self):
        """
        Returns the jump mnemonic in the current C-command (8 possibilities).
        Should be called only when command_type() is C_COMMAND.
        """
        if self.current_command_type != 'C_COMMAND':
            return None
            
        if ';' in self.current_instruction:
            return self.current_instruction.split(';')[1]
        return None

class Code:
    def __init__(self):
        # Lookup tables for binary codes
        self.dest_table = {
            None: '000',  # No destination
            'M': '001',   # Memory
            'D': '010',   # D register
            'MD': '011',  # Memory and D register
            'A': '100',   # A register
            'AM': '101',  # A register and Memory
            'AD': '110',  # A register and D register
            'ADM': '111'  # A register, Memory, and D register
        }

        self.jump_table = {
            None: '000',  # No jump
            'JGT': '001', # Jump if greater than zero
            'JEQ': '010', # Jump if equal to zero
            'JGE': '011', # Jump if greater or equal to zero
            'JLT': '100', # Jump if less than zero
            'JNE': '101', # Jump if not equal to zero
            'JLE': '110', # Jump if less or equal to zero
            'JMP': '111'  # Jump unconditionally
        }

        self.comp_table = {
            # When a=0
            '0': '0101010',
            '1': '0111111',
            '-1': '0111010',
            'D': '0001100',
            'A': '0110000',
            '!D': '0001101',
            '!A': '0110001',
            '-D': '0001111',
            '-A': '0110011',
            'D+1': '0011111',
            'A+1': '0110111',
            'D-1': '0001110',
            'A-1': '0110010',
            'D+A': '0000010',
            'D-A': '0010011',
            'A-D': '0000111',
            'D&A': '0000000',
            'D|A': '0010101',
            # When a=1 (M instead of A)
            'M': '1110000',
            '!M': '1110001',
            '-M': '1110011',
            'M+1': '1110111',
            'M-1': '1110010',
            'D+M': '1000010',
            'D-M': '1010011',
            'M-D': '1000111',
            'D&M': '1000000',
            'D|M': '1010101'
        }

    def dest(self, mnemonic):
        """Convert dest mnemonic to binary"""
        return self.dest_table[mnemonic]

    def comp(self, mnemonic):
        """Convert comp mnemonic to binary"""
        return self.comp_table[mnemonic]

    def jump(self, mnemonic):
        """Convert jump mnemonic to binary"""
        return self.jump_table[mnemonic]

    def a_instruction(self, value):
        """Convert A-instruction to binary
        For now, assumes value is a number (not a symbol)
        """
        # Convert to binary and remove '0b' prefix
        binary = bin(int(value))[2:]
        # Pad with zeros to make it 16 bits
        return '0' * (16 - len(binary)) + binary

    def c_instruction(self, dest, comp, jump):
        """Convert C-instruction to binary"""
        # C-instruction format: 111accccccdddjjj
        return '111' + self.comp(comp) + self.dest(dest) + self.jump(jump)

class SymbolTable:
    def __init__(self):
        """Initialize the symbol table with predefined symbols"""
        self.table = {
            # Predefined symbols
            'SP': 0,
            'LCL': 1,
            'ARG': 2,
            'THIS': 3,
            'THAT': 4,
            'R0': 0,
            'R1': 1,
            'R2': 2,
            'R3': 3,
            'R4': 4,
            'R5': 5,
            'R6': 6,
            'R7': 7,
            'R8': 8,
            'R9': 9,
            'R10': 10,
            'R11': 11,
            'R12': 12,
            'R13': 13,
            'R14': 14,
            'R15': 15,
            'SCREEN': 16384,
            'KBD': 24576
        }
        self.next_variable_address = 16  # Variables start at RAM[16]

    def add_entry(self, symbol, address):
        """
        Adds a new symbol-address pair to the table.
        Args:
            symbol (str): The symbol name
            address (int): The memory or instruction address
        """
        self.table[symbol] = address

    def contains(self, symbol):
        """
        Checks if the symbol table contains the given symbol.
        Args:
            symbol (str): The symbol to look up
        Returns:
            bool: True if the symbol exists in the table
        """
        return symbol in self.table

    def get_address(self, symbol):
        """
        Returns the address associated with the symbol.
        Args:
            symbol (str): The symbol to look up
        Returns:
            int: The address associated with the symbol
        """
        return self.table[symbol]

    def add_variable(self, symbol):
        """
        Adds a new variable to the symbol table if it doesn't exist.
        Returns the address assigned to the variable.
        Args:
            symbol (str): The variable name
        Returns:
            int: The address assigned to the variable
        """
        if not self.contains(symbol):
            self.add_entry(symbol, self.next_variable_address)
            self.next_variable_address += 1
        return self.get_address(symbol)

def first_pass(parser, symbol_table):
    """
    First pass through the assembly code to record label positions.
    Args:
        parser (Parser): The parser object
        symbol_table (SymbolTable): The symbol table object
    """
    instruction_counter = 0
    
    while parser.has_more_instructions():
        parser.advance()
        if parser.command_type() == 'L_COMMAND':
            # Add label and its instruction number to symbol table
            symbol_table.add_entry(parser.symbol(), instruction_counter)
        else:
            # Only increment counter for actual instructions (A or C)
            instruction_counter += 1

def second_pass(parser, symbol_table, code):
    """
    Second pass through the assembly code to handle variables and generate binary code.
    Args:
        parser (Parser): The parser object
        symbol_table (SymbolTable): The symbol table object
        code (Code): The code object for binary conversion
    Returns:
        list: List of binary instructions
    """
    binary_code = []
    
    while parser.has_more_instructions():
        parser.advance()
        if parser.command_type() == 'A_COMMAND':
            symbol = parser.symbol()
            # Check if it's a number or a symbol
            try:
                address = int(symbol)
            except ValueError:
                # It's a symbol, get or create its address
                address = symbol_table.add_variable(symbol)
            binary = code.a_instruction(str(address))
            binary_code.append(binary)
            
        elif parser.command_type() == 'C_COMMAND':
            binary = code.c_instruction(parser.dest(), parser.comp(), parser.jump())
            binary_code.append(binary)
            
    return binary_code

def main():
    import sys
    import os
    
    if len(sys.argv) != 2:
        print("Usage: python assembler.py file.asm")
        sys.exit(1)

    # Get input file path
    input_path = sys.argv[1]
    
    # Check if file exists and has .asm extension
    if not os.path.exists(input_path):
        print(f"Error: File {input_path} not found")
        sys.exit(1)
    if not input_path.endswith('.asm'):
        print("Error: Input file must have .asm extension")
        sys.exit(1)

    # Create output file path by replacing .asm with .hack
    output_path = input_path[:-4] + '.hack'
    
    # Initialize assembler components
    parser = Parser(input_path)
    code = Code()
    symbol_table = SymbolTable()
    
    # First pass: collecting labels
    first_pass(parser, symbol_table)
    
    # Second pass: generating binary code
    parser = Parser(input_path)
    binary_code = second_pass(parser, symbol_table, code)
    
    # Write binary code to output file
    with open(output_path, 'w') as f:
        for instruction in binary_code:
            f.write(instruction + '\n')

if __name__ == "__main__":
    main()
