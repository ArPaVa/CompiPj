class AstNode:

    def accept(self, visitor):
        lookup = f'visit_{type(self).__qualname__}'
        if hasattr(visitor, lookup):
            return getattr(visitor, lookup)(self)
        return visitor.visit_default(self)


class AstRoot(AstNode):

    # noinspection SpellCheckingInspection
    def __init__(self, top_level, expr):
        self.top_level = top_level
        self.expr = expr


class AstFunction(AstNode):

    def __init__(self, proto, block):
        self.proto = proto
        self.block = block


class AstProto(AstNode):

    def __init__(self, name, args, type_annotation=None):
        self.name = name.lexeme
        self.args = args
        self.type_annotation = type_annotation


class AstBinding(AstNode):

    def __init__(self, name, type_annotation=None):
        self.name = name.lexeme
        self.type_annotation = type_annotation


class AstTypeDefinition(AstNode):

    def __init__(self, constructor, block, inherit=None):
        self.constructor = constructor
        self.block = block
        self.inherit = inherit


class AstAssignment(AstNode):

    def __init__(self, name, expr):
        self.name = name
        self.expr = expr


class AstProtocolDefinition(AstNode):

    def __init__(self, name, block, extends=None):
        self.name = name
        self.block = block
        self.extends = extends


class AstAdd(AstNode):

    def __init__(self, left, right):
        self.left = left
        self.right = right


class AstSub(AstNode):

    def __init__(self, left, right):
        self.left = left
        self.right = right


class AstStringConcat(AstNode):

    def __init__(self, left, right, extra=False):
        self.left = left
        self.right = right
        self.extra = extra


class AstProd(AstNode):

    def __init__(self, left, right):
        self.left = left
        self.right = right


class AstDiv(AstNode):

    def __init__(self, left, right):
        self.left = left
        self.right = right


class AstRem(AstNode):

    def __init__(self, left, right):
        self.left = left
        self.right = right


class AstUnarySub(AstNode):

    def __init__(self, expr):
        self.expr = expr


class AstPow(AstNode):

    def __init__(self, left, right):
        self.left = left
        self.right = right


class AstBlockExpr(AstNode):

    def __init__(self, expr_list):
        self.expr_list = expr_list


class AstLetExpr(AstNode):

    def __init__(self, assignment_list, expr):
        self.assignment_list = assignment_list
        self.expr = expr


class AstDestructiveAssignment(AstNode):

    def __init__(self, name, expr):
        self.name = name
        self.expr = expr


class AstBranch(AstNode):

    def __init__(self, expr, then, _else):
        self.expr = expr
        self.then = then
        self._else = _else


class AstAnd(AstNode):

    def __init__(self, left, right):
        self.left = left
        self.right = right


class AstOr(AstNode):

    def __init__(self, left, right):
        self.left = left
        self.right = right


class AstNot(AstNode):

    def __init__(self, predicate):
        self.predicate = predicate


class AstLessThan(AstNode):

    def __init__(self, left, right):
        self.left = left
        self.right = right


class AstLessEqual(AstNode):

    def __init__(self, left, right):
        self.left = left
        self.right = right


class AstGreaterThan(AstNode):

    def __init__(self, left, right):
        self.left = left
        self.right = right


class AstGreaterEqual(AstNode):

    def __init__(self, left, right):
        self.left = left
        self.right = right


class AstNotEqual(AstNode):

    def __init__(self, left, right):
        self.left = left
        self.right = right


class AstEqual(AstNode):

    def __init__(self, left, right):
        self.left = left
        self.right = right


class AstWhileExpr(AstNode):

    def __init__(self, expr, block):
        self.expr = expr
        self.block = block


class AstForExpr(AstNode):

    def __init__(self, iterator, expr):
        self.iterator = iterator
        self.expr = expr
        


class AstIterator(AstNode):

    def __init__(self, name, expr):
        self.name = name
        self.expr = expr


class AstDowncast(AstNode):

    # noinspection PyShadowingBuiltins
    def __init__(self, expr, type):
        self.expr = expr
        self.type = type


class AstTypeInstantiation(AstNode):

    # noinspection PyShadowingBuiltins
    def __init__(self, type, params):
        self.type = type.lexeme
        self.params = params


class AstVectorLiteral(AstNode):

    def __init__(self, elements):
        self.elements = elements


class AstVectorComprehension(AstNode):

    def __init__(self, expr, iterator):
        self.expr = expr
        self.iterator = iterator


class AstCallExpr(AstNode):

    def __init__(self, token, params):
        self.name = token.lexeme
        self.params = params


class AstIndexAccess(AstNode):

    def __init__(self, source, expr):
        self.source = source
        self.expr = expr


class AstBoolLiteral(AstNode):

    def __init__(self, value):
        self.value = value


class AstTypeTest(AstNode):

    # noinspection PyShadowingBuiltins
    def __init__(self, expr, type):
        self.expr = expr
        self.type = type


class AstNumericLiteral(AstNode):

    def __init__(self, token):
        self.value = float(token.lexeme)


class AstStringLiteral(AstNode):

    def __init__(self, token):
        self.value = token.lexeme


class AstAccess(AstNode):

    def __init__(self, source, calling=None):
        self.source = source
        self.calling = calling
