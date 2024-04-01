from hulk import hulk_parse
from lexer import tokenize


# noinspection PyPep8Naming,PyMethodMayBeStatic
class Runner:

    def __init__(self, names):
        self.names = names

    def visit_default(self, _):
        raise NotImplementedError()

    def visit_AstRoot(self, node):
        return node.expr.accept(self)

    def visit_AstNumericLiteral(self, node):
        return node.value

    def visit_AstBoolLiteral(self, node):
        return node.value

    def visit_AstAdd(self, node):
        return node.left.accept(self) + node.right.accept(self)

    def visit_AstWhileExpr(self, node):
        ret = None
        while node.expr.accept(self):
            ret = node.block.accept(self)
        return ret

    def visit_AstCallExpr(self, node):
        func = self.names[node.name]
        return func(*[param.accept(self) for param in node.params])


runner = Runner({'print': print})
root = hulk_parse(tokenize("""
    while (true) print(1 + 1);
"""))

print(root.accept(runner))
