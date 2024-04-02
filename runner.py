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
        name, args, type_annotation = node.proto.accept(self)
        self.names[name] = None # we don't know
        return node.block.accept(self)
        
    
    def visit_AstProto(self, node):
        return node.name, node.args, node.type_annotation
    
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

    def visit_AstUnarySub(self, node): 
        return - node.expr.accept(self) 
    
    def visit_AstPow(self, node):
        return node.left.accept(self) ** node.right.accept(self)
    
    def visit_AstBlockExpr(self, node): #TODO revisar
        for expr in node.expr_list:
            r = expr.accept(self)
        return r
        
    def visit_AstLetExpr(self, node):
        raise NotImplementedError()
        
    def visit_AstDestructiveAssignment(self, node):
        raise NotImplementedError()
        
    def visit_AstBranch(self, node):
        if bool(node.expr.accept(self)):
            return node.then.accept(self)
        return node._else.accept(self)
        
    def visit_AstAnd(self, node): # TODO not working
        return bool(node.left.accept(self)) and bool(node.right.accept(self))
        
    def visit_AstOr(self, node): # TODO not working
        return bool(node.left.accept(self)) or bool(node.right.accept(self))

    def visit_AstNot(self, node): # TODO not working
        return not bool(node.predicate.accept(self))
        
    def visit_AstLessThan(self, node):
        return node.left.accept(self) < node.right.accept(self)
        
    def visit_AstLessEqual(self, node):
        return node.left.accept(self) <= node.right.accept(self)
        
    def visit_AstGreaterThan(self, node):
        return node.left.accept(self) > node.right.accept(self)
        
    def visit_AstGreaterEqual(self, node):
        return node.left.accept(self) >= node.right.accept(self)
        
    def visit_AstNotEqual(self, node):
        return node.left.accept(self) != node.right.accept(self)
        
    def visit_AstEqual(self, node):
        return node.left.accept(self) == node.right.accept(self)
    
    def visit_AstWhileExpr(self, node):
        ret = None
        while node.expr.accept(self):
            ret = node.block.accept(self)
        return ret
    
    def visit_AstForExpr(self, node): #TODO
        raise NotImplementedError()
    
    def visit_AstIterator(self, node): #TODO
        raise NotImplementedError()
    
    def visit_AstDowncast(self, node): #TODO
        raise NotImplementedError()
    
    def visit_AstTypeInstantiation(self, node): #TODO
        raise NotImplementedError()
    
    def visit_AstVectorLiteral(self, node): #TODO
        raise NotImplementedError()
    
    def visit_AstVectorComprehesion(self, node): #TODO
        raise NotImplementedError()
    
    def visit_AstCallExpr(self, node):
        func = self.names[node.name]
        return func(*[param.accept(self) for param in node.params])

    def visit_AstIndexAccess(self, node): #TODO
        raise NotImplementedError()
    
    def visit_AstBoolLiteral(self, node):
        return node.value

    def visit_AstIndexAccess(self, node): #TODO
        raise NotImplementedError()
    
    def visit_AstTypeTest(self, node): #TODO
        raise NotImplementedError()
    
    def visit_AstNumericLiteral(self, node):
        return node.value

    def visit_AstStringLiteral(self, node):
        return node.value
    
    def visit_AstAccess(self, node):
        return node.value

runner = Runner(builting)
root = hulk_parse(tokenize("""
    
    print(3 != 3);
"""))

print(root.accept(runner))
