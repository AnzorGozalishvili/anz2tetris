# Compiler I: Syntax Analysis

Implementation of a syntax analyzer (tokenizer and parser) for the Jack programming language, generating XML output representing the program's structure.

## Compiler Specifications

### Tokenizer
| Token Type | Description                          | Examples          |
|------------|--------------------------------------|-------------------|
| KEYWORD    | Jack language keywords               | class, if, while  |
| SYMBOL     | Special symbols and operators        | {, }, (, ), =, ; |
| IDENTIFIER | Names of variables, classes, etc.    | Main, counter    |
| INT_CONST  | Integer constants (0-32767)          | 123, 0, 32767    |
| STRING_CONST| String literals                     | "Hello World"    |

### Grammar Rules
```
class: 'class' className '{' classVarDec* subroutineDec* '}'
classVarDec: ('static'|'field') type varName (',' varName)* ';'
subroutineDec: ('constructor'|'function'|'method') ('void'|type) subroutineName '(' parameterList ')' subroutineBody
```

## Implementation Examples

### Tokenizer
```python
class JackTokenizer:
    def __init__(self, input_file):
        self.tokens = []
        self.current = -1
        
        # Remove comments and tokenize
        content = self.remove_comments(input_file.read())
        self.tokenize(content)

    def has_more_tokens(self):
        return self.current < len(self.tokens) - 1

    def advance(self):
        self.current += 1
        return self.tokens[self.current]

    def token_type(self):
        token = self.tokens[self.current]
        if token in KEYWORDS:
            return "KEYWORD"
        elif token in SYMBOLS:
            return "SYMBOL"
        elif token.isdigit():
            return "INT_CONST"
        elif token.startswith('"'):
            return "STRING_CONST"
        else:
            return "IDENTIFIER"
```

### Parser
```python
class CompilationEngine:
    def __init__(self, tokenizer, output_file):
        self.tokenizer = tokenizer
        self.output = output_file
        self.indent_level = 0

    def compile_class(self):
        self.write_xml_tag("class")
        self.indent_level += 1

        # 'class' keyword
        self.write_terminal(self.tokenizer.token_type(),
                          self.tokenizer.current_token())
        self.tokenizer.advance()

        # className
        self.write_terminal("IDENTIFIER",
                          self.tokenizer.current_token())
        self.tokenizer.advance()

        # '{' symbol
        self.write_terminal("SYMBOL", "{")
        self.tokenizer.advance()

        # classVarDec* subroutineDec*
        while self.tokenizer.has_more_tokens():
            if self.tokenizer.current_token() in ["static", "field"]:
                self.compile_class_var_dec()
            elif self.tokenizer.current_token() in ["constructor", "function", "method"]:
                self.compile_subroutine()
            else:
                break

        # '}' symbol
        self.write_terminal("SYMBOL", "}")
        
        self.indent_level -= 1
        self.write_xml_tag("/class")
```

## Test Cases

### Class Declaration
```
// Input: Main.jack
class Main {
    static boolean test;
    field int x, y;
    
    method void main() {
        var int i;
        let i = 0;
        return;
    }
}

// Output: Main.xml
<class>
  <keyword> class </keyword>
  <identifier> Main </identifier>
  <symbol> { </symbol>
  <classVarDec>
    <keyword> static </keyword>
    <keyword> boolean </keyword>
    <identifier> test </identifier>
    <symbol> ; </symbol>
  </classVarDec>
  <classVarDec>
    <keyword> field </keyword>
    <keyword> int </keyword>
    <identifier> x </identifier>
    <symbol> , </symbol>
    <identifier> y </identifier>
    <symbol> ; </symbol>
  </classVarDec>
  <subroutineDec>
    <keyword> method </keyword>
    <keyword> void </keyword>
    <identifier> main </identifier>
    <symbol> ( </symbol>
    <parameterList>
    </parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
      <symbol> { </symbol>
      <varDec>
        <keyword> var </keyword>
        <keyword> int </keyword>
        <identifier> i </identifier>
        <symbol> ; </symbol>
      </varDec>
      <statements>
        <letStatement>
          <keyword> let </keyword>
          <identifier> i </identifier>
          <symbol> = </symbol>
          <expression>
            <term>
              <integerConstant> 0 </integerConstant>
            </term>
          </expression>
          <symbol> ; </symbol>
        </letStatement>
        <returnStatement>
          <keyword> return </keyword>
          <symbol> ; </symbol>
        </returnStatement>
      </statements>
      <symbol> } </symbol>
    </subroutineBody>
  </subroutineDec>
  <symbol> } </symbol>
</class>
```

## Project Structure
```
project10/
├── JackAnalyzer/
│   ├── JackAnalyzer.py
│   ├── JackTokenizer.py
│   └── CompilationEngine.py
├── ArrayTest/
│   ├── Main.jack
│   └── Main.xml
└── Square/
    ├── Main.jack
    ├── Square.jack
    ├── SquareGame.jack
    └── *.xml
```

## Testing Instructions
1. Run analyzer on .jack files
2. Compare output .xml with provided solution
3. Use TextComparer to verify output
4. Check XML structure and formatting

## Common Issues
- Comment handling
- String constant parsing
- XML formatting
- Token classification
- Grammar rule implementation

## Grammar Elements

### Program Structure
```
class: 'class' className '{' classVarDec* subroutineDec* '}'
classVarDec: ('static'|'field') type varName (',' varName)* ';'
type: 'int'|'char'|'boolean'|className
subroutineDec: ('constructor'|'function'|'method') ('void'|type) subroutineName '(' parameterList ')' subroutineBody
```

### Statements
```
statements: statement*
statement: letStatement|ifStatement|whileStatement|doStatement|returnStatement
letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
whileStatement: 'while' '(' expression ')' '{' statements '}'
```

## Resources
- [nand2tetris Course](https://www.nand2tetris.org)
- [Compiler Specification](https://www.nand2tetris.org/project10)
- [Jack Grammar](https://www.nand2tetris.org/project10) 