import re


class Token:
    def __init__(self, type_, value, pos=None):
        self.type = type_
        self.value = value
        self.pos = pos

    def __repr__(self):
        return f"{self.type}:{self.value}"


class TokenizerError(Exception):
    def __init__(self, char, pos):
        super().__init__(f"Unexpected character '{char}' at position {pos}")
        self.char = char
        self.pos = pos


class Tokenizer:
    def __init__(self, input_string):
        self.input = input_string
        self.tokens = self._tokenize()

    def _tokenize(self):
        token_specification = [
            ('NUMBER', r'\d+(\.\d+)?'),  # integers or floats
            ('PLUS',   r'\+'),
            ('MINUS',  r'-'),
            ('MULT',   r'\*'),
            ('DIV',    r'/'),
            ('SKIP',   r'[ \t\n\r]+'),    # whitespace
            ('MISMATCH', r'.'),          # anything else is invalid
        ]

        tok_regex = '|'.join(
            f'(?P<{name}>{pattern})'
            for name, pattern in token_specification
        )

        tokens = []

        for match in re.finditer(tok_regex, self.input):
            kind = match.lastgroup
            value = match.group()
            pos = match.start()

            if kind == 'NUMBER':
                tokens.append(Token('NUMBER', float(value) if '.' in value else int(value), pos))

            elif kind in ('PLUS', 'MINUS', 'MULT', 'DIV'):
                tokens.append(Token(kind, value, pos))

            elif kind == 'SKIP':
                continue

            elif kind == 'MISMATCH':
                raise TokenizerError(value, pos)

        tokens.append(Token('EOF', '$', len(self.input)))
        return tokens

    def get_tokens(self):
        return self.tokens