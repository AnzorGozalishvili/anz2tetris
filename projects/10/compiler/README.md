# Jack Analyzer

A syntax analyzer that parses Jack programs according to the Jack grammar and outputs XML representation.

## Architecture

### JackAnalyzer (Main Driver)
1. Input Processing:
   - Accepts either a single .jack file or directory containing .jack files
   - Creates corresponding output files: 
     - *T.xml for tokenizer output
     - .xml for parsed structure

2. Two Operation Modes:
   - Tokenizer mode (`--tokens` flag): Outputs only tokenized XML
   - Full parsing mode: Outputs complete syntax tree XML

### JackTokenizer
1. Lexical Analysis:
   - Removes comments and whitespace
   - Breaks input into atomic tokens:
     - Keywords (class, if, while, etc.)
     - Symbols ({, }, (, ), etc.)
     - Identifiers (variable/class names)
     - Integer constants
     - String constants

2. Token Processing:
   - Maintains current token state
   - Provides methods to:
     - Advance to next token
     - Query token type
     - Access token value based on type

### CompilationEngine
1. Recursive Descent Parser:
   - Starts from class (root of syntax tree)
   - Recursively processes program structure:
     - Class declarations
     - Subroutine declarations
     - Variable declarations
     - Statements
     - Expressions

2. Grammar Handling:
   - Handles different statement types:
     - let, if, while, do, return
   - Processes expressions and terms
   - Manages subroutine calls
   - Handles array access

3. XML Generation:
   - Creates nested structure reflecting program hierarchy
   - Maintains proper indentation
   - Handles special XML characters
   - Generates both terminal and non-terminal elements

## Output Format

1. Tokenizer Output (*T.xml):
```xml
<tokens>
  <keyword> class </keyword>
  <identifier> Main </identifier>
  <symbol> { </symbol>
  ...
</tokens>
```

2. Parser Output (.xml):
```xml
<class>
  <keyword> class </keyword>
  <identifier> Main </identifier>
  <symbol> { </symbol>
  <subroutineDec>
    ...
  </subroutineDec>
  ...
</class>
```

## Development Stages

1. Stage 1: Tokenizer implementation and testing
2. Stage 2: Basic parsing without expressions
3. Stage 3: Expression handling
4. Stage 4: Array access support

## Testing

- Use `make test-tokenizer` for tokenizer tests
- Use `make test-parser` for parser tests
- Use `make test` for all tests
- Compare output with provided test files using TextComparer

## Special Handling

- XML special characters (<, >, &) are escaped
- Comments (// and /* */) are removed
- Proper indentation in output XML
- Expression list counting for future VM code generation