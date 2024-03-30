class Token:

    def __init__(self, line, column, _type, lexeme):
        self.line = line
        self.column = column
        self.type = _type
        self.lexeme = lexeme
    def __str__(self) -> str:
        return f"{self.lexeme} {self.type}. ln={self.line} col={self.column}"
        #return f"{self.type}"
    def __repr__(self) -> str:
        return self.__str__()

from enum import Enum
TType = Enum('TType', [
    # Non-terminals
    'Access', 'Arguments', 'Assignment', 'AssignmentList', 'BlockExpression', 'BoolLiteral', 'BooleanExpression', 
    'CallExpression', 'ChainedConditional', 'Comparable', 'ConditionalExpression', 'Constructor', 'DestructiveAssignment', 
    'DowncastExpression', 'Expression', 'ExpressionList', 'Extends', 'Factor', 'ForExpression', 'FunctionBlock', 
    'FunctionDefinition', 'FunctionHead', 'HulkProgram', 'Identifier', 'Inheritance', 'Iterator', 'LetExpression', 
    'MemberDefinitions', 'MethodDeclarations', 'Nor', 'NumericLiteral', 'Params', 'PowBase', 'PrimitiveExpression', 
    'ProtocolBlock', 'ProtocolDefinition', 'StringLiteral', 'StructuredExpression', 'Term', 'TopLevelDefinitions', 
    'TypeAnnotation', 'TypeBlock', 'TypeDefinition', 'TypeInstantiation', 'TypeTestExpression', 'TypedIdentifier', 
    'UnarySub', 'VectorLiteral', 'WhileExpression', 

    # Terminals
    '_not', 'not_equal', 'double_quote', 'mod', '_and', 'opar', 'cpar', 'mult', 'plus', 'comma', 'minus', 'dot', 
    'div', 'two_dots', 'dequal', 'semicolon', 'less', 'less_equal', 'equal', 'equal_equal', '_lambda', 'greater', 
    'greater_equal', 'at_sign', 'double_at_sign', 'obracket', 'cbracket', 'potency', 'obrace', 'cbrace', '_or', 'generator',
    'string_chain', 'number', 'identifier', 
    '_as', '_elif', '_else', 'extends', 'false', '_for', 'function', '_if', '_in', '_inherit', '_is', 'let', '_new', 
    'protocol', 'true', 'type', '_while',

    'EOF'
])

terminal_tokens = {
    ';'   : TType.semicolon,
    '{'   : TType.obrace,
    '}'   : TType.cbrace,
    '('   : TType.opar,
    ')'   : TType.cpar,
    '['   : TType.obracket,
    ']'   : TType.cbracket,
    '||'  : TType.generator,
    ','   : TType.comma,
    '='   : TType.equal,
    '+'   : TType.plus,
    '-'   : TType.minus,
    '*'   : TType.mult,
    '/'   : TType.div,
    '%'   : TType.mod,
    '^'   : TType.potency,
    '.'   : TType.dot,    
    '=>'  : TType._lambda,
    ':='  : TType.dequal,
    '@'   : TType.at_sign,
    '@@'   : TType.double_at_sign,
    '&'   : TType._and,
    '|'   : TType._or,
    '!'   : TType._not,
    '>'   : TType.greater,
    '>='  : TType.greater_equal,
    '<'   : TType.less,
    '<='  : TType.less_equal,
    '!='  : TType.not_equal,
    '=='  : TType.equal_equal,
    ':'   : TType.two_dots,    
    '\"'  : TType.double_quote,    

    'new'      : TType._new,
    'as'       : TType._as,
    # 'print'    : TType._print,
    'function' : TType.function,
    'let'      : TType.let,
    'in'       : TType._in,

    'if'       : TType._if,
    'elif'     : TType._elif,
    'else'     : TType._else,

    'true'     : TType.true,
    'false'    : TType.false,
    'is'       : TType._is,
  
    'while'    : TType._while,
    'for'      : TType._for,    
    'type'     : TType.type,
    'inherit'  : TType._inherit,
    'protocol' : TType.protocol,
    'extends'  : TType.extends,
    # '$'   : TType.EOF, ##Not sure about the $
}

generate_hulk_terminals = [';', '{', '}', '\\(', '\\)', '\\[', '\\]', '\\|\\|', ',', '=', '\\+', '\\-', '\\*', '/', '%', 
                           '^', '.', '=>', ':=', '@', '@@', '&', '\\|', '!', '>', '>=', '<', '<=', '!=', '==', ':', #'"', 
                           'new', 'as', 'function', 'let', 'in', 'if', 'elif', 'else', 'true', 'false', 'is', 
                           'while', 'for', 'type', 'inherit', 'protocol', 'extends', '"([^"]|\"|\n\t)*"' , '[0-9]+|[0-9]*.[0-9]+', '[_a-zA-Z][_a-zA-Z0-9]*']
#generate_hulk_terminals = {'[_a-zA-Z][_a-zA-Z0-9]*'}

