class Token:

    def __init__(self, line, column, _type, lexeme):
        self.line = line
        self.column = column
        self.type = _type
        self.lexeme = lexeme
    def __str__(self) -> str:
        return f"{self.lexeme} {self.type}"
    def __repr__(self) -> str:
        return self.__str__()

from enum import Enum
TokenType = Enum('TokenType', [
    ## Main
    # Non-terminals
    'Program', 'Body', 'Exp', 'ClassList', 'Expression', 'BlockExpression', 'ExpressionList',
    'EndOfStatment', 'Value', 'ArgumentList', 'Vector', 'Explicit', 'Iterable', 'SubExp',
    # Terminals
    'semicolon', 'obrace', 'cbrace', 'opar', 'cpar', 'New', 'identifier', 'As', 'obracket',
    'cbracket', 'generator', 'comma', 'equal',

    ## ArithmeticExpression
    # Non-terminals
    'ArithmeticExpression', 'Term', 'Usub', 'Factor', 'Base', 'PosibleArguments',
    # Terminals    
    'minus', 'plus', 'mult', 'div', 'rest', 'potency', 'number', 'dot',

    ## PrintExpression
    # Non-terminals
    'PrintExpression', 'CanPrint',
    # Terminals
    'Print',
    ## StringExpression
    # Non-terminals
    'StringExpresion', 'ConcatString', ''
    # Terminals
    'string', 'at_sign', #'double_quote',# lo quite para cojer los strings empezando por ahí

    ## Functions
    # Non-terminals
    'Function', 'FunctionList', 'FunctionHeader', 'Params',
    # Terminals
    'Lambda', 'function',

    ## Variables
    # Non-terminals
    'LetExpression', 'AssignList', 'AfterIn', 'DestructiveExpression',
    # Terminals
    'Let', 'In', 'dequal',

    ## Conditionals
    # Non-terminals
    'IfExpression', 'ConditionalExpression', 'ElseExpression', 'Nor', 'Comparable',
    # Terminals
    'If', 'Elif', 'Else', 'And', 'Or', 'Not', 'true', 'false', 'greater', 'greater_equal',
    'less', 'less_equal', 'equal_equal', 'not_equal', 'Is', 

    ##Loops
    # Non-terminals
    'WhileExpression', 'ForExpression',
    # Terminals
    'While', 'For', 

    ## Types/TypesChecking
    # Non-terminals
    'TypeDeclaration', 'TypeParams', 'Inherit', 'TypeBody', 'AttributeDef', 'MethodDef', 'TypeCheck',
    # Terminals
    'type', '_inherit', 'two_dots',

    ##Protocols
    # Non-terminals
    'ProtocolDefinition', 'MethodDefList', 'ProtocolsMethods',
    # Terminals
    'protocol',
    # Non-terminals
    # Terminals
    # Terminals in this context

    # Extra
    'EOF'
])
# TODO it should'n be needed 2 dict one fpr the regex to work, and one to have the actual terminals
terminal_tokens = {
    ';'   : TokenType.semicolon,
    '{'   : TokenType.obrace,
    '}'   : TokenType.cbrace,
    '('   : TokenType.opar,
    ')'   : TokenType.cpar,
    '['   : TokenType.obracket,
    ']'   : TokenType.cbracket,
    '||'  : TokenType.generator,
    ','   : TokenType.comma,
    '='   : TokenType.equal,
    '$'   : TokenType.EOF, ##Not sure about the $

    '+'   : TokenType.plus,
    '-'   : TokenType.minus,
    '*'   : TokenType.mult,
    '/'   : TokenType.div,
    '%'   : TokenType.rest,
    '^'   : TokenType.potency,
    '.'   : TokenType.dot,
    
    '=>'  : TokenType.Lambda,

    ':='  : TokenType.dequal,
    '@'   : TokenType.at_sign,
    '&'   : TokenType.And,
    '|'   : TokenType.Or,
    '!'   : TokenType.Not,
    '>'   : TokenType.greater,
    '>='  : TokenType.greater_equal,
    '<'   : TokenType.less,
    '<='  : TokenType.less_equal,
    '!='  : TokenType.not_equal,

    ':'   : TokenType.two_dots,
    
    # '\"'  : TokenType.double_quote,
    
    '=='  : TokenType.equal_equal,


    'new'      : TokenType.New,
    'as'       : TokenType.As,
    'print'    : TokenType.Print,
    'function' : TokenType.Function,
    'let'      : TokenType.Let,
    'in'       : TokenType.In,

    'if'       : TokenType.If,
    'elif'     : TokenType.Elif,
    'else'     : TokenType.Else,

    'true'     : TokenType.true,
    'false'    : TokenType.false,
    'is'       : TokenType.Is,
  
    'while'    : TokenType.While,
    'for'      : TokenType.For,    
    'type'     : TokenType.type,
    'inherit'  : TokenType._inherit,
    'protocol' : TokenType.protocol
}

escape_terminal_tokens = {
    ';'   : TokenType.semicolon,
    '{'   : TokenType.obrace,
    '}'   : TokenType.cbrace,
    '\\('   : TokenType.opar,
    '\\)'   : TokenType.cpar,
    '\\['   : TokenType.obracket,
    '\\]'   : TokenType.cbracket,
    '\\|\\|'  : TokenType.generator,
    ','   : TokenType.comma,
    '='   : TokenType.equal,
    '$'   : TokenType.EOF, ##Not sure about the $

    '\\+'   : TokenType.plus,
    '\\-'   : TokenType.minus,
    '\\*'   : TokenType.mult,
    '/'   : TokenType.div,
    '%'   : TokenType.rest,
    '^'   : TokenType.potency,
    '.'   : TokenType.dot,
    
    '=>'  : TokenType.Lambda,

    ':='  : TokenType.dequal,
    '@'   : TokenType.at_sign,
    '&'   : TokenType.And,
    '\\|'   : TokenType.Or,
    '!'   : TokenType.Not,
    '>'   : TokenType.greater,
    '>='  : TokenType.greater_equal,
    '<'   : TokenType.less,
    '<='  : TokenType.less_equal,
    '!='  : TokenType.not_equal,

    ':'   : TokenType.two_dots,
    
    # '\"'  : TokenType.double_quote,
    
    '=='  : TokenType.equal_equal,


    'new'      : TokenType.New,
    'as'       : TokenType.As,
    'print'    : TokenType.Print,
    'function' : TokenType.Function,
    'let'      : TokenType.Let,
    'in'       : TokenType.In,

    'if'       : TokenType.If,
    'elif'     : TokenType.Elif,
    'else'     : TokenType.Else,

    'true'     : TokenType.true,
    'false'    : TokenType.false,
    'is'       : TokenType.Is,
  
    'while'    : TokenType.While,
    'for'      : TokenType.For,    
    'type'     : TokenType.type,
    'inherit'  : TokenType._inherit,
    'protocol' : TokenType.protocol
}