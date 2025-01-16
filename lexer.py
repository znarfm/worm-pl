import re  # module for regular expressions

class Token:
    """A simple class to represent tokens"""
    def __init__(self, type, value, line, indent_level=0):
        self.type = type              # token type (e.g., NUMBER, IDENTIFIER)
        self.value = value            # actual token value
        self.line = line              # line number in source code
        self.indent_level = indent_level  # indentation level (0, 1, 2, etc.)
    
    def __str__(self):
        """String representation of the token"""
        return f'Type: {self.type:<15} Value: {self.value:<15} Line: {self.line:<4} Indent: {self.indent_level}'

class Lexer:
    def __init__(self, input_text, include_comments=False):
        self.input_text = input_text
        self.current_line = 1  # Start from line 1
        self.pos = 0
        self.tokens = []
        self.current_char = self.input_text[self.pos]
        self.include_comments = include_comments
        self.patterns = {
            # Whitespace
            "NEWLINE": r"\n+",
            "INDENT": r"^[ \t]+",

            # Comments - updated patterns
            "SINGLE_LINE_COMMENT": r"#[^\n]*(?:\n|$)",
            "MULTI_LINE_COMMENT": r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'',

            # Numbers
            "INTEGER": r"\b\d+\b",
            "FLOAT": r"\b\d*\.\d+([eE][+-]?\d+)?\b",
            "HEX": r"\b0[xX][0-9a-fA-F]+\b",
            
            # Identifiers and keywords
            "IDENTIFIER": r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
            
            # Arithmetic Operators
            "PLUS": r"\+",
            "MINUS": r"-",
            "MULTIPLY": r"\*",
            "DIVIDE": r"\/",
            "MODULO": r"%",
            "FLOOR_DIV": r"\/\/",
            "POWER": r"\*\*",
            
            # Comparison Operators
            "EQUALS": r"==",
            "NOT_EQUALS": r"!=",
            "LESS_EQUAL": r"<=",
            "GREATER_EQUAL": r">=",
            "LESS_THAN": r"<",
            "GREATER_THAN": r">",
            
            # Assignment Operators
            "ASSIGN": r"=",
            "PLUS_ASSIGN": r"\+=",
            "MINUS_ASSIGN": r"-=",
            "MULT_ASSIGN": r"\*=",
            "DIV_ASSIGN": r"\/=",
            "MOD_ASSIGN": r"%=",
            
            # Logical Operators
            "AND": r"and",
            "OR": r"or",
            "NOT": r"not",
            
            # Delimiters
            "LEFT_PAREN": r"\(",
            "RIGHT_PAREN": r"\)",
            "LEFT_BRACKET": r"\[",
            "RIGHT_BRACKET": r"\]",
            "LEFT_BRACE": r"\{",
            "RIGHT_BRACE": r"\}",
            "COMMA": r",",
            "DOT": r"\.",
            "COLON": r":",
            
            # Strings
            "STRING": r'\"(?:\\.|[^"\\])*\"|\'(?:\\.|[^\'\\])*\'',
        }
        
        # Store keywords separately
        self.keywords = {
            'if', 'else', 'while', 'for', 'def', 'return', 'class',
            'import', 'from', 'as', 'try', 'except', 'finally',
            'raise', 'with', 'print', 'assert', 'break', 'continue',
            'global', 'nonlocal', 'lambda', 'yield', 'in', 'is',
        }
        
        # Combine all patterns into a single regular expression
        # Use named groups to identify the token type
        pattern_strings = [f'(?P<{name}>{pattern})' for name, pattern in self.patterns.items()]
        # Join all patterns with the OR operator '|'
        self.token_regex = re.compile('|'.join(pattern_strings))

    def __str__(self):
        """String representation of the Lexer"""
        status = f"Number of Tokens: {len(self.tokens)}\n"
        return status

    def calculate_indent_level(self, indent_str):
        """Calculate indentation level based on spaces/tabs"""
        if '\t' in indent_str:
            return len(indent_str)  # Count tabs
        return len(indent_str) // 4  # Assume 4 spaces per level

    def count_lines(self, text):
        """Count the number of newlines in a piece of text"""
        return text.count('\n')

    def tokenize(self) -> list:
        """
        Tokenize the input text into a list of tokens.
        
        Returns:
            list: List of Token objects
        """
        tokens = []
        line_num = 1
        current_indent = 0
        
        for token_match in self.token_regex.finditer(self.input_text):
            kind = token_match.lastgroup    # The last matched group name (token type)
            value = token_match.group()     # Actual token value
            
            # Handle indentation
            if kind == 'INDENT':
                current_indent = self.calculate_indent_level(value)
                continue
            
            # Count lines for multi-line tokens
            lines_in_token = self.count_lines(value)
            
            # Handle different token types
            if kind == 'NEWLINE':
                tokens.append(Token(kind, '\\n', line_num, current_indent))
                line_num += 1
                current_indent = 0
            elif kind == 'MULTI_LINE_COMMENT':
                # Add the multi-line comment token with its starting line
                tokens.append(Token(kind, value, line_num, current_indent))
                line_num += lines_in_token
            elif kind == 'STRING' and lines_in_token > 0:
                # Handle multi-line strings
                tokens.append(Token(kind, value, line_num, current_indent))
                line_num += lines_in_token
            else:
                # Handle all other tokens
                if kind == 'IDENTIFIER' and value in self.keywords:
                    kind = 'KEYWORD'
                if kind != 'SINGLE_LINE_COMMENT' or self.include_comments:  # Optional comment inclusion
                    tokens.append(Token(kind, value, line_num, current_indent))
                if kind == 'SINGLE_LINE_COMMENT':
                    line_num += 1
        self.tokens = tokens
        return tokens

    def get_patterns(self):
        """
        Returns a dictionary of token types and their corresponding regex patterns.

        Returns:
            dict: Dictionary mapping token types to their regex patterns
        """
        return self.patterns
    
    def print_input_code(self):
        """
        Print the input code with proper formatting and line numbers.
        """
        lines = self.input_text.split('\n')
        print("-" * 40)
        for i, line in enumerate(lines, 1):
            print(f"{i:2d} | {line}")
        print("-" * 40)

    def print_tokens(self):
        """
        Print all tokens in a readable format.
        """
        tokens = self.tokens
        for token in tokens:
            print(token)  # Uses Token.__str__ method

# Example usage:
test_code = '''def main():
    # This is a single line comment
    """
    This is a multi-line
    comment that spans
    several lines
    """
    x = 42
    print('Hello,\\nWorld!')  # with newline'''

lexer = Lexer(test_code, include_comments=True)
print("Input:")
lexer.print_input_code()
print("\nTokens:")
lexer.tokenize()
lexer.print_tokens()
print(lexer)
# print(lexer.get_patterns())