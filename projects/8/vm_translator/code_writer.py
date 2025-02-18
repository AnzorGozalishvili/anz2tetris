class CodeWriter:
    def __init__(self, output_file):
        """
        Opens the output file and gets ready to write into it.
        Args:
            output_file (str): Path to the output .asm file
        """
        self.file = open(output_file, 'w')
        self.label_counter = 0
        self.current_function = ""

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

    def write_label(self, label):
        """Writes assembly code for label command"""
        # Create a unique label by combining function name and label
        full_label = f"{self.current_function}${label}"
        self.file.write(f"({full_label})\n")
    
    def write_goto(self, label):
        """Writes assembly code for goto command"""
        full_label = f"{self.current_function}${label}"
        self.file.write(f"@{full_label}\n")
        self.file.write("0;JMP\n")
    
    def write_if(self, label):
        """Writes assembly code for if-goto command"""
        self.file.write("@SP\n")
        self.file.write("AM=M-1\n")
        self.file.write("D=M\n")
        full_label = f"{self.current_function}${label}"
        self.file.write(f"@{full_label}\n")
        self.file.write("D;JNE\n")

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
        
        if segment == 'static':
            # Static variables are file-specific
            self.file.write(f"""// push static {index}
@{self.current_file}.{index}
D=M
@SP
A=M
M=D
@SP
M=M+1
""")
            return

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
        
        if segment == 'static':
            # Static variables are file-specific
            self.file.write(f"""// pop static {index}
@SP
AM=M-1
D=M
@{self.current_file}.{index}
M=D
""")
            return

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

    def write_function(self, function_name, num_locals):
        """
        Writes assembly code for function declaration
        Args:
            function_name (str): name of the function
            num_locals (int): number of local variables
        """
        # Update current function name for label handling
        self.current_function = function_name
        
        # Create function entry label
        self.file.write(f"// function {function_name} {num_locals}\n")
        self.file.write(f"({function_name})\n")
        
        # Initialize local variables to 0
        for _ in range(num_locals):
            self.file.write("""@0    // push 0
D=A
@SP
A=M
M=D
@SP
M=M+1
""")

    def write_call(self, function_name, num_args):
        """
        Writes assembly code for function calls
        Args:
            function_name (str): name of the function to call
            num_args (int): number of arguments already pushed by the caller
        """
        return_label = f"{self.current_function}$ret.{self.label_counter}"
        self.label_counter += 1
        
        # Save return address and caller's state
        self.file.write(f"""// call {function_name} {num_args}
@{return_label}    // push return address
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL            // push LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG            // push ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS           // push THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT           // push THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP             // ARG = SP - 5 - num_args
D=M
@5
D=D-A
@{num_args}
D=D-A
@ARG
M=D
@SP             // LCL = SP
D=M
@LCL
M=D
@{function_name}    // goto function
0;JMP
({return_label})    // return label
""")

    def write_return(self):
        """Writes assembly code for function return"""
        self.file.write("""// return
@LCL            // FRAME = LCL
D=M
@R13            // R13 = FRAME
M=D
@5              // RET = *(FRAME-5)
A=D-A
D=M
@R14            // R14 = RET
M=D
@SP             // *ARG = pop()
AM=M-1
D=M
@ARG
A=M
M=D
@ARG            // SP = ARG + 1
D=M+1
@SP
M=D
@R13            // THAT = *(FRAME-1)
AM=M-1
D=M
@THAT
M=D
@R13            // THIS = *(FRAME-2)
AM=M-1
D=M
@THIS
M=D
@R13            // ARG = *(FRAME-3)
AM=M-1
D=M
@ARG
M=D
@R13            // LCL = *(FRAME-4)
AM=M-1
D=M
@LCL
M=D
@R14            // goto RET
A=M
0;JMP
""")

    def close(self):
        """Closes the output file."""
        self.file.close()

    def set_filename(self, filename):
        """
        Informs the code writer that translation of a new VM file has started
        Args:
            filename (str): The name of the VM file being processed
        """
        # Extract just the filename without path and extension
        self.current_file = filename.split('/')[-1].replace('.vm', '')

    def write_init(self):
        """
        Writes the assembly code that effects the VM initialization
        (bootstrap code) at the beginning of the output file.
        """
        self.file.write("""// Bootstrap code
@256            // Initialize SP=256
D=A
@SP
M=D
""")
        
        # Call Sys.init
        self.current_function = "Bootstrap"
        self.write_call("Sys.init", 0) 