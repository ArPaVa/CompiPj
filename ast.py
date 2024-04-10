class AstNode:

    def accept(self, visitor):
        lookup = 'visit_' + type(self).__name__
        if hasattr(visitor, lookup):
            return getattr(visitor, lookup)(self)
        return visitor.visit_default(self)


class AstFile(AstNode):

    # noinspection PyShadowingBuiltins
    def __init__(self, list, main=None):
        self.list = list
        self.main = main


class AstFunction(AstNode):

    def __init__(self, prototype, block):
        self.prototype = prototype
        self.block = block


class AstPrototype(AstNode):

    def __init__(self, name, params, type_annotation=None):
        self.name = name.lexeme
        self.params = params
        self.type_annotation = type_annotation


class AstBinding(AstNode):

    def __init__(self, name, type_annotation=None):
        self.name = name.lexeme
        self.type_annotation = type_annotation


class AstType(AstNode):

    def __init__(self, constructor, block, inherit=None):
        self.constructor = constructor
        self.block = block
        self.inherit = inherit


class AstAssignment(AstNode):

    def __init__(self, binding, expr):
        self.binding = binding
        self.expr = expr


class AstProtocol(AstNode):

    def __init__(self, name, block, extends=None):
        self.name = name.lexeme
        self.block = block
        self.extends = extends


class AstBinaryOp(AstNode):

    def __init__(self, left, right):
        self.left = left
        self.right = right


class AstAdd(AstBinaryOp):
    pass


class AstSub(AstBinaryOp):
    pass


class AstMul(AstBinaryOp):
    pass


class AstDiv(AstBinaryOp):
    pass


class AstRem(AstBinaryOp):
    pass


class AstPow(AstBinaryOp):
    pass


class AstAnd(AstBinaryOp):
    pass


class AstOr(AstBinaryOp):
    pass


class AstLessThan(AstBinaryOp):
    pass


class AstLessEqual(AstBinaryOp):
    pass


class AstGreaterThan(AstBinaryOp):
    pass


class AstGreaterEqual(AstBinaryOp):
    pass


class AstNotEqual(AstBinaryOp):
    pass


class AstEqual(AstBinaryOp):
    pass


class AstUnaryOp(AstNode):

    def __init__(self, operand):
        self.operand = operand


class AstUnarySub(AstUnaryOp):
    pass


class AstNot(AstUnaryOp):
    pass


class AstAccess(AstNode):

    def __init__(self, name, prev=None):
        self.name = name.lexeme
        self.prev = prev


class AstStringLiteral(AstNode):

    def __init__(self, literal):
        self.value = literal.lexeme


class AstNumericLiteral(AstNode):

    def __init__(self, literal):
        self.value = float(literal.lexeme)


class AstBoolLiteral(AstNode):

    def __init__(self, value):
        self.value = value


class AstExpressionList(AstNode):

    # noinspection PyShadowingBuiltins
    def __init__(self, list):
        self.list = list


class AstVectorLiteral(AstExpressionList):
    pass


class AstBlockExpression(AstExpressionList):
    pass


class AstStringConcat(AstBinaryOp):

    def __init__(self, left, right, extra=False):
        super().__init__(left, right)
        self.extra = extra


class AstLetExpression(AstNode):

    def __init__(self, assignment_list, expr):
        self.assignment_list = assignment_list
        self.expr = expr


class AstDestructiveAssignment(AstNode):

    def __init__(self, binding, expr):
        self.binding = binding
        self.expr = expr


class AstBranch(AstNode):

    def __init__(self, expr, then, _else):
        self.expr = expr
        self.then = then
        self._else = _else


class AstWhileExpression(AstNode):

    def __init__(self, expr, block):
        self.expr = expr
        self.block = block


class AstForExpression(AstNode):

    def __init__(self, iterator, expr):
        self.iterator = iterator
        self.expr = expr


class AstIterator(AstNode):

    def __init__(self, binding, expr):
        self.binding = binding
        self.expr = expr


class AstDowncast(AstNode):

    # noinspection PyShadowingBuiltins
    def __init__(self, expr, type):
        self.expr = expr
        self.type = type


class AstTypeInstantiation(AstNode):

    # noinspection PyShadowingBuiltins
    def __init__(self, type, args):
        self.type = type.lexeme
        self.args = args


class AstCallExpression(AstNode):

    def __init__(self, binding, args):
        self.binding = binding
        self.args = args


class AstTypeTest(AstNode):

    # noinspection PyShadowingBuiltins
    def __init__(self, expr, type):
        self.expr = expr
        self.type = type


class AstIndexAccess(AstNode):

    def __init__(self, binding, expr):
        self.binding = binding
        self.expr = expr


class AstVectorComprehension(AstNode):

    def __init__(self, expr, iterator):
        self.expr = expr
        self.iterator = iterator
