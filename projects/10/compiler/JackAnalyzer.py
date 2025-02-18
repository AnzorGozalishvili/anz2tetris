import os
import sys
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

class JackAnalyzer:
    def __init__(self):
        self.tokenizer = None
        self.compilation_engine = None
    
    def tokenize_only(self, input_file):
        """
        First stage: Tokenizer only - creates *T.xml file with token XML
        """
        # Create output file in the same directory as input file
        output_file = os.path.splitext(input_file)[0] + 'T.xml'
        
        try:
            self.tokenizer = JackTokenizer(input_file)
            
            with open(output_file, 'w') as f:
                f.write('<tokens>\n')
                
                while self.tokenizer.has_more_tokens():
                    self.tokenizer.advance()
                    token_type = self.tokenizer.token_type()
                    
                    # Map token types to XML tags
                    tag_map = {
                        "KEYWORD": "keyword",
                        "SYMBOL": "symbol",
                        "IDENTIFIER": "identifier",
                        "INT_CONST": "integerConstant",
                        "STRING_CONST": "stringConstant"
                    }
                    
                    tag = tag_map[token_type]
                    
                    if token_type == "KEYWORD":
                        value = self.tokenizer.keyword()
                    elif token_type == "SYMBOL":
                        value = self.tokenizer.symbol()
                        # Handle XML special characters
                        if value == '<': value = '&lt;'
                        elif value == '>': value = '&gt;'
                        elif value == '&': value = '&amp;'
                    elif token_type == "IDENTIFIER":
                        value = self.tokenizer.identifier()
                    elif token_type == "INT_CONST":
                        value = str(self.tokenizer.int_val())
                    elif token_type == "STRING_CONST":
                        value = self.tokenizer.string_val().strip('"')  # Remove quotes
                    
                    f.write(f'  <{tag}> {value} </{tag}>\n')
                    
                f.write('</tokens>\n')
        except Exception as e:
            print(f"Error processing file {input_file}: {str(e)}")
            raise
    
    def analyze(self, input_file, tokenizer_only=False):
        """
        Main analysis method that processes a single .jack file
        """
        try:
            if tokenizer_only:
                self.tokenize_only(input_file)
            else:
                # Create output file in the same directory as input file
                output_file = os.path.splitext(input_file)[0] + '.xml'
                
                # Ensure the directory exists
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                
                self.tokenizer = JackTokenizer(input_file)
                self.compilation_engine = CompilationEngine(self.tokenizer, output_file)
                self.compilation_engine.compile_class()
        except Exception as e:
            print(f"Error analyzing file {input_file}: {str(e)}")
            raise

    @staticmethod
    def main(input_path, tokenizer_only=False):
        """
        Main entry point. Can handle both single files and directories
        containing .jack files
        """
        try:
            analyzer = JackAnalyzer()
            
            if os.path.isfile(input_path):
                # Handle single file
                if input_path.endswith('.jack'):
                    analyzer.analyze(input_path, tokenizer_only)
            elif os.path.isdir(input_path):
                # Handle directory
                for filename in os.listdir(input_path):
                    if filename.endswith('.jack'):
                        full_path = os.path.join(input_path, filename)
                        analyzer.analyze(full_path, tokenizer_only)
            else:
                raise ValueError(f"Input path {input_path} is neither a file nor a directory")
        except Exception as e:
            print(f"Error in main: {str(e)}")
            raise

if __name__ == "__main__":
    # Get input path from command line argument
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python JackAnalyzer.py <input_path> [--tokens]")
        print("<input_path> can be a .jack file or a directory containing .jack files")
        print("--tokens: optional flag to output only tokenizer XML for testing")
        sys.exit(1)
        
    input_path = sys.argv[1]
    tokenizer_only = "--tokens" in sys.argv
    
    try:
        JackAnalyzer.main(input_path, tokenizer_only)
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1) 