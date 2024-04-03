from hulk import hulk_parse
from lexer import tokenize
from scope import RunScope
import math
import random

#TODO Type conforming?
builting = {('print', 1):print,
            ('range', 2):lambda x,y: range(x,y), #TODO next y current
            ('sqrt', 1) :lambda   x: math.sqrt(x),
            ('sin', 1)  :lambda   x: math.sin(x),
            ('cos', 1)  :lambda   x: math.cos(x),
            ('exp', 1)  :lambda   x: math.exp(x),
            ('log', 2)  :lambda x,y: math.log(y,x),
            ('rand', 0) :lambda    : random.uniform(0,1),
            }
ctes = {'PI' :math.pi,
        'E'  :math.e  
        }
# noinspection PyPep8Naming,PyMethodMayBeStatic
class Runner:

    def __init__(self, builting, ctes):
        self.builting = builting
        self.scope = RunScope(parent=None)
        for fname, n in builting:
            self.scope.assign_function(fname, list(range(n)), None)
        for vname in ctes:
            self.scope.assign_variable(vname, ctes[vname])

    def visit_default(self, _):
        raise NotImplementedError()

    def visit_AstRoot(self, node):
        for definition in node.top_level:
            definition.accept(self)
        return node.expr.accept(self)

    def visit_AstFunction(self, node):
        name, params, type_annotation = node.proto.accept(self)
        self.scope.assign_function(name.lexeme, [p.name.lexeme for p in params], node.block)
        return # TODO
        
    
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
        return float(node.left.accept(self)) + float(node.right.accept(self))
    
    def visit_AstSub(self, node):
        return float(node.left.accept(self)) - float(node.right.accept(self))
    
    def visit_AstStringConcat(self, node):
        if node.extra:
            return str(node.left.accept(self)) + ' ' + str(node.right.accept(self))
        return str(node.left.accept(self)) + str(node.right.accept(self))
    
    def visit_AstProd(self, node):
        return float(node.left.accept(self)) * float(node.right.accept(self))
    
    def visit_AstDiv(self, node):
        return float(node.left.accept(self)) / float(node.right.accept(self))
    
    def visit_AstRem(self, node):
        return float(node.left.accept(self)) % float(node.right.accept(self))

    def visit_AstUnarySub(self, node): 
        return - float(node.expr.accept(self))
    
    def visit_AstPow(self, node):
        return float(node.left.accept(self)) ** float(node.right.accept(self))
    
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
        return float(node.left.accept(self)) < float(node.right.accept(self))
        
    def visit_AstLessEqual(self, node):
        return float(node.left.accept(self)) <= float(node.right.accept(self))
        
    def visit_AstGreaterThan(self, node):
        return float(node.left.accept(self)) > float(node.right.accept(self))
        
    def visit_AstGreaterEqual(self, node):
        return float(node.left.accept(self)) >= float(node.right.accept(self))
        
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
        args = node.params
        func = self.builting.get((node.name,len(args)), None)
        if func:
            return func(*[arg.accept(self) for arg in args])
        # It's not a builtin function
        ok, info = self.scope.get_function_info(node.name, len(args))
        if ok:
            params, block = info
            function_scope = self.scope.create_child_scope()
            for i in range(len(args)):
                ok = function_scope.assign_variable(params[i], args[i].accept(self))
                if not ok:
                    break

            # execute block
            global_scope = self.scope
            self.scope = function_scope
            value = block.accept(self)
            self.scope = global_scope

            return value
        
        raise Exception(f"The function {node.name} with {len(args)} parameters is not defined")

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
        ok, vvalue = self.scope.get_variable_info(node.name)
        if ok:
            return vvalue
        raise Exception(f"The variable {node.name} is not defined")

runner = Runner(builting, ctes)
root = hulk_parse(tokenize("""

    function tan(x) => sin(x) / cos(x);
    function operate(x, y) {
        print(x + y);
        print(x - y);
        print(x * y);
        print(x / y);
    }
    
    operate(4,2);
"""))

print(root.accept(runner))
