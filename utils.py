class Token:

    def __init__(self, line, column, _type, lexeme):
        self.line = line
        self.column = column
        self.type = _type
        self.lexeme = lexeme

