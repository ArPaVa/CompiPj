class Token:
    def _init_(self,line,column,type,lexeme):
        self.line = line
        self.column = column
        self.type = type
        self.lexeme = lexeme