import os
import sys
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine
from VMWriter import VMWriter
from SymbolTable import SymbolTable

class JackCompiler:
    def __init__(self):
        self.tokenizer = None
        self.compilation_engine = None
    
    def compile(self, input_file):
        """
        Compiles a single .jack file into .vm file
        """
        try:
            # Create output file in the same directory as input file
            output_file = os.path.splitext(input_file)[0] + '.vm'
            
            self.tokenizer = JackTokenizer(input_file)
            self.compilation_engine = CompilationEngine(self.tokenizer, output_file)
            self.compilation_engine.compile_class()
        except Exception as e:
            print(f"Error compiling file {input_file}: {str(e)}")
            raise

    @staticmethod
    def main(input_path):
        """
        Main entry point. Can handle both single files and directories
        containing .jack files
        """
        try:
            compiler = JackCompiler()
            
            if os.path.isfile(input_path):
                # Handle single file
                if input_path.endswith('.jack'):
                    compiler.compile(input_path)
            elif os.path.isdir(input_path):
                # Handle directory
                for filename in os.listdir(input_path):
                    if filename.endswith('.jack'):
                        full_path = os.path.join(input_path, filename)
                        compiler.compile(full_path)
            else:
                raise ValueError(f"Input path {input_path} is neither a file nor a directory")
        except Exception as e:
            print(f"Error in main: {str(e)}")
            raise

if __name__ == "__main__":
    # Get input path from command line argument
    if len(sys.argv) != 2:
        print("Usage: python JackCompiler.py <input_path>")
        print("<input_path> can be a .jack file or a directory containing .jack files")
        sys.exit(1)
        
    input_path = sys.argv[1]
    
    try:
        JackCompiler.main(input_path)
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1) 