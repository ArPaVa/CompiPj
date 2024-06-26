from astd import *
from lexer import Terminal
from parsing import AttributeGrammar, build_slr_parser

hulk_grammar = AttributeGrammar(
    list(Terminal),
    [
        ('Start', ['File']),
        ('File', ['TopLevel'], lambda s: AstFile(s[0])),
        ('File', ['TopLevel', 'Expression'], lambda s: AstFile(s[0], s[1])),
        ('File', ['TopLevel', 'Expression', Terminal.Semicolon], lambda s: AstFile(s[0], s[1])),
        ('TopLevel', ['TopLevel', 'Type'], lambda s: [*s[0], s[1]]),
        ('TopLevel', ['TopLevel', 'Function'], lambda s: [*s[0], s[1]]),
        ('TopLevel', ['TopLevel', 'Protocol'], lambda s: [*s[0], s[1]]),
        ('TopLevel', [], lambda _: []),
        ('Function', [Terminal.Function, 'Prototype', 'FunctionBlock'], lambda s: AstFunction(s[1], s[2])),
        ('Prototype', [Terminal.Identifier, Terminal.ParenL, 'Params', Terminal.ParenR, 'TypeAnnotation'],
         lambda s: AstPrototype(s[0], s[2], s[4])),
        ('Prototype', [Terminal.Identifier, Terminal.ParenL, 'Params', Terminal.ParenR],
         lambda s: AstPrototype(s[0], s[2])),
        ('FunctionBlock', ['BlockExpression'], lambda s: s[0]),
        ('FunctionBlock', [Terminal.Equal, Terminal.GreaterThan, 'Expression', Terminal.Semicolon], lambda s: s[2]),
        ('Params', ['Params', Terminal.Comma, 'Binding'], lambda s: [*s[0], s[2]]),
        ('Params', ['Binding'], lambda s: s),
        ('Params', [], lambda _: []),
        ('Binding', [Terminal.Identifier, 'TypeAnnotation'], lambda s: AstBinding(s[0], s[1])),
        ('Binding', [Terminal.Identifier], lambda s: AstBinding(s[0])),
        ('TypeAnnotation', [Terminal.Colon, Terminal.Identifier], lambda s: s[1]),
        ('Type', [Terminal.Type, 'Constructor', 'Inheritance', 'TypeBlock'], lambda s: AstType(s[1], s[3], s[2])),
        ('Type', [Terminal.Type, 'Constructor', 'TypeBlock'], lambda s: AstType(s[1], s[2])),
        ('Constructor', [Terminal.Identifier, Terminal.ParenL, 'Params', Terminal.ParenR],
         lambda s: AstPrototype(s[0], s[2])),
        ('Constructor', [Terminal.Identifier], lambda s: s[0]),
        ('Inheritance', [Terminal.Inherit, 'BaseType'], lambda s: s[1]),
        ('BaseType', [Terminal.Identifier], lambda s: s[0]),
        ('BaseType', ['CallExpression'], lambda s: s[0]),
        ('TypeBlock', [Terminal.BraceL, 'Members', Terminal.BraceR], lambda s: s[1]),
        ('Members', ['Members', 'Assignment', Terminal.Semicolon], lambda s: [*s[0], s[1]]),
        ('Members', ['Members', 'Prototype', 'FunctionBlock'], lambda s: [*s[0], AstFunction(s[1], s[2])]),
        ('Members', [], lambda _: []),
        ('Assignment', ['Binding', Terminal.Equal, 'Expression'], lambda s: AstAssignment(s[0], s[2])),
        ('Protocol', [Terminal.Protocol, Terminal.Identifier, 'Extends', 'ProtocolBlock'],
         lambda s: AstProtocol(s[1], s[3], s[2])),
        ('Protocol', [Terminal.Protocol, Terminal.Identifier, 'ProtocolBlock'], lambda s: AstProtocol(s[1], s[2])),
        ('Extends', [Terminal.Extends, Terminal.Identifier], lambda s: s[1]),
        ('ProtocolBlock', [Terminal.BraceL, 'Methods', Terminal.BraceR], lambda s: s[1]),
        ('Methods', ['Methods', 'Prototype', Terminal.Semicolon], lambda s: [*s[0], s[1]]),
        ('Methods', [], lambda _: []),
        ('Expression', ['StructuredExpression'], lambda s: s[0]),
        ('Expression', ['BasicExpression'], lambda s: s[0]),
        ('BasicExpression', ['BasicExpression', Terminal.And, 'BoolExpression'], lambda s: AstAnd(s[0], s[2])),
        ('BasicExpression', ['BasicExpression', Terminal.Or, 'BoolExpression'], lambda s: AstOr(s[0], s[2])),
        ('BasicExpression', ['BoolExpression'], lambda s: s[0]),
        ('BoolExpression', [Terminal.Not, 'BoolExpression'], lambda s: AstNot(s[1])),
        ('BoolExpression', ['Predicate'], lambda s: s[0]),
        ('Predicate', ['ArithExpression', Terminal.LessThan, 'ArithExpression'], lambda s: AstLessThan(s[0], s[2])),
        ('Predicate', ['ArithExpression', Terminal.LessThan, Terminal.Equal, 'ArithExpression'],
         lambda s: AstLessEqual(s[0], s[3])),
        ('Predicate', ['ArithExpression', Terminal.GreaterThan, 'ArithExpression'],
         lambda s: AstGreaterThan(s[0], s[2])),
        ('Predicate', ['ArithExpression', Terminal.GreaterThan, Terminal.Equal, 'ArithExpression'],
         lambda s: AstGreaterEqual(s[0], s[3])),
        ('Predicate', ['ArithExpression', Terminal.Not, Terminal.Equal, 'ArithExpression'],
         lambda s: AstNotEqual(s[0], s[3])),
        ('Predicate', ['ArithExpression', Terminal.Equal, Terminal.Equal, 'ArithExpression'],
         lambda s: AstEqual(s[0], s[3])),
        ('Predicate', ['TypeTestExpression'], lambda s: s[0]),
        ('Predicate', ['ArithExpression'], lambda s: s[0]),
        ('ArithExpression', ['ArithExpression', Terminal.Plus, 'Term'], lambda s: AstAdd(s[0], s[2])),
        ('ArithExpression', ['ArithExpression', Terminal.Sub, 'Term'], lambda s: AstSub(s[0], s[2])),
        ('ArithExpression', ['ArithExpression', Terminal.At, Terminal.At, 'Term'],
         lambda s: AstStringConcat(s[0], s[3], True)),
        ('ArithExpression', ['ArithExpression', Terminal.At, 'Term'], lambda s: AstStringConcat(s[0], s[2])),
        ('ArithExpression', ['Term'], lambda s: s[0]),
        ('Term', ['Term', Terminal.Star, 'UnarySub'], lambda s: AstMul(s[0], s[2])),
        ('Term', ['Term', Terminal.Div, 'UnarySub'], lambda s: AstDiv(s[0], s[2])),
        ('Term', ['Term', Terminal.Rem, 'UnarySub'], lambda s: AstRem(s[0], s[2])),
        ('Term', ['UnarySub'], lambda s: s[0]),
        ('UnarySub', [Terminal.Sub, 'Factor'], lambda s: AstUnarySub(s[1])),
        ('UnarySub', ['Factor'], lambda s: s[0]),
        ('Factor', ['PrimitiveExpression', Terminal.Pow, 'UnarySub'], lambda s: AstPow(s[0], s[2])),
        ('Factor', ['PrimitiveExpression'], lambda s: s[0]),
        ('StructuredExpression', ['BlockExpression'], lambda s: s[0]),
        ('StructuredExpression', ['LetExpression'], lambda s: s[0]),
        ('StructuredExpression', ['ConditionalExpression'], lambda s: s[0]),
        ('StructuredExpression', ['WhileExpression'], lambda s: s[0]),
        ('StructuredExpression', ['ForExpression'], lambda s: s[0]),
        ('StructuredExpression', ['DowncastExpression'], lambda s: s[0]),
        ('StructuredExpression', ['DestructiveAssignment'], lambda s: s[0]),
        ('BlockExpression', [Terminal.BraceL, 'ExpressionList', Terminal.BraceR, Terminal.Semicolon],
         lambda s: AstBlockExpression(s[1])),
        ('BlockExpression', [Terminal.BraceL, 'ExpressionList', Terminal.BraceR], lambda s: AstBlockExpression(s[1])),
        ('BlockExpression', [Terminal.BraceL, 'ExpressionList', Terminal.Semicolon, Terminal.BraceR],
         lambda s: AstBlockExpression(s[1])),
        ('ExpressionList', ['ExpressionList', Terminal.Semicolon, 'Expression'], lambda s: [*s[0], s[2]]),
        ('ExpressionList', ['Expression'], lambda s: s),
        ('ExpressionList', [], lambda _: []),
        ('LetExpression', [Terminal.Let, 'AssignmentList', Terminal.In, 'Expression'],
         lambda s: AstLetExpression(s[1], s[3])),
        ('AssignmentList', ['AssignmentList', Terminal.Comma, 'Assignment'], lambda s: [*s[0], s[2]]),
        ('AssignmentList', ['Assignment'], lambda s: s),
        ('DestructiveAssignment', ['Access', Terminal.Colon, Terminal.Equal, 'Expression'],
         lambda s: AstDestructiveAssignment(s[0], s[3])),
        ('ConditionalExpression',
         [Terminal.If, Terminal.ParenL, 'Expression', Terminal.ParenR, 'Expression', 'ChainedConditional'],
         lambda s: AstBranch(s[2], s[4], s[5])),
        ('ChainedConditional',
         [Terminal.Elif, Terminal.ParenL, 'Expression', Terminal.ParenR, 'Expression', 'ChainedConditional'],
         lambda s: AstBranch(s[2], s[4], s[5])),
        ('ChainedConditional', [Terminal.Else, 'Expression'], lambda s: s[1]),
        ('WhileExpression', [Terminal.While, Terminal.ParenL, 'Expression', Terminal.ParenR, 'Expression'],
         lambda s: AstWhileExpression(s[2], s[4])),
        ('ForExpression', [Terminal.For, Terminal.ParenL, 'Iterator', Terminal.ParenR, 'Expression'],
         lambda s: AstForExpression(s[2], s[4])),
        ('Iterator', ['Binding', Terminal.In, 'Expression'], lambda s: AstIterator(s[0], s[2])),
        ('TypeTestExpression', ['ArithExpression', Terminal.Is, Terminal.Identifier],
         lambda s: AstTypeTest(s[0], s[2])),
        ('DowncastExpression', ['ArithExpression', Terminal.As, Terminal.Identifier],
         lambda s: AstDowncast(s[0], s[2])),
        ('TypeInstantiation', [Terminal.New, Terminal.Identifier, Terminal.ParenL, 'Arguments', Terminal.ParenR],
         lambda s: AstTypeInstantiation(s[1], s[3])),
        ('Arguments', ['Arguments', Terminal.Comma, 'Expression'], lambda s: [*s[0], s[2]]),
        ('Arguments', ['Expression'], lambda s: s),
        ('Arguments', [], lambda _: []),
        ('PrimitiveExpression', [Terminal.ParenL, 'Expression', Terminal.ParenR], lambda s: s[1]),
        ('PrimitiveExpression', [Terminal.Number], lambda s: AstNumericLiteral(s[0])),
        ('PrimitiveExpression', [Terminal.String], lambda s: AstStringLiteral(s[0])),
        ('PrimitiveExpression', ['TypeInstantiation'], lambda s: s[0]),
        ('PrimitiveExpression', ['VectorLiteral'], lambda s: s[0]),
        ('PrimitiveExpression', ['CallExpression'], lambda s: s[0]),
        ('PrimitiveExpression', ['BoolLiteral'], lambda s: s[0]),
        ('PrimitiveExpression', ['Access'], lambda s: s[0]),
        ('BoolLiteral', [Terminal.true], lambda s: AstBoolLiteral(True)),
        ('BoolLiteral', [Terminal.false], lambda s: AstBoolLiteral(False)),
        ('VectorLiteral', [Terminal.BracketL, 'Arguments', Terminal.BracketR], lambda s: AstVectorLiteral(s[1])),
        ('VectorLiteral', [Terminal.BracketL, 'Expression', Terminal.Comprehension, 'Iterator', Terminal.BracketR],
         lambda s: AstVectorComprehension(s[1], s[3])),
        ('CallExpression', ['Access', Terminal.ParenL, 'Arguments', Terminal.ParenR],
         lambda s: AstCallExpression(s[0], s[2])),
        ('Access', ['Access', Terminal.Dot, Terminal.Identifier], lambda s: AstAccess(s[2], s[0])),
        ('Access', ['Access', Terminal.BracketL, 'Expression', Terminal.BracketR],
         lambda s: AstIndexAccess(s[0], s[2])),
        ('Access', [Terminal.Identifier], lambda s: AstAccess(s[0])),
    ])

hulk_parse = build_slr_parser(hulk_grammar, key=lambda t: t.type)
