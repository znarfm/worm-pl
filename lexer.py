import re  # module for regular expressions
import argparse
import sys
from pathlib import Path


class Token:
    """A simple class to represent tokens"""

    def __init__(self, type, value, line, column):
        self.type = type  # token type (e.g., NUMBER, IDENTIFIER)
        self.value = value  # actual token value
        self.line = line  # line number in source code
        self.column = column  # column number in source code

    def __str__(self):
        """String representation of the token"""
        return f"Type: {self.type:<15} Value: {self.value:<15} Line: {self.line:<4} Col: {self.column}"


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
            "WHITESPACE": r"[\s]+",
            # Comments
            "SINGLE_LINE_COMMENT": r"#[^\n]*(?:\n|$)",
            "MULTI_LINE_COMMENT": r'~~[\s\S]*?~~',
            # Numbers
            "FLOAT": r"(?<!\w)-?(\d+(_?\d+)*)?\.\d+(_?\d+)*",
            "INTEGER": r"(?<!\w)-?\d+(_?\d+)*",
            # Keywords
            "TYPE_INT": r"\b:int\b",
            "TYPE_CHAR": r"\b:char\b",
            "TYPE_FLOAT": r"\b:float\b",
            "TYPE_STRING": r"\b:str\b",
            "TYPE_LIST": r"\b:list\b",
            "TYPE_DICT": r"\b:dict\b",
            "TYPE_SET": r"\b:set\b",
            "TYPE_TUPLE": r"\b:tuple\b",
            "TYPE_BOOL": r"\b:bool\b",
            "IF": r"\bif\b",
            "ELSEIF": r"\belif\b",
            "ELSE": r"\belse\b",
            "WHILE": r"\bwhile\b",
            "FOR": r"\bfor\b",
            "DEFINE": r"\bdef\b",
            "RETURN": r"\breturn\b",
            "CLASS": r"\bclass\b",
            "IMPORT": r"\bimport\b",
            "FROM": r"\bfrom\b",
            "AS": r"\bas\b",
            "TRY": r"\btry\b",
            "EXCEPT": r"\bexcept\b",
            "FINALLY": r"\bfinally\b",
            "RAISE": r"\braise\b",
            "WITH": r"\bwith\b",
            "BREAK": r"\bbreak\b",
            "CONTINUE": r"\bcontinue\b",
            "NOTIN": r"\bnot in\b",
            "IN": r"\bin\b",
            "IS": r"\bis\b",
            # Booleans
            "TRUE": r"\bTrue\b",
            "FALSE": r"\bFalse\b",
            # Special
            "NULL": r"\bNone\b",
            # Logical Operators
            "NOT": r"\bnot\b",
            "AND": r"\band\b",
            "OR": r"\bor\b",
            # Identifiers
            "IDENTIFIER": r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
            "ARROW": r"->",
            "LAMBDA_ARROW": r"=>",
            # Bitwise Operators
            "BITW_AND": r"&",
            "BITW_OR": r"\|",
            "BITW_XOR": r"\^",
            "BITW_NOT": r"~",
            "BITW_LEFT_SHIFT": r"<<",
            "BITW_RIGHT_SHIFT": r">>",
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
            "POWER_ASSIGN": r"\*\*=",
            "FLOOR_DIV_ASSIGN": r"\/\/=",
            "MULT_ASSIGN": r"\*=",
            "DIV_ASSIGN": r"\/=",
            "MOD_ASSIGN": r"%=",
            # Arithmetic Operators
            "PLUS": r"\+",
            "MINUS": r"-",
            "POWER": r"\*\*",
            "FLOOR_DIV": r"\/\/",
            "MULTIPLY": r"\*",
            "DIVIDE": r"\/",
            "MODULO": r"%",
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
            "MULTI_LINE_STRING": r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'',
            "STRING": r'\"(?:\\.|[^"\\])*\"|\'(?:\\.|[^\'\\])*\'',
            # Special tokens
            "EXCLAIM": r"!",
            "NULL_COALESCING": r"\?\?",
            "QUESTION_MARK": r"\?",
        }

        # Combine all patterns into a single regular expression
        # Use named groups to identify the token type
        pattern_strings = [
            f"(?P<{name}>{pattern})" for name, pattern in self.patterns.items()
        ]
        pattern_strings.append(r"(?P<INVALID>.)")
        # Join all patterns with the OR operator '|'
        self.token_regex = re.compile("|".join(pattern_strings))

    def __str__(self):
        """String representation of the Lexer"""
        status = f"Number of Tokens: {len(self.tokens)}\n"
        return status

    def count_lines(self, text):
        """Count the number of newlines in a piece of text"""
        return text.count("\n")

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
            kind = token_match.lastgroup  # The last matched group name (token type)
            value = token_match.group()  # Actual token value / lexeme
            start_pos = token_match.start()
            column = start_pos - line_start + 1  # Calculate column number

            # Skip whitespace
            if kind == "WHITESPACE":
                continue

            # Count lines for multi-line tokens
            lines_in_token = self.count_lines(value)

            # Handle different token types
            if kind == "NEWLINE":
                line_num += 1
                line_start = start_pos + len(value)  # Update line start position
                continue
            elif kind == "INVALID":
                tokens.append(Token("INVALID", value, line_num, column))
            elif kind == "MULTI_LINE_COMMENT":
                if self.include_comments:
                    tokens.append(Token(kind, value, line_num, column))
                line_num += lines_in_token
                if lines_in_token > 0:
                    line_start = start_pos + value.rfind("\n") + 1
            elif kind == "STRING" and lines_in_token > 0:
                tokens.append(Token(kind, value, line_num, column))
                line_num += lines_in_token
                if lines_in_token > 0:
                    line_start = start_pos + value.rfind("\n") + 1
            else:
                if (
                    kind != "SINGLE_LINE_COMMENT" or self.include_comments
                ):  # Optional comment inclusion
                    tokens.append(Token(kind, value, line_num, column))
                if kind == "SINGLE_LINE_COMMENT":
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

    def get_complete_pattern(self, console_readable=False) -> str:
        """Returns the complete regex pattern used for tokenization."""
        # Get the scanner's pattern directly
        pattern = self.token_regex.pattern

        # Make it more readable by adding newlines between patterns
        if console_readable:
            pattern = pattern.replace("(?P", "\n(?P")
        return pattern

    def print_input_code(self):
        """
        Print the input code with proper formatting and line numbers.
        """
        lines = self.input_text.split("\n")
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


