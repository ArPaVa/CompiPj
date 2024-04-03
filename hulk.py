from m_ast import *
from lexer import Terminal
from parsing import AttributeGrammar, build_slr_parser

hulk_grammar = AttributeGrammar(
    list(Terminal),
    [
        ('Start', ['HulkProgram']),
        ('HulkProgram', ['TopLevelDefinitions', 'Expression'], lambda s: AstRoot(*s)),
        ('TopLevelDefinitions', ['TopLevelDefinitions', 'TypeDefinition'], lambda s: [*s[0], s[1]]),
        ('TopLevelDefinitions', ['TopLevelDefinitions', 'FunctionDefinition'], lambda s: [*s[0], s[1]]),
        ('TopLevelDefinitions', ['TopLevelDefinitions', 'ProtocolDefinition'], lambda s: [*s[0], s[1]]),
        ('TopLevelDefinitions', [], lambda s: []),
        ('FunctionDefinition', [Terminal.Function, 'FunctionHead', 'FunctionBlock'], lambda s: AstFunction(*s[1:])),
        ('FunctionHead', [Terminal.Identifier, Terminal.ParenL, 'Arguments', Terminal.ParenR, 'TypeAnnotation'],
         lambda s: AstProto(s[0], s[2], s[4])),
        ('FunctionHead', [Terminal.Identifier, Terminal.ParenL, 'Arguments', Terminal.ParenR],
         lambda s: AstProto(s[0], s[2])),
        ('FunctionBlock', ['BlockExpression'], lambda s: s[0]),
        ('FunctionBlock', [Terminal.Equal, Terminal.GreaterThan, 'Expression', Terminal.Semicolon], lambda s: s[2]),
        ('Arguments', ['Arguments', Terminal.Comma, 'TypedIdentifier'], lambda s: [*s[0], s[2]]),
        ('Arguments', ['TypedIdentifier'], lambda s: s),
        ('Arguments', [], lambda s: []),
        ('TypedIdentifier', [Terminal.Identifier, 'TypeAnnotation'], lambda s: AstBinding(*s)),
        ('TypedIdentifier', [Terminal.Identifier], lambda s: AstBinding(*s)),
        ('TypeAnnotation', [Terminal.Colon, Terminal.Identifier], lambda s: s[1]),
        ('TypeDefinition', [Terminal.Type, 'Constructor', 'Inheritance', 'TypeBlock'],
         lambda s: AstTypeDefinition(s[1], s[3], s[2])),
        ('TypeDefinition', [Terminal.Type, 'Constructor', 'TypeBlock'], lambda s: AstTypeDefinition(*s[1:])),
        ('Constructor', [Terminal.Identifier, Terminal.ParenL, 'Arguments', Terminal.ParenR],
         lambda s: AstProto(s[0], s[2])),
        ('Constructor', [Terminal.Identifier], lambda s: s[0]),
        ('Inheritance', [Terminal.Inherit, 'BaseType'], lambda s: s[0]),
        ('BaseType', [Terminal.Identifier], lambda s: s[0]),
        ('BaseType', ['CallExpression'], lambda s: s[0]),
        ('TypeBlock', [Terminal.BraceL, 'MemberDefinitions', Terminal.BraceR], lambda s: s[1]),
        ('MemberDefinitions', ['MemberDefinitions', 'Assignment', Terminal.Semicolon], lambda s: [*s[0], s[1]]),
        ('MemberDefinitions', ['MemberDefinitions', 'FunctionHead', 'FunctionBlock', Terminal.Semicolon],
         lambda s: [*s[0], AstFunction(s[1], s[2])]),
        ('MemberDefinitions', [], lambda s: []),
        ('Assignment', ['TypedIdentifier', Terminal.Equal, 'Expression'], lambda s: AstAssignment(s[0], s[2])),
        ('ProtocolDefinition', [Terminal.Protocol, Terminal.Identifier, 'Extends', 'ProtocolBlock'],
         lambda s: AstProtocolDefinition(s[1], s[3], s[2])),
        ('ProtocolDefinition', [Terminal.Protocol, Terminal.Identifier, 'ProtocolBlock'],
         lambda s: AstProtocolDefinition(s[1], s[3])),
        ('Extends', [Terminal.Extends, Terminal.Identifier], lambda s: s[1]),
        ('ProtocolBlock', [Terminal.BraceL, 'MethodDeclarations', Terminal.BraceR], lambda s: s[1]),
        ('MethodDeclarations', ['MethodDeclarations', 'FunctionHead', Terminal.Semicolon], lambda s: [*s[0], s[1]]),
        ('MethodDeclarations', [], lambda s: []),
        ('Expression', ['Expression', Terminal.Plus, 'Term'], lambda s: AstAdd(s[0], s[2])),
        ('Expression', ['Expression', Terminal.Sub, 'Term'], lambda s: AstSub(s[0], s[2])),
        ('Expression', ['Expression', Terminal.At, Terminal.At, 'Term'], lambda s: AstStringConcat(s[0], s[2], True)),
        ('Expression', ['Expression', Terminal.At, 'Term'], lambda s: AstStringConcat(s[0], s[2])),
        ('Expression', ['StructuredExpression'], lambda s: s[0]),
        ('Expression', ['BoolExpression'], lambda s: s[0]),
        ('Expression', ['Expression', Terminal.Semicolon], lambda s: s[0]),
        ('Expression', ['Term'], lambda s: s[0]),
        ('Term', ['Term', Terminal.Prod, 'UnarySub'], lambda s: AstProd(s[0], s[2])),
        ('Term', ['Term', Terminal.Div, 'UnarySub'], lambda s: AstDiv(s[0], s[2])),
        ('Term', ['Term', Terminal.Rem, 'UnarySub'], lambda s: AstRem(s[0], s[2])),
        ('Term', ['UnarySub'], lambda s: s[0]),
        ('UnarySub', [Terminal.Sub, 'Factor'], lambda s: AstUnarySub(s[1])),
        ('UnarySub', ['Factor'], lambda s: s[0]),
        ('Factor', ['PrimitiveExpression', Terminal.Pow, 'Factor'], lambda s: AstPow(s[0], s[2])),
        ('Factor', ['PrimitiveExpression'], lambda s: s[0]),
        ('StructuredExpression', ['BlockExpression'], lambda s: s[0]),
        ('StructuredExpression', ['LetExpression'], lambda s: s[0]),
        ('StructuredExpression', ['ConditionalExpression'], lambda s: s[0]),
        ('StructuredExpression', ['WhileExpression'], lambda s: s[0]),
        ('StructuredExpression', ['ForExpression'], lambda s: s[0]),
        ('StructuredExpression', ['TypeTestExpression'], lambda s: s[0]),
        ('StructuredExpression', ['DowncastExpression'], lambda s: s[0]),
        ('StructuredExpression', ['TypeInstantiation'], lambda s: s[0]),
        ('StructuredExpression', ['DestructiveAssignment'], lambda s: s[0]),
        ('BlockExpression', [Terminal.BraceL, 'ExpressionList', Terminal.BraceR, Terminal.Semicolon],
         lambda s: AstBlockExpr(s[1])),
        ('BlockExpression', [Terminal.BraceL, 'ExpressionList', Terminal.BraceR], lambda s: AstBlockExpr(s[1])),
        ('ExpressionList', ['ExpressionList', 'Expression', Terminal.Semicolon], lambda s: [*s[0], s[1]]),
        ('ExpressionList', [], lambda s: []),
        ('LetExpression', [Terminal.Let, 'AssignmentList', Terminal.In, 'Expression'],
         lambda s: AstLetExpr(s[1], s[3])),
        ('AssignmentList', ['AssignmentList', Terminal.Comma, 'Assignment'], lambda s: [*s[0], s[2]]),
        ('AssignmentList', ['Assignment'], lambda s: s),
        ('DestructiveAssignment', [Terminal.Identifier, Terminal.Colon, Terminal.Equal, 'Expression'],
         lambda s: AstDestructiveAssignment(s[0], s[3])),
        ('ConditionalExpression',
         [Terminal.If, Terminal.ParenL, 'Expression', Terminal.ParenR, 'Expression', 'ChainedConditional'],
         lambda s: AstBranch(s[2], s[4], s[5])),
        ('BoolExpression', ['BoolExpression', Terminal.And, 'Nor'], lambda s: AstAnd(s[0], s[2])),
        ('BoolExpression', ['BoolExpression', Terminal.Or, 'Nor'], lambda s: AstOr(s[0], s[2])),
        ('BoolExpression', ['Nor'], lambda s: s[0]),
        ('Nor', [Terminal.Not, 'Predicate'], lambda s: AstNot(s[1])),
        ('Nor', ['Predicate'], lambda s: s[0]),
        ('Predicate', ['Expression', Terminal.LessThan, 'Expression'], lambda s: AstLessThan(s[0], s[2])),
        ('Predicate', ['Expression', Terminal.LessThan, Terminal.Equal, 'Expression'],
         lambda s: AstLessEqual(s[0], s[3])),
        ('Predicate', ['Expression', Terminal.GreaterThan, 'Expression'], lambda s: AstGreaterThan(s[0], s[2])),
        ('Predicate', ['Expression', Terminal.GreaterThan, Terminal.Equal, 'Expression'],
         lambda s: AstGreaterEqual(s[0], s[3])),
        ('Predicate', ['Expression', Terminal.Not, Terminal.Equal, 'Expression'], lambda s: AstNotEqual(s[0], s[3])),
        ('Predicate', ['Expression', Terminal.Equal, Terminal.Equal, 'Expression'], lambda s: AstEqual(s[0], s[3])),
        ('Predicate', ['TypeTestExpression'], lambda s: s[0]),
        ('Predicate', ['BoolLiteral'], lambda s: s[0]),
        ('ChainedConditional',
         [Terminal.Elif, Terminal.ParenL, 'Expression', Terminal.ParenR, 'Expression', 'ChainedConditional'],
         lambda s: AstBranch(s[2], s[4], s[5])),
        ('ChainedConditional', [Terminal.Else, 'Expression'], lambda s: s[1]),
        ('WhileExpression', [Terminal.While, Terminal.ParenL, 'Expression', Terminal.ParenR, 'Expression'],
         lambda s: AstWhileExpr(s[2], s[4])),
        ('ForExpression', [Terminal.For, Terminal.ParenL, 'Iterator', Terminal.ParenR, 'Expression'],
         lambda s: AstForExpr(s[2], s[4])),
        ('Iterator', ['TypedIdentifier', Terminal.In, 'Expression'], lambda s: AstIterator(s[0], s[2])),
        ('TypeTestExpression', ['Expression', Terminal.Is, Terminal.Identifier], lambda s: AstTypeTest(s[0], s[2])),
        ('DowncastExpression', ['Expression', Terminal.As, Terminal.Identifier], lambda s: AstDowncast(s[0], s[2])),
        ('TypeInstantiation', [Terminal.New, Terminal.Identifier, Terminal.ParenL, 'Params', Terminal.ParenR],
         lambda s: AstTypeInstantiation(s[1], s[3])),
        ('Params', ['Params', Terminal.Comma, 'Expression'], lambda s: [*s[0], s[2]]),
        ('Params', ['Expression'], lambda s: s),
        ('Params', [], lambda s: []),
        ('PrimitiveExpression', [Terminal.ParenL, 'Expression', Terminal.ParenR], lambda s: s[1]),
        ('PrimitiveExpression', [Terminal.Number], lambda s: AstNumericLiteral(s[0])),
        ('PrimitiveExpression', [Terminal.String], lambda s: AstStringLiteral(s[0])),
        ('PrimitiveExpression', ['VectorLiteral'], lambda s: s[0]),
        ('PrimitiveExpression', ['CallExpression'], lambda s: s[0]),
        ('PrimitiveExpression', ['Access'], lambda s: s[0]),
        ('BoolLiteral', [Terminal.true], lambda s: AstBoolLiteral(True)),
        ('BoolLiteral', [Terminal.false], lambda s: AstBoolLiteral(False)),
        ('VectorLiteral', [Terminal.BracketL, 'Params', Terminal.BracketR], lambda s: AstVectorLiteral(s[1])),
        ('VectorLiteral', [Terminal.BracketL, 'Expression', Terminal.Or, Terminal.Or, 'Iterator', Terminal.BracketR],
         lambda s: AstVectorComprehension(s[1], s[4])),
        ('CallExpression', [Terminal.Identifier, Terminal.ParenL, 'Params', Terminal.ParenR],
         lambda s: AstCallExpr(s[0], s[2])),
        ('Access', ['Access', Terminal.Dot, Terminal.Identifier], lambda s: AstAccess(s[2], s[0])),
        ('Access', ['Access', Terminal.BracketL, 'Expression', Terminal.BracketR],
         lambda s: AstIndexAccess(s[0], s[2])),
        ('Access', [Terminal.Identifier], lambda s: AstAccess(s[0])),
    ])

hulk_parse = build_slr_parser(hulk_grammar, key=lambda t: t.type)
print(Terminal.And in hulk_grammar.follows['Expression'])