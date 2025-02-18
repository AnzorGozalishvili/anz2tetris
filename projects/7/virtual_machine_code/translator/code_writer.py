class CodeWriter:
    def __init__(self, output_file):
        """
        Opens the output file and gets ready to write into it.
        Args:
            output_file (str): Path to the output .asm file
        """
        self.file = open(output_file, 'w')
        self.label_counter = 0

    def write_arithmetic(self, command):
        """
        Writes assembly code for arithmetic/logical commands.
        Args:
            command (str): The arithmetic command (add, sub, neg, eq, gt, lt, and, or, not)
        """
        if command == 'add':
            self._write_binary_operation('+')
        elif command == 'sub':
            self._write_binary_operation('-')
        elif command == 'neg':
            self._write_unary_operation('-')
        elif command == 'and':
            self._write_binary_operation('&')
        elif command == 'or':
            self._write_binary_operation('|')
        elif command == 'not':
            self._write_unary_operation('!')
        elif command in ['eq', 'gt', 'lt']:
            self._write_comparison(command)

    def write_push_pop(self, command_type, segment, index):
        """
        Writes assembly code for push/pop commands.
        Args:
            command_type (str): C_PUSH or C_POP
            segment (str): memory segment
            index (int): index in the segment
        """
        if command_type == 'C_PUSH':
            if segment == 'constant':
                self._write_push_constant(index)
            elif segment == 'pointer':
                self._write_push_pointer(index)
            else:
                self._write_push_segment(segment, index)
        elif command_type == 'C_POP':
            if segment == 'pointer':
                self._write_pop_pointer(index)
            else:
                self._write_pop_segment(segment, index)

    def _write_binary_operation(self, operator):
        """Helper method for binary operations"""
        self.file.write(f"""// Binary operation {operator}
@SP
AM=M-1
D=M
A=A-1
M=M{operator}D
""")

    def _write_unary_operation(self, operator):
        """Helper method for unary operations"""
        self.file.write(f"""// Unary operation {operator}
@SP
A=M-1
M={operator}M
""")

    def _write_comparison(self, command):
        """Helper method for comparison operations"""
        label = f"{command.upper()}_{self.label_counter}"
        self.label_counter += 1
        
        self.file.write(f"""// Comparison {command}
@SP
AM=M-1
D=M
A=A-1
D=M-D
@{label}_TRUE
D;J{command.upper()}
@SP
A=M-1
M=0
@{label}_END
0;JMP
({label}_TRUE)
@SP
A=M-1
M=-1
({label}_END)
""")

    def _write_push_constant(self, value):
        """Helper method for push constant"""
        self.file.write(f"""// push constant {value}
@{value}
D=A
@SP
A=M
M=D
@SP
M=M+1
""")

    def _write_push_pointer(self, index):
        """Helper method for push pointer"""
        base = '3' if index == 0 else '4'  # THIS (3) or THAT (4)
        self.file.write(f"""// push pointer {index}
@{base}
D=M
@SP
A=M
M=D
@SP
M=M+1
""")

    def _write_pop_pointer(self, index):
        """Helper method for pop pointer"""
        base = '3' if index == 0 else '4'  # THIS (3) or THAT (4)
        self.file.write(f"""// pop pointer {index}
@SP
AM=M-1
D=M
@{base}
M=D
""")

    def _write_push_segment(self, segment, index):
        """Helper method for push from segment"""
        segment_map = {
            'local': 'LCL',
            'argument': 'ARG',
            'this': 'THIS',
            'that': 'THAT',
            'temp': '5',  # temp is mapped to RAM[5-12]
        }
        
        base = segment_map.get(segment)
        if segment in ['temp']:
            self.file.write(f"""// push {segment} {index}
@{base}
D=A
@{index}
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
""")
        else:
            self.file.write(f"""// push {segment} {index}
@{base}
D=M
@{index}
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
""")

    def _write_pop_segment(self, segment, index):
        """Helper method for pop to segment"""
        segment_map = {
            'local': 'LCL',
            'argument': 'ARG',
            'this': 'THIS',
            'that': 'THAT',
            'temp': '5',  # temp is mapped to RAM[5-12]
        }
        
        base = segment_map.get(segment)
        if segment in ['temp']:
            self.file.write(f"""// pop {segment} {index}
@{base}
D=A
@{index}
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
""")
        else:
            self.file.write(f"""// pop {segment} {index}
@{base}
D=M
@{index}
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
""")

    def close(self):
        """Closes the output file."""
        self.file.close() 