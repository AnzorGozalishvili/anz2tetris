#!/usr/bin/env python3

import sys
import os
from parser import Parser
from code_writer import CodeWriter

def translate_file(input_path, code_writer):
    """
    Translates a single .vm file to Hack assembly code.
    Args:
        input_path (str): Path to the input .vm file
        code_writer (CodeWriter): CodeWriter instance to write the output
    """
    # Inform code writer about new source file
    code_writer.set_filename(input_path)
    
    parser = Parser(input_path)
    
    while parser.has_more_commands():
        parser.advance()
        
        if parser.command_type() == 'C_ARITHMETIC':
            code_writer.write_arithmetic(parser.arg1())
        elif parser.command_type() in ['C_PUSH', 'C_POP']:
            code_writer.write_push_pop(parser.command_type(), parser.arg1(), parser.arg2())
        elif parser.command_type() == 'C_LABEL':
            code_writer.write_label(parser.arg1())
        elif parser.command_type() == 'C_GOTO':
            code_writer.write_goto(parser.arg1())
        elif parser.command_type() == 'C_IF':
            code_writer.write_if(parser.arg1())
        elif parser.command_type() == 'C_FUNCTION':
            code_writer.write_function(parser.arg1(), parser.arg2())
        elif parser.command_type() == 'C_RETURN':
            code_writer.write_return()
        elif parser.command_type() == 'C_CALL':
            code_writer.write_call(parser.arg1(), parser.arg2())

def main():
    if len(sys.argv) != 2:
        print("Usage: VMTranslator [file.vm | directory]")
        sys.exit(1)

    input_path = sys.argv[1]
    
    if os.path.isdir(input_path):
        # Handle directory input
        vm_files = [f for f in os.listdir(input_path) if f.endswith('.vm')]
        if not vm_files:
            print(f"Error: No .vm files found in {input_path}")
            sys.exit(1)
            
        # Create output file with same name as directory
        dir_name = os.path.basename(input_path)
        output_path = os.path.join(input_path, f"{dir_name}.asm")
        
        # Initialize CodeWriter and write bootstrap code
        code_writer = CodeWriter(output_path)
        code_writer.write_init()  # Bootstrap code only for directory input
        
        # Translate each .vm file
        for vm_file in vm_files:
            file_path = os.path.join(input_path, vm_file)
            translate_file(file_path, code_writer)
            
    else:
        # Handle single file input
        if not input_path.endswith('.vm'):
            print("Error: Input file must have .vm extension")
            sys.exit(1)
        if not os.path.exists(input_path):
            print(f"Error: File {input_path} not found")
            sys.exit(1)
            
        # Create output file path by replacing .vm with .asm
        output_path = input_path[:-3] + '.asm'
        
        # Initialize CodeWriter (no bootstrap code for single file)
        code_writer = CodeWriter(output_path)
        translate_file(input_path, code_writer)
    
    code_writer.close()

if __name__ == "__main__":
    main() 