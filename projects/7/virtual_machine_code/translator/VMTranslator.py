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
    parser = Parser(input_path)
    
    while parser.has_more_commands():
        parser.advance()
        
        if parser.command_type() == 'C_ARITHMETIC':
            code_writer.write_arithmetic(parser.arg1())
        elif parser.command_type() in ['C_PUSH', 'C_POP']:
            code_writer.write_push_pop(parser.command_type(), parser.arg1(), parser.arg2())

def main():
    if len(sys.argv) != 2:
        print("Usage: VMTranslator file.vm")
        sys.exit(1)

    # Get input file path
    input_path = sys.argv[1]
    
    # Check if file exists and has .vm extension
    if not os.path.exists(input_path):
        print(f"Error: File {input_path} not found")
        sys.exit(1)
    if not input_path.endswith('.vm'):
        print("Error: Input file must have .vm extension")
        sys.exit(1)

    # Create output file path by replacing .vm with .asm
    output_path = input_path[:-3] + '.asm'
    
    # Initialize CodeWriter
    code_writer = CodeWriter(output_path)
    
    # Translate the file
    translate_file(input_path, code_writer)
    
    # Close the output file
    code_writer.close()

if __name__ == "__main__":
    main() 