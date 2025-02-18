# VMTranslator Logic

1. call `VMTranslator.py` and pass `.vm` extension file with vm code to translate into machine code in `.asm` format
2. Main method parses input file name, resolves it and creates an output file to append translation
3. `CodeWriter` is initialized with `output_path` argument
4. `translate_file` is called with `input_path` and `CoreWriter` passed as arguments
5. Initiates `Parser` class object which processes commands sequentially (line by line)
   1. `Parser` iterates on lines and stips comments, if available. Only lines with valid commands are left
      1. `advance` method of `Parser` allows you to iterate on commands and process them by separating the constituent parts of command.
         1. Check if Parsed command is `C_ARITHMETIC` or `C_PUSH/POP` and write it to output file accordingly using codewriter
            1. if command type is `C_ARITHMETIC` then there are many options: (add, sub, neg, and, or, not, eq, gt, lt)
               1. `add` command example:
                  1. // Binary operation {operator}
                  2. @SP
                  3. AM=M-1
                  4. D=M
                  5. A=A-1
                  6. M=M{operator}D
            2. if command type is `C_PUSH` or `C_POP` then there are cases of push and pop with constant, segment and pointer. 
               1. `push` command example with `pointer`:
                  1. // push pointer {index}
                  2. @{base}
                  3. D=M
                  4. @SP
                  5. A=M
                  6. M=D
                  7. @SP
                  8. M=M+1
6. Finally, it closes the output file