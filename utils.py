class Token:

    def __init__(self, line, column, _type, lexeme):
        self.line = line
        self.column = column
        self.type = _type
        self.lexeme = lexeme

from enum import Enum
TokenType = Enum('TokenType', [
    ## Main
    # Non-terminals
    'Program', 'Body', 'Exp', 'ClassList', 'Expression', 'BlockExpression', 'ExpressionList',
    'EndOfStatment', 'Value', 'ArgumentList', 'Vector', 'Explicit', 'Iterable', 'SubExp',
    # Terminals
    'semicolon', 'obrace', 'cbrace', 'opar', 'cpar', 'new', 'identifier', 'as', 'obracket',
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
    'print',
    ## StringExpression
    # Non-terminals
    'StringExpresion', 'ConcatString', 'FunctionHeader', ''
    # Terminals
    'string', 

    ## Functions
    # Non-terminals
    'Function', 'FunctionList', 'FunctionHeader', 'Params', 'TypeCheck',
    # Terminals
    'lambda', 'function',

    ## Variables
    # Non-terminals
    'LetExpression', 'AssignList', 'AfterIn', 'DestructiveExpression',
    # Terminals
    'let', 'in', 'dequal',

    ## Conditionals
    # Non-terminals
    'IfExpression', 'ConditionalExpression', 'ElseExpression', 'Nor', 'Comparable',
    # Terminals
    'if', 'elif', 'else', 'and', 'or', 'not', 'true', 'false', 'greater', 'greater_equal',
    'less', 'less_equal', 'equal_equal', 'not_equal', 'is', 

    ##Loops
    # Non-terminals
    'WhileExpression', 'ForExpression',
    # Terminals
    'while', 'for', 

    ## Types/TypesChecking
    # Non-terminals
    'TypeDeclaration', 'TypeParams', 'Inherit', 'TypeBody', 'AttributeDef', 'MethodDef', 'TypeCheck',
    # Terminals
    'type', 'inherit', 'two_dots',

    ##Protocols
    # Non-terminals
    'ProtocolDefinition', 'MethodDefList', 'ProtocolsMethods'
    # Terminals
    'protocol',
    # Non-terminals
    # Terminals
    # Terminals in this context

    # Extra
    'EOF'
])

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
    
    '&'   : TokenType.And,
    '|'   : TokenType.Or,
    '!'   : TokenType.Not,
    '>'   : TokenType.greater,
    '>='  : TokenType.greater_equal,
    '<'   : TokenType.less,
    '<='  : TokenType.less_equal,
    '!='  : TokenType.not_equal,

    ':'   : TokenType.two_dots,
    
    '\"'  : TokenType.double_quoat,
    
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
    'type'     : TokenType.Type,
    'inherit'  : TokenType.Inherit,
    'protocol' : TokenType.Protocol
}