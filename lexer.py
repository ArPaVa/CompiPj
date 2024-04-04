import enum
import regex


class Token:

    # noinspection PyShadowingBuiltins
    def __init__(self, line, column, type, lexeme):
        self.line = line
        self.column = column
        self.type = type
        self.lexeme = lexeme

    def __repr__(self) -> str:
        return f"Token({self.line}, {self.column}, {self.type}, {self.lexeme})"


names = [
    'Semicolon', 'BraceL', 'BraceR', 'ParenL', 'ParenR', 'BracketL', 'BracketR', 'Comma', 'Equal',
    'Plus', 'Sub', 'Prod', 'Div', 'Rem', 'Pow', 'Dot', 'Colon', 'At', 'And', 'Or', 'Not',
    'GreaterThan', 'LessThan', 'New', 'As', 'Function', 'Let', 'In', 'If', 'Elif', 'Else', 'true',
    'false', 'Is', 'While', 'For', 'Type', 'Inherit', 'Protocol', 'Extends', 'Comprehension', 'Number',
    'Identifier', 'String'
]

Terminal = enum.Enum('Terminal', names)

# noinspection PyUnresolvedReferences
str2tk = {
    ';': Terminal.Semicolon,
    '{': Terminal.BraceL,
    '}': Terminal.BraceR,
    '(': Terminal.ParenL,
    ')': Terminal.ParenR,
    '[': Terminal.BracketL,
    ']': Terminal.BracketR,
    ',': Terminal.Comma,
    '=': Terminal.Equal,
    '+': Terminal.Plus,
    '-': Terminal.Sub,
    '*': Terminal.Prod,
    '/': Terminal.Div,
    '%': Terminal.Rem,
    '^': Terminal.Pow,
    '.': Terminal.Dot,
    ':': Terminal.Colon,
    '@': Terminal.At,
    '&': Terminal.And,
    '|': Terminal.Or,
    '||': Terminal.Comprehension,
    '!': Terminal.Not,
    '>': Terminal.GreaterThan,
    '<': Terminal.LessThan,
    'new': Terminal.New,
    'as': Terminal.As,
    'function': Terminal.Function,
    'let': Terminal.Let,
    'in': Terminal.In,
    'if': Terminal.If,
    'elif': Terminal.Elif,
    'else': Terminal.Else,
    'true': Terminal.true,
    'false': Terminal.false,
    'is': Terminal.Is,
    'while': Terminal.While,
    'for': Terminal.For,
    'type': Terminal.Type,
    'inherit': Terminal.Inherit,
    'protocol': Terminal.Protocol,
    'extends': Terminal.Extends,
}

escaped = [''.join(['\\' + char if char in regex.special else char for char in k]) for k in str2tk.keys()]

keywords = regex.regex('|'.join(escaped))
number = regex.regex('[0-9]+|[0-9]*.[0-9]+')
identifier = regex.regex('[_a-zA-Z][_a-zA-Z0-9]*')


# noinspection PyShadowingBuiltins
def tokenize(input):
    tokens = []
    input = input.rstrip()

    line = 1
    column = 1

    while len(input):

        while input[0].isspace():
            if input[0] == '\n':
                line += 1
                column = 1

            else:
                column += 1

            input = input[1:]

        match, i, lexeme = keywords.match(input)

        if match:
            tokens.append(Token(line, column, str2tk[lexeme], lexeme))

            column += i
            input = input[i:]

            continue

        match, i, lexeme = number.match(input)

        if match:
            # noinspection PyUnresolvedReferences
            tokens.append(Token(line, column, Terminal.Number, lexeme))

            column += i
            input = input[i:]

            continue

        match, i, lexeme = identifier.match(input)

        if match:
            # noinspection PyUnresolvedReferences
            tokens.append(Token(line, column, Terminal.Identifier, lexeme))

            column += i
            input = input[i:]

            continue

        if input[0] == '"':

            i = 1
            while input[i] != '"':
                if input[i] == '\\':
                    i += 1

                i += 1

            # noinspection PyUnresolvedReferences
            tokens.append(Token(line, column, Terminal.String, input[1:i]))

            column += i + 1
            input = input[i + 1:]

            continue

        # TODO: pretty print error
        raise SyntaxError(f'invalid syntax at {line}:{column}')

    tokens.append(Token(line, column, 0, '$'))
    return tokens