def print_tokens_table(tokens):
    """Print tokens in a formatted table"""
    # Print table header
    print("\nTokenization Results:")
    print("-" * 80)
    print(f"{'Line':<6} {'Column':<8} {'Token Type':<20} {'Value':<30}")
    print("-" * 80)

    # Print each token
    for token in tokens:
        print(
            f"{token.line:<6} {token.column:<8} {token.type:<20} {repr(token.value):<30}"
        )
    print("-" * 80)


def main():
    parser = argparse.ArgumentParser(description="Worm Programming Language Lexer")
    parser.add_argument("file", type=str, help="Path to the .worm file to tokenize")
    parser.add_argument(
        "-p", "--patterns", action="store_true", help="Show regex patterns"
    )
    parser.add_argument(
        "-c", "--comments", action="store_true", help="Include comments in tokenization"
    )
    args = parser.parse_args()

    try:
        # Read input file
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File '{args.file}' not found")
            sys.exit(1)

        code = file_path.read_text(encoding="utf-8")

        # Print input code
        print("\nInput Code:")
        print("-" * 40)
        for i, line in enumerate(code.split("\n"), 1):
            print(f"{i:2d} | {line}")
        print("-" * 40)

        # Tokenize and print results
        lexer = Lexer(code, include_comments=args.comments)
        tokens = lexer.tokenize()
        print_tokens_table(tokens)

        # Show patterns if requested
        if args.patterns:
            print("\nToken Patterns:")
            print("-" * 80)
            for name, pattern in lexer.get_patterns().items():
                print(f"{name:<20} {pattern}")
            print("-" * 80)

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
