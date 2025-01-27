import re  # module for regular expressions

class Token:
    """A simple class to represent tokens"""
    def __init__(self, type, value, line, column):
        self.type = type              # token type (e.g., NUMBER, IDENTIFIER)
        self.value = value            # actual token value
        self.line = line              # line number in source code
        self.column = column          # column number in source code
    
    def __str__(self):
        """String representation of the token"""
        return f'Type: {self.type:<15} Value: {self.value:<15} Line: {self.line:<4} Col: {self.column}'

class Lexer:
    def __init__(self, input_text, include_comments=False):
        self.input_text = input_text
        self.current_line = 1
        self.pos = 0
        self.tokens = []
        self.current_char = self.input_text[self.pos]
        self.include_comments = include_comments
        self.patterns = {
            # Whitespace
            "NEWLINE": r"\r\n|\n|\r",
            "WHITESPACE": r"[ \t]+",

            # Comments - updated patterns
            "SINGLE_LINE_COMMENT": r"#[^\n]*(?:\n|$)",
            "MULTI_LINE_COMMENT": r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'',

            # Numbers
            "FLOAT": r"\b\d*\.\d+([eE][+-]?\d+)?\b",
            "INTEGER": r"\b\d+\b",
            # "HEX": r"\b0[xX][0-9a-fA-F]+\b",
            
            'TYPE_INT': r'\bint\b',
            'TYPE_CHAR': r'\bchar\b',
            'TYPE_FLOAT': r'\bfloat\b',
            'TYPE_STRING': r'\bstr\b',
            'IF': r'\bif\b',
            'ELSEIF': r'\belif\b',
            'ELSE': r'\belse\b',
            'WHILE': r'\bwhile\b',
            'FOR': r'\bfor\b',
            'DEF': r'\bdef\b',
            'RETURN': r'\breturn\b',
            'CLASS': r'\bclass\b',
            'IMPORT': r'\bimport\b',
            'FROM': r'\bfrom\b',
            'AS': r'\bas\b',
            'TRY': r'\btry\b',
            'EXCEPT': r'\bexcept\b',
            'FINALLY': r'\bfinally\b',
            'RAISE': r'\braise\b',
            'WITH': r'\bwith\b',
            'STDOUT': r'\bprint\b',
            'BREAK': r'\bbreak\b',
            'CONTINUE': r'\bcontinue\b',
            'NOTIN': r'\bnot in\b',
            'IN': r'\bin\b',
            'IS': r'\bis\b',

            # Booleans
            "TRUE": r"\bTrue\b",
            "FALSE": r"\bFalse\b",
            "NULL": r"\bNone\b",

            # Logical Operators
            "NOT": r"not",
            "AND": r"and",
            "OR": r"or",

            # Identifiers and keywords
            "IDENTIFIER": r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
            
            'ARROW': r'->',
            'LAMBDA_ARROW': r'=>' ,

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

            # Arithmetic Operators
            "PLUS": r"\+",
            "MINUS": r"-",
            "MULTIPLY": r"\*",
            "FLOOR_DIV": r"\/\/",
            "DIVIDE": r"\/",
            "MODULO": r"%",
            "POWER": r"\*\*",
            
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
            "SEMICOLON": r";",
            
            # Strings
            "STRING": r'\"(?:\\.|[^"\\])*\"|\'(?:\\.|[^\'\\])*\'',

            # Special tokens
            'TRY_SHORT': r'!',
            'NULL_COALESCING': r'\?\?',
            'QUESTION_MARK': r'\?',
        }
        

        # No need for keywords set anymore since they're in patterns
        self.keywords = set()
        
        # Combine all patterns into a single regular expression
        # Use named groups to identify the token type
        pattern_strings = [f'(?P<{name}>{pattern})' for name, pattern in self.patterns.items()]
        pattern_strings.append(r'(?P<INVALID>.)')
        # Join all patterns with the OR operator '|'
        self.token_regex = re.compile('|'.join(pattern_strings))

    def __str__(self):
        """String representation of the Lexer"""
        status = f"Number of Tokens: {len(self.tokens)}\n"
        return status

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
        line_start = 0  # Track the start position of current line
        
        for token_match in self.token_regex.finditer(self.input_text):
            kind = token_match.lastgroup    # The last matched group name (token type)
            value = token_match.group()     # Actual token value
            start_pos = token_match.start()
            column = start_pos - line_start + 1  # Calculate column number
            
            # Skip whitespace
            if kind == 'WHITESPACE':
                continue
            
            # Count lines for multi-line tokens
            lines_in_token = self.count_lines(value)
            
            # Handle different token types
            if kind == 'NEWLINE':
                line_num += 1
                line_start = start_pos + len(value)  # Update line start position
                continue  # We don't need to tokenize newlines anymore
            elif kind == 'INVALID':
                tokens.append(Token('INVALID', value, line_num, column))
            elif kind == 'MULTI_LINE_COMMENT':
                if self.include_comments:
                    tokens.append(Token(kind, value, line_num, column))
                line_num += lines_in_token
                if lines_in_token > 0:
                    line_start = start_pos + value.rfind('\n') + 1
            elif kind == 'STRING' and lines_in_token > 0:
                tokens.append(Token(kind, value, line_num, column))
                line_num += lines_in_token
                if lines_in_token > 0:
                    line_start = start_pos + value.rfind('\n') + 1
            else:
                if kind != 'SINGLE_LINE_COMMENT' or self.include_comments:  # Optional comment inclusion
                    tokens.append(Token(kind, value, line_num, column))
                if kind == 'SINGLE_LINE_COMMENT':
                    line_num += 1
                    line_start = start_pos + len(value)
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
# test_code = '''def main() {
#     # This is a single line comment
#     """
#     This is a multi-line
#     comment that spans
#     several lines
#     """
#     x = 42;  # Assigning a number
#     if (x > 0) {
#         print("Positive");
#     };
#     print("Done");
# }'''

test_code = '''default_user = {
    name: "Guest",
    role: "Viewer"
}
current_user = user ?? default_user
welcome_message = current_user?name ? "Welcome, " + current_user.name : "Welcome!"'''

lexer = Lexer(test_code, include_comments=True)
print("Input:")
lexer.print_input_code()
print("\nTokens:")
lexer.tokenize()
lexer.print_tokens()
print(lexer)
# print(lexer.get_patterns())