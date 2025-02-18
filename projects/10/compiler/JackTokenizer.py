class JackTokenizer:
    # Token types
    KEYWORD = "KEYWORD"
    SYMBOL = "SYMBOL"
    IDENTIFIER = "IDENTIFIER"
    INT_CONST = "INT_CONST"
    STRING_CONST = "STRING_CONST"
    
    # Keywords in Jack language
    KEYWORDS = {
        'class', 'constructor', 'function', 'method', 'field', 'static',
        'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null',
        'this', 'let', 'do', 'if', 'else', 'while', 'return'
    }
    
    # Symbols in Jack language
    SYMBOLS = {
        '{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/',
        '&', '|', '<', '>', '=', '~'
    }
    
    def __init__(self, input_file):
        """Opens the input file and gets ready to tokenize it"""
        with open(input_file, 'r') as file:
            # Remove comments and empty lines
            self.content = self._remove_comments(file.read())
            
        self.tokens = self._tokenize()
        self.current_token = None
        self.current_index = -1
    
    def _remove_comments(self, content):
        """Removes all comments from the input"""
        # Remove multi-line comments
        while '/*' in content:
            start = content.find('/*')
            end = content.find('*/', start) + 2
            if end < 2:  # If '*/' not found
                break
            content = content[:start] + ' ' + content[end:]
            
        # Remove single-line comments
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            comment_start = line.find('//')
            if comment_start != -1:
                line = line[:comment_start]
            if line.strip():
                cleaned_lines.append(line)
        return '\n'.join(cleaned_lines)
    
    def _tokenize(self):
        """Tokenizes the input content"""
        tokens = []
        i = 0
        content = self.content
        
        while i < len(content):
            char = content[i]
            
            # Skip whitespace
            if char.isspace():
                i += 1
                continue
                
            # Handle string constants
            if char == '"':
                end = content.find('"', i + 1)
                if end != -1:
                    tokens.append((self.STRING_CONST, content[i+1:end]))
                    i = end + 1
                    continue
                    
            # Handle symbols
            if char in self.SYMBOLS:
                tokens.append((self.SYMBOL, char))
                i += 1
                continue
                
            # Handle integer constants
            if char.isdigit():
                num = ''
                while i < len(content) and content[i].isdigit():
                    num += content[i]
                    i += 1
                tokens.append((self.INT_CONST, int(num)))
                continue
                
            # Handle identifiers and keywords
            if char.isalnum() or char == '_':
                word = ''
                while i < len(content) and (content[i].isalnum() or content[i] == '_'):
                    word += content[i]
                    i += 1
                if word in self.KEYWORDS:
                    tokens.append((self.KEYWORD, word))
                else:
                    tokens.append((self.IDENTIFIER, word))
                continue
                
            i += 1
            
        return tokens
    
    def has_more_tokens(self):
        """Returns True if there are more tokens to process"""
        return self.current_index < len(self.tokens) - 1
    
    def advance(self):
        """Advances to the next token"""
        if self.has_more_tokens():
            self.current_index += 1
            self.current_token = self.tokens[self.current_index]
    
    def token_type(self):
        """Returns the type of the current token"""
        if self.current_token:
            return self.current_token[0]
        return None
    
    def keyword(self):
        """Returns the keyword which is the current token"""
        if self.token_type() == self.KEYWORD:
            return self.current_token[1]
        raise ValueError("Current token is not a keyword")
    
    def symbol(self):
        """Returns the character which is the current token"""
        if self.token_type() == self.SYMBOL:
            return self.current_token[1]
        raise ValueError("Current token is not a symbol")
    
    def identifier(self):
        """Returns the identifier which is the current token"""
        if self.token_type() == self.IDENTIFIER:
            return self.current_token[1]
        raise ValueError("Current token is not an identifier")
    
    def int_val(self):
        """Returns the integer value of the current token"""
        if self.token_type() == self.INT_CONST:
            return self.current_token[1]
        raise ValueError("Current token is not an integer constant")
    
    def string_val(self):
        """Returns the string value of the current token"""
        if self.token_type() == self.STRING_CONST:
            return self.current_token[1]
        raise ValueError("Current token is not a string constant") 