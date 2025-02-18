class CompilationEngine:
    def __init__(self, tokenizer, output_file):
        self.tokenizer = tokenizer
        self.output_file = open(output_file, 'w')
        self.indent_level = 0
        self.debug = True  # Add debug flag
        
    def __del__(self):
        """Destructor to ensure output file is closed"""
        self.output_file.close()
        
    def write_terminal(self, token_type, token_value):
        """Write a terminal token with proper XML formatting"""
        indent = "  " * self.indent_level
        
        # Map token types to XML tags
        tag_map = {
            "KEYWORD": "keyword",
            "SYMBOL": "symbol",
            "IDENTIFIER": "identifier",
            "INT_CONST": "integerConstant",     # For regular XML output
            "STRING_CONST": "stringConstant"    # For regular XML output
        }
        
        tag = tag_map[token_type]
        
        if token_type == "SYMBOL":
            # Handle XML special characters
            if token_value == '<': token_value = '&lt;'
            elif token_value == '>': token_value = '&gt;'
            elif token_value == '&': token_value = '&amp;'
        elif token_type == "STRING_CONST":
            # Remove the quotes from string constants
            token_value = token_value.strip('"')
        
        self.output_file.write(f'{indent}<{tag}> {token_value} </{tag}>\n')
    
    def write_tag(self, tag, is_closing=False):
        """Write an XML tag with proper indentation"""
        indent = "  " * (self.indent_level - 1 if is_closing else self.indent_level)
        self.output_file.write(f'{indent}{"</" if is_closing else "<"}{tag}>\n')
    
    def eat(self, expected_token=None):
        """Consume current token and advance to next"""
        if not self.tokenizer.current_token:
            self.tokenizer.advance()
            
        token_type = self.tokenizer.token_type()
        if expected_token and token_type != expected_token:
            # Add more context to error message
            value = None
            if token_type == "KEYWORD":
                value = self.tokenizer.keyword()
            elif token_type == "SYMBOL":
                value = self.tokenizer.symbol()
            elif token_type == "IDENTIFIER":
                value = self.tokenizer.identifier()
            elif token_type == "INT_CONST":
                value = str(self.tokenizer.int_val())
            elif token_type == "STRING_CONST":
                value = self.tokenizer.string_val()
            
            raise SyntaxError(
                f"Syntax Error: Expected {expected_token}, but got {token_type} ({value})"
            )
            
        value = None
        if token_type == "KEYWORD":
            value = self.tokenizer.keyword()
        elif token_type == "SYMBOL":
            value = self.tokenizer.symbol()
        elif token_type == "IDENTIFIER":
            value = self.tokenizer.identifier()
        elif token_type == "INT_CONST":
            value = str(self.tokenizer.int_val())
        elif token_type == "STRING_CONST":
            value = self.tokenizer.string_val()
            
        self.write_terminal(token_type, value)
        self.tokenizer.advance()
        return value
        
    def compile_class(self):
        """Compiles a complete class"""
        self.write_tag("class")
        self.indent_level += 1
        
        # class declaration
        self.eat("KEYWORD")  # 'class'
        self.eat("IDENTIFIER")  # className
        self.eat("SYMBOL")  # '{'
        
        # class variables
        while self.tokenizer.current_token and self.tokenizer.token_type() == "KEYWORD":
            if self.tokenizer.keyword() in ['static', 'field']:
                self.compile_class_var_dec()
            else:
                break
                
        # class subroutines
        while self.tokenizer.current_token and self.tokenizer.token_type() == "KEYWORD":
            if self.tokenizer.keyword() in ['constructor', 'function', 'method']:
                self.compile_subroutine()
            else:
                break
                
        self.eat("SYMBOL")  # '}'
        
        self.indent_level -= 1
        self.write_tag("class", True)
        
    def compile_class_var_dec(self):
        """Compiles a static declaration or field declaration"""
        self.write_tag("classVarDec")
        self.indent_level += 1
        
        self.eat("KEYWORD")  # 'static' or 'field'
        self.eat()  # type
        self.eat("IDENTIFIER")  # varName
        
        while self.tokenizer.symbol() == ',':
            self.eat("SYMBOL")  # ','
            self.eat("IDENTIFIER")  # varName
            
        self.eat("SYMBOL")  # ';'
        
        self.indent_level -= 1
        self.write_tag("classVarDec", True)
        
    def compile_subroutine(self):
        """Compiles a complete method, function, or constructor"""
        self.write_tag("subroutineDec")
        self.indent_level += 1
        
        self.eat("KEYWORD")  # 'constructor'/'function'/'method'
        self.eat()  # 'void' or type
        self.eat("IDENTIFIER")  # subroutineName
        self.eat("SYMBOL")  # '('
        self.compile_parameter_list()
        self.eat("SYMBOL")  # ')'
        
        # subroutine body
        self.write_tag("subroutineBody")
        self.indent_level += 1
        
        self.eat("SYMBOL")  # '{'
        while self.tokenizer.current_token and self.tokenizer.keyword() == 'var':
            self.compile_var_dec()
        self.compile_statements()
        self.eat("SYMBOL")  # '}'
        
        self.indent_level -= 1
        self.write_tag("subroutineBody", True)
        
        self.indent_level -= 1
        self.write_tag("subroutineDec", True)
        
    def compile_parameter_list(self):
        """Compiles a (possibly empty) parameter list"""
        self.write_tag("parameterList")
        self.indent_level += 1
        
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ')':
            self.eat()  # type
            self.eat("IDENTIFIER")  # varName
            while self.tokenizer.symbol() == ',':
                self.eat("SYMBOL")  # ','
                self.eat()  # type
                self.eat("IDENTIFIER")  # varName
                
        self.indent_level -= 1
        self.write_tag("parameterList", True)
        
    def compile_var_dec(self):
        """Compiles a var declaration"""
        self.write_tag("varDec")
        self.indent_level += 1
        
        self.eat("KEYWORD")  # 'var'
        self.eat()  # type
        self.eat("IDENTIFIER")  # varName
        
        while self.tokenizer.symbol() == ',':
            self.eat("SYMBOL")  # ','
            self.eat("IDENTIFIER")  # varName
            
        self.eat("SYMBOL")  # ';'
        
        self.indent_level -= 1
        self.write_tag("varDec", True)
        
    def compile_statements(self):
        """Compiles a sequence of statements"""
        self.write_tag("statements")
        self.indent_level += 1
        
        while self.tokenizer.token_type() == "KEYWORD":
            keyword = self.tokenizer.keyword()
            if keyword == 'let':
                self.compile_let()
            elif keyword == 'if':
                self.compile_if()
            elif keyword == 'while':
                self.compile_while()
            elif keyword == 'do':
                self.compile_do()
            elif keyword == 'return':
                self.compile_return()
            else:
                break
                
        self.indent_level -= 1
        self.write_tag("statements", True)
        
    def compile_do(self):
        """Compiles a do statement"""
        self.write_tag("doStatement")
        self.indent_level += 1
        
        self.eat("KEYWORD")  # 'do'
        self.compile_subroutine_call(identifier_consumed=False)
        self.eat("SYMBOL")  # ';'
        
        self.indent_level -= 1
        self.write_tag("doStatement", True)
        
    def compile_let(self):
        """Compiles a let statement"""
        self.write_tag("letStatement")
        self.indent_level += 1
        
        self.eat("KEYWORD")  # 'let'
        self.eat("IDENTIFIER")  # varName
        
        # Handle array access
        if self.tokenizer.symbol() == '[':
            self.eat("SYMBOL")  # '['
            self.compile_expression()
            self.eat("SYMBOL")  # ']'
            
        self.eat("SYMBOL")  # '='
        self.compile_expression()
        self.eat("SYMBOL")  # ';'
        
        self.indent_level -= 1
        self.write_tag("letStatement", True)
        
    def compile_while(self):
        """Compiles a while statement"""
        self.write_tag("whileStatement")
        self.indent_level += 1
        
        self.eat("KEYWORD")  # 'while'
        self.eat("SYMBOL")  # '('
        self.compile_expression()
        self.eat("SYMBOL")  # ')'
        self.eat("SYMBOL")  # '{'
        self.compile_statements()
        self.eat("SYMBOL")  # '}'
        
        self.indent_level -= 1
        self.write_tag("whileStatement", True)
        
    def compile_return(self):
        """Compiles a return statement"""
        self.write_tag("returnStatement")
        self.indent_level += 1
        
        self.eat("KEYWORD")  # 'return'
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ';':
            self.compile_expression()
        self.eat("SYMBOL")  # ';'
        
        self.indent_level -= 1
        self.write_tag("returnStatement", True)
        
    def compile_if(self):
        """Compiles an if statement"""
        self.write_tag("ifStatement")
        self.indent_level += 1
        
        self.eat("KEYWORD")  # 'if'
        self.eat("SYMBOL")  # '('
        self.compile_expression()
        self.eat("SYMBOL")  # ')'
        self.eat("SYMBOL")  # '{'
        self.compile_statements()
        self.eat("SYMBOL")  # '}'
        
        # Handle else clause
        if self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() == 'else':
            self.eat("KEYWORD")  # 'else'
            self.eat("SYMBOL")  # '{'
            self.compile_statements()
            self.eat("SYMBOL")  # '}'
            
        self.indent_level -= 1
        self.write_tag("ifStatement", True)
        
    def compile_expression(self):
        """Compiles an expression"""
        self.write_tag("expression")
        self.indent_level += 1
        
        self.compile_term()
        while (self.tokenizer.token_type() == "SYMBOL" and 
               self.tokenizer.symbol() in '+-*/&|<>='):
            self.eat("SYMBOL")  # op
            self.compile_term()
            
        self.indent_level -= 1
        self.write_tag("expression", True)
        
    def compile_term(self):
        """Compiles a term"""
        self.write_tag("term")
        self.indent_level += 1
        
        self.debug_print("Compiling term")
        
        if self.tokenizer.token_type() == "INT_CONST":
            self.eat("INT_CONST")
        elif self.tokenizer.token_type() == "STRING_CONST":
            self.eat("STRING_CONST")
        elif self.tokenizer.token_type() == "KEYWORD":
            self.eat("KEYWORD")  # true/false/null/this
        elif self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == '(':
            self.eat("SYMBOL")  # '('
            self.compile_expression()
            self.eat("SYMBOL")  # ')'
        elif self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() in '-~':
            self.eat("SYMBOL")  # unary op
            self.compile_term()
        else:
            # Must be identifier
            self.eat("IDENTIFIER")  # varName or subroutineName or className
            
            if self.tokenizer.token_type() == "SYMBOL":
                if self.tokenizer.symbol() == '[':  # array access
                    self.eat("SYMBOL")  # '['
                    self.compile_expression()
                    self.eat("SYMBOL")  # ']'
                elif self.tokenizer.symbol() in '(.':  # subroutine call
                    self.compile_subroutine_call(identifier_consumed=True)
                    
        self.indent_level -= 1
        self.write_tag("term", True)
        
    def compile_expression_list(self):
        """
        Compiles a (possibly empty) comma-separated list of expressions.
        Returns the number of expressions in the list.
        """
        self.write_tag("expressionList")
        self.indent_level += 1
        
        expression_count = 0
        
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ')':
            self.compile_expression()
            expression_count += 1
            
            while self.tokenizer.symbol() == ',':
                self.eat("SYMBOL")  # ','
                self.compile_expression()
                expression_count += 1
                
        self.indent_level -= 1
        self.write_tag("expressionList", True)
        
        return expression_count
        
    def compile_subroutine_call(self, identifier_consumed=False):
        """
        Compiles a subroutine call.
        Can be in the form of:
        1. subroutineName(expressionList)
        2. className.subroutineName(expressionList)
        3. varName.subroutineName(expressionList)
        
        Args:
            identifier_consumed: True if the first identifier has already been consumed
        """
        self.debug_print("Starting subroutine call")
        
        if not identifier_consumed:
            self.eat("IDENTIFIER")  # subroutineName or className/varName
        
        # Check for method/function call with dot notation
        if self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == '.':
            self.eat("SYMBOL")  # eat the '.'
            self.eat("IDENTIFIER")  # subroutineName
        
        self.eat("SYMBOL")  # '('
        nArgs = self.compile_expression_list()
        self.eat("SYMBOL")  # ')'
        
        return nArgs

    def debug_print(self, message):
        """Print debug information if debug mode is on"""
        if self.debug:
            current_token = self.tokenizer.current_token
            token_type = self.tokenizer.token_type() if current_token else "None"
            token_value = None
            if token_type == "KEYWORD":
                token_value = self.tokenizer.keyword()
            elif token_type == "SYMBOL":
                token_value = self.tokenizer.symbol()
            elif token_type == "IDENTIFIER":
                token_value = self.tokenizer.identifier()
            elif token_type == "INT_CONST":
                token_value = str(self.tokenizer.int_val())
            elif token_type == "STRING_CONST":
                token_value = self.tokenizer.string_val()
            
            print(f"DEBUG: {message}")
            print(f"Current token: {token_type} ({token_value})") 