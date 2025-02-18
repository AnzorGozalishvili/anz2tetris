from VMWriter import VMWriter
from SymbolTable import SymbolTable

class CompilationEngine:
    def __init__(self, tokenizer, output_file):
        self.tokenizer = tokenizer
        self.vm_writer = VMWriter(output_file)
        self.symbol_table = SymbolTable()
        self.class_name = None
        self.subroutine_name = None
        self.while_counter = 0
        self.if_counter = 0
        
    def __del__(self):
        """Destructor to ensure output file is closed"""
        self.vm_writer.close()
        
    def _get_unique_label(self, label_type):
        """Generate unique labels for control flow"""
        if label_type == 'WHILE':
            label = f'WHILE_{self.while_counter}'
            self.while_counter += 1
        elif label_type == 'IF':
            label = f'IF_{self.if_counter}'
            self.if_counter += 1
        return label
        
    def _get_segment(self, kind):
        """Convert symbol kind to VM segment"""
        segment_map = {
            'STATIC': 'static',
            'FIELD': 'this',
            'ARG': 'argument',
            'VAR': 'local'
        }
        return segment_map.get(kind, None)
        
    def _write_push_var(self, name):
        """Push variable onto stack"""
        kind = self.symbol_table.kind_of(name)
        if kind is None:
            raise ValueError(f"Undefined variable: {name}")
        index = self.symbol_table.index_of(name)
        segment = self._get_segment(kind)
        self.vm_writer.write_push(segment, index)
        
    def _write_pop_var(self, name):
        """Pop value from stack into variable"""
        kind = self.symbol_table.kind_of(name)
        if kind is None:
            raise ValueError(f"Undefined variable: {name}")
        index = self.symbol_table.index_of(name)
        segment = self._get_segment(kind)
        self.vm_writer.write_pop(segment, index)
        
    def compile_class(self):
        """Compiles a complete class"""
        # class declaration
        self.eat("KEYWORD")  # 'class'
        self.class_name = self.eat("IDENTIFIER")  # className
        self.symbol_table.class_name = self.class_name
        self.eat("SYMBOL")  # '{'
        
        # class variables
        while (self.tokenizer.current_token and 
               self.tokenizer.token_type() == "KEYWORD" and
               self.tokenizer.keyword() in ['static', 'field']):
            self.compile_class_var_dec()
            
        # class subroutines
        while (self.tokenizer.current_token and 
               self.tokenizer.token_type() == "KEYWORD" and
               self.tokenizer.keyword() in ['constructor', 'function', 'method']):
            self.compile_subroutine()
            
        self.eat("SYMBOL")  # '}'
        
    def compile_class_var_dec(self):
        """Compiles a static declaration or field declaration"""
        kind = self.eat("KEYWORD").upper()  # 'static' or 'field'
        var_type = self.eat()  # type
        var_name = self.eat("IDENTIFIER")  # varName
        
        # Add first variable to symbol table
        self.symbol_table.define(var_name, var_type, kind)
        
        # Handle additional variables
        while self.tokenizer.symbol() == ',':
            self.eat("SYMBOL")  # ','
            var_name = self.eat("IDENTIFIER")  # varName
            self.symbol_table.define(var_name, var_type, kind)
            
        self.eat("SYMBOL")  # ';'
        
    def compile_subroutine(self):
        """Compiles a complete method, function, or constructor"""
        # Reset symbol table for new subroutine
        self.symbol_table.reset()
        
        # Get subroutine info
        subroutine_type = self.eat("KEYWORD")  # 'constructor'/'function'/'method'
        return_type = self.eat()  # 'void' or type
        self.subroutine_name = self.eat("IDENTIFIER")  # subroutineName
        
        # For methods, first argument is always 'this'
        if subroutine_type == 'method':
            self.symbol_table.define('this', self.class_name, 'ARG')
            
        self.eat("SYMBOL")  # '('
        self.compile_parameter_list()
        self.eat("SYMBOL")  # ')'
        
        # Subroutine body
        self.eat("SYMBOL")  # '{'
        
        # Compile local variables
        n_locals = 0
        while (self.tokenizer.current_token and 
               self.tokenizer.token_type() == "KEYWORD" and 
               self.tokenizer.keyword() == 'var'):
            n_locals += self.compile_var_dec()
            
        # Write function declaration
        function_name = f"{self.class_name}.{self.subroutine_name}"
        self.vm_writer.write_function(function_name, n_locals)
        
        # Handle constructor/method setup
        if subroutine_type == 'constructor':
            # Allocate memory for object
            n_fields = self.symbol_table.var_count('FIELD')
            self.vm_writer.write_push('constant', n_fields)
            self.vm_writer.write_call('Memory.alloc', 1)
            self.vm_writer.write_pop('pointer', 0)  # Set this
        elif subroutine_type == 'method':
            # Set this to argument 0 (the object)
            self.vm_writer.write_push('argument', 0)
            self.vm_writer.write_pop('pointer', 0)
            
        self.compile_statements()
        self.eat("SYMBOL")  # '}'
        
    def compile_parameter_list(self):
        """Compiles a (possibly empty) parameter list"""
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ')':
            param_type = self.eat()  # type
            param_name = self.eat("IDENTIFIER")  # varName
            self.symbol_table.define(param_name, param_type, 'ARG')
            
            while self.tokenizer.symbol() == ',':
                self.eat("SYMBOL")  # ','
                param_type = self.eat()  # type
                param_name = self.eat("IDENTIFIER")  # varName
                self.symbol_table.define(param_name, param_type, 'ARG')
                
    def compile_var_dec(self):
        """Compiles a var declaration. Returns number of variables declared."""
        n_vars = 0
        
        self.eat("KEYWORD")  # 'var'
        var_type = self.eat()  # type
        var_name = self.eat("IDENTIFIER")  # varName
        
        # Add first variable to symbol table
        self.symbol_table.define(var_name, var_type, 'VAR')
        n_vars += 1
        
        # Handle additional variables
        while self.tokenizer.symbol() == ',':
            self.eat("SYMBOL")  # ','
            var_name = self.eat("IDENTIFIER")  # varName
            self.symbol_table.define(var_name, var_type, 'VAR')
            n_vars += 1
            
        self.eat("SYMBOL")  # ';'
        return n_vars
        
    def compile_statements(self):
        """Compiles a sequence of statements"""
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
                
    def compile_let(self):
        """Compiles a let statement"""
        self.eat("KEYWORD")  # 'let'
        var_name = self.eat("IDENTIFIER")  # varName
        
        # Handle array assignment
        if self.tokenizer.symbol() == '[':
            self.eat("SYMBOL")  # '['
            self.compile_expression()  # Array index
            self.eat("SYMBOL")  # ']'
            
            # Push array base address
            self._write_push_var(var_name)
            
            # Calculate target address (base + index)
            self.vm_writer.write_arithmetic('add')
            
            self.eat("SYMBOL")  # '='
            self.compile_expression()  # Value to assign
            
            # Store value in temp, get target address, then store value
            self.vm_writer.write_pop('temp', 0)  # Save value
            self.vm_writer.write_pop('pointer', 1)  # Set that
            self.vm_writer.write_push('temp', 0)  # Restore value
            self.vm_writer.write_pop('that', 0)  # Store in array
        else:
            self.eat("SYMBOL")  # '='
            self.compile_expression()
            self._write_pop_var(var_name)
            
        self.eat("SYMBOL")  # ';'
        
    def compile_if(self):
        """Compiles an if statement"""
        label_true = self._get_unique_label('IF')
        label_false = self._get_unique_label('IF')
        label_end = self._get_unique_label('IF')
        
        self.eat("KEYWORD")  # 'if'
        self.eat("SYMBOL")  # '('
        self.compile_expression()  # Condition
        self.eat("SYMBOL")  # ')'
        
        # if-goto label_true
        self.vm_writer.write_if(label_true)
        self.vm_writer.write_goto(label_false)
        self.vm_writer.write_label(label_true)
        
        self.eat("SYMBOL")  # '{'
        self.compile_statements()
        self.eat("SYMBOL")  # '}'
        
        # Handle else clause
        if self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() == 'else':
            self.vm_writer.write_goto(label_end)
            self.vm_writer.write_label(label_false)
            
            self.eat("KEYWORD")  # 'else'
            self.eat("SYMBOL")  # '{'
            self.compile_statements()
            self.eat("SYMBOL")  # '}'
            
            self.vm_writer.write_label(label_end)
        else:
            self.vm_writer.write_label(label_false)
        
    def compile_while(self):
        """Compiles a while statement"""
        label_loop = self._get_unique_label('WHILE')
        label_end = self._get_unique_label('WHILE')
        
        self.vm_writer.write_label(label_loop)
        
        self.eat("KEYWORD")  # 'while'
        self.eat("SYMBOL")  # '('
        self.compile_expression()  # Condition
        self.eat("SYMBOL")  # ')'
        
        # not and if-goto to handle while condition
        self.vm_writer.write_arithmetic('not')
        self.vm_writer.write_if(label_end)
        
        self.eat("SYMBOL")  # '{'
        self.compile_statements()
        self.eat("SYMBOL")  # '}'
        
        self.vm_writer.write_goto(label_loop)
        self.vm_writer.write_label(label_end)
        
    def compile_do(self):
        """Compiles a do statement"""
        self.eat("KEYWORD")  # 'do'
        self.compile_subroutine_call()
        self.eat("SYMBOL")  # ';'
        
        # Void methods/functions must pop return value
        self.vm_writer.write_pop('temp', 0)
        
    def compile_return(self):
        """Compiles a return statement"""
        self.eat("KEYWORD")  # 'return'
        
        # Handle return value if present
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ';':
            self.compile_expression()
        else:
            # Void functions must return 0
            self.vm_writer.write_push('constant', 0)
            
        self.eat("SYMBOL")  # ';'
        self.vm_writer.write_return()
        
    def compile_expression(self):
        """Compiles an expression"""
        self.compile_term()
        
        # Handle operators
        while (self.tokenizer.token_type() == "SYMBOL" and 
               self.tokenizer.symbol() in '+-*/&|<>='):
            # Save operator
            op = self.tokenizer.symbol()
            self.eat("SYMBOL")  # op
            
            self.compile_term()
            
            # Generate VM code for operator
            op_map = {
                '+': 'add',
                '-': 'sub',
                '*': 'call Math.multiply 2',
                '/': 'call Math.divide 2',
                '&': 'and',
                '|': 'or',
                '<': 'lt',
                '>': 'gt',
                '=': 'eq'
            }
            
            if op in ['*', '/']:
                self.vm_writer.write_call(op_map[op].split()[1], 2)
            else:
                self.vm_writer.write_arithmetic(op_map[op])
            
    def compile_term(self):
        """Compiles a term"""
        if self.tokenizer.token_type() == "INT_CONST":
            # Integer constant
            value = self.tokenizer.int_val()
            self.eat("INT_CONST")
            self.vm_writer.write_push('constant', value)
            
        elif self.tokenizer.token_type() == "STRING_CONST":
            # String constant
            string = self.tokenizer.string_val()
            self.eat("STRING_CONST")
            
            # Create new string object
            self.vm_writer.write_push('constant', len(string))
            self.vm_writer.write_call('String.new', 1)
            
            # Append each character
            for char in string:
                self.vm_writer.write_push('constant', ord(char))
                self.vm_writer.write_call('String.appendChar', 2)
                
        elif self.tokenizer.token_type() == "KEYWORD":
            # Keyword constant
            keyword = self.tokenizer.keyword()
            self.eat("KEYWORD")
            
            if keyword == 'true':
                self.vm_writer.write_push('constant', 0)
                self.vm_writer.write_arithmetic('not')
            elif keyword in ['false', 'null']:
                self.vm_writer.write_push('constant', 0)
            elif keyword == 'this':
                self.vm_writer.write_push('pointer', 0)
                
        elif self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == '(':
            # Parenthesized expression
            self.eat("SYMBOL")  # '('
            self.compile_expression()
            self.eat("SYMBOL")  # ')'
            
        elif self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() in '-~':
            # Unary operation
            op = self.tokenizer.symbol()
            self.eat("SYMBOL")
            self.compile_term()
            
            if op == '-':
                self.vm_writer.write_arithmetic('neg')
            else:  # '~'
                self.vm_writer.write_arithmetic('not')
                
        else:
            # Must be identifier
            name = self.tokenizer.identifier()
            self.eat("IDENTIFIER")
            
            if self.tokenizer.token_type() == "SYMBOL":
                if self.tokenizer.symbol() == '[':  # array access
                    self.eat("SYMBOL")  # '['
                    self.compile_expression()  # index
                    self.eat("SYMBOL")  # ']'
                    
                    # Push array base and add index
                    self._write_push_var(name)
                    self.vm_writer.write_arithmetic('add')
                    
                    # Get array value
                    self.vm_writer.write_pop('pointer', 1)
                    self.vm_writer.write_push('that', 0)
                    
                elif self.tokenizer.symbol() in '(.':  # subroutine call
                    self.compile_subroutine_call(name)
                else:
                    self._write_push_var(name)
            else:
                self._write_push_var(name)
                
    def compile_subroutine_call(self, name=None):
        """Compiles a subroutine call"""
        n_args = 0
        
        if name is None:
            name = self.eat("IDENTIFIER")
            
        # Method/function call with dot notation
        if self.tokenizer.symbol() == '.':
            self.eat("SYMBOL")  # '.'
            method_name = self.eat("IDENTIFIER")
            
            # Check if it's a method call on an object
            var_type = self.symbol_table.type_of(name)
            if var_type is not None:
                # Push object reference (this)
                self._write_push_var(name)
                n_args += 1
                function_name = f"{var_type}.{method_name}"
            else:
                # Static function call
                function_name = f"{name}.{method_name}"
        else:
            # Method call on current object
            self.vm_writer.write_push('pointer', 0)  # push this
            n_args += 1
            function_name = f"{self.class_name}.{name}"
            
        self.eat("SYMBOL")  # '('
        n_args += self.compile_expression_list()
        self.eat("SYMBOL")  # ')'
        
        self.vm_writer.write_call(function_name, n_args)
        
    def compile_expression_list(self):
        """Compiles a (possibly empty) comma-separated list of expressions"""
        n_args = 0
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ')':
            self.compile_expression()
            n_args += 1
            
            while self.tokenizer.symbol() == ',':
                self.eat("SYMBOL")  # ','
                self.compile_expression()
                n_args += 1
                
        return n_args

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
            value = self.tokenizer.int_val()
        elif token_type == "STRING_CONST":
            value = self.tokenizer.string_val()
            
        self.tokenizer.advance()
        return value 