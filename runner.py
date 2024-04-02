from hulk import hulk_parse
from lexer import tokenize
import math
import random

builting = {'print':print,
            'range':lambda x,y: range(x,y), #TODO next y current
            'sqrt' :lambda   x: math.sqrt(x),
            'sin'  :lambda   x: math.sin(x),
            'cos'  :lambda   x: math.cos(x),
            'exp'  :lambda   x: math.exp(x),
            'log'  :lambda x,y: math.log(y,x),
            'rand' :lambda    : random.uniform(0,1),
            'PI'   :math.pi,
            'E'    :math.e  #TODO Type conforming?
            }
# noinspection PyPep8Naming,PyMethodMayBeStatic
class Runner:

    def __init__(self, names):
        self.names = names

    def visit_default(self, _):
        raise NotImplementedError()

    def visit_AstRoot(self, node):
        return node.expr.accept(self)

    def visit_AstFunction(self, node):
        raise NotImplementedError()
    
    def visit_AstProto(self, node):
        raise NotImplementedError()
    
    def visit_AstBinding(self, node):
        raise NotImplementedError()
    
    def visit_AstTypeDefinition(self, node):
        raise NotImplementedError()
    
    def visit_AstAssignment(self, node):
        raise NotImplementedError()
    
    def visit_AstProtocolDefinition(self, node):
        raise NotImplementedError()
    
    def visit_AstAdd(self, node):
        return node.left.accept(self) + node.right.accept(self)
    
    def visit_AstSub(self, node):
        return node.left.accept(self) - node.right.accept(self)
    
    def visit_AstStringConcat(self, node):
        if node.extra:
            return str(node.left.accept(self)) + ' ' + str(node.right.accept(self))
        return str(node.left.accept(self)) + str(node.right.accept(self))
    
    def visit_AstProd(self, node):
        return node.left.accept(self) * node.right.accept(self)
    
    def visit_AstDiv(self, node):
        return node.left.accept(self) / node.right.accept(self)
    
    def visit_AstRem(self, node):
        return node.left.accept(self) % node.right.accept(self)
    
    def visit_AstNumericLiteral(self, node):
        return node.value

    def visit_AstUnarySub(self, node): 
        return - node.expr.accept(self) 
    
    def visit_AstPow(self, node):
        return node.left.accept(self) ** node.right.accept(self)
    
    def visit_AstBoolLiteral(self, node):
        return node.value

    def visit_AstBlockExpr(self, node): #TODO revisar
        for expr in node.expr_list:
            r = expr.accept(self)
        return r
        
    def visit_AstLetExpr(self, node):
        raise NotImplementedError()
        
    def visit_AstDestructiveAssignment(self, node):
        raise NotImplementedError()
        
    def visit_AstBranch(self, node):
        raise NotImplementedError()
        
    def visit_AstAnd(self, node):
        return node.left.accept(self) and node.right.accept(self)
    
    def visit_AstWhileExpr(self, node):
        ret = None
        while node.expr.accept(self):
            ret = node.block.accept(self)
        return ret

    def visit_AstCallExpr(self, node):
        func = self.names[node.name]
        return func(*[param.accept(self) for param in node.params])



runner = Runner(builting)
root = hulk_parse(tokenize("""
    
    print(true & true);
"""))

print(root.accept(runner))
