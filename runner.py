from hulk import hulk_parse
from lexer import tokenize, Token, Terminal
from scope import RunScope, Attribute, Method, Type, Instance, Context
from m_ast import *
import math
import random

# def _range(min, max):
    
#     min = min;
#     max = max;
#     current = min - 1;

#     next(): Boolean => (self.current := self.current + 1) < max;
#     current(): Number => self.current;

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

def create_builtin_functions():

    pass
def create_builtin_type():
    pass

# noinspection PyPep8Naming,PyMethodMayBeStatic
class Runner:

    def __init__(self, builting, ctes):
        self.builting = builting
        self.scope = RunScope(parent=None)
        self.context = Context()
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
        self.scope.assign_function(name, [p.name for p in params], node.block)
        return # TODO
        
    def visit_AstProto(self, node):
        return node.name, node.args, node.type_annotation
    
    def visit_AstBinding(self, node):
        raise NotImplementedError()
    
    def visit_AstProtocolDefinition(self, node):
        raise NotImplementedError()
    
    def visit_AstTypeDefinition(self, node):
        node.constructor # AstProto(with type args) or Identifier
        node.block # type attributes + type methods(is a list)
        node.inherit # Identifier or CallExpression or None
        if isinstance(node.constructor, AstProto):
            type = self.context.create_type(node.constructor.name, [arg.name for arg in node.constructor.args])
        else: 
            type = self.context.create_type(node.constructor.lexeme)

        if node.inherit != None:
            if isinstance(node.inherit, AstCallExpr):
                type.set_parent(node.inherit.name)
                # hacer algo con los arg
            else:
                type.set_parent(node.inherit)

        for member in node.block:
            # member is a AstAssignment or a AstFunction
            if isinstance(member, AstAssignment):
                if not isinstance(node.constructor, AstProto):
                    type.define_attribute(member.name.name, member.expr.accept(self))
                else:
                    type.define_attribute(member.name.name, member.expr)

            if isinstance(member, AstFunction):
                type.define_method(member.proto.name, [arg.name for arg in member.proto.args], member.block)


        return # TODO
    
    def visit_AstAssignment(self, node): # let
        vname = node.name.name
        vvalue = node.expr.accept(self)
        self.scope.assign_variable(vname, vvalue)
        return vvalue    
    
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
            ret = expr.accept(self)
        return ret
        
    def visit_AstLetExpr(self, node):
        scopes = [self.scope]
        for assig in node.assignment_list:
            scopes.append(scopes[-1].create_child_scope())
            self.scope = scopes[-1]
            assig.accept(self)
        value = node.expr.accept(self)
        self.scope = scopes[0]
        return value
        
    def visit_AstDestructiveAssignment(self, node):
        # node.name is an Access. Meaning a AstAccess or AstIndexAccess
        vvalue = node.expr.accept(self)
        access = node.name
        if access.calling == None:
            # Then access.source is an Identifier
            vname = access.source.lexeme
            self.scope.assign_variable_destructive(vname, vvalue)
            return vvalue
        access_source = access.source
        if isinstance(access.calling, AstCallExpr):
            raise Exception(f"The destructive assignment cannot be applied to a function or method")
        if isinstance(access.calling, Token):
            # only possible if access_source is self
            ok, instance, inst_scope = self.scope.get_variable_info('self')
            if ok:
                inst_scope.assign_variable_destructive(access.calling.lexeme, vvalue)
                return vvalue
        raise Exception(f"The destructive assignment cannot be applied in this circumstance")

        
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
        # let iterable = range(0, 10) in
        # while (iterable.next())
        #     let x = iterable.current() in
        #         print(x);
        iter = Token(0,0,Terminal.Identifier,"0iterable")
        next = Token(0,0,Terminal.Identifier,"next")
        current = Token(0,0,Terminal.Identifier,"current")

        for_scope = self.scope.create_child_scope()
        for_scope.assign_variable("0iterable", node.iterator.expr) #.accept(self)
        iternext = AstAccess(AstCallExpr(next,[]), iter)
        itercurrent = AstAccess(AstCallExpr(current,[]), iter)
        self.scope = for_scope
        while iternext.accept(self):
            let_scope = for_scope.create_child_scope()
            let_scope.assign_variable(node.iterator.name, itercurrent) 
            self.scope = let_scope
            ret = node.expr.accept(self)
        self.scope = for_scope.parent
        return ret
    
    def visit_AstIterator(self, node): #TODO
        raise NotImplementedError()
    
    def visit_AstDowncast(self, node): #TODO
        raise NotImplementedError()
    
    def visit_AstTypeInstantiation(self, node): #TODO
        type: Type = self.context.get_type(node.type)
        inst = Instance(type, self.scope.get_global_scope(), self, None if len(node.params)==0 else node.params)
        return inst
    
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
    
    def visit_AstTypeTest(self, node): #TODO
        raise NotImplementedError()
    
    def visit_AstNumericLiteral(self, node):
        return node.value

    def visit_AstStringLiteral(self, node):
        return node.value
    
    def visit_AstAccess(self, node):
        if node.calling == None:
            # Then node.source is an Identifier, the it is a type instance
            ok, instance, var_scope = self.scope.get_variable_info(node.source.lexeme)
            if ok:
                return instance
            raise Exception(f"The variable {node.source.lexeme} is not defined")

        # node.source is an AstAccess and node.calling is a AstCallExpr or an Identifier
        instance:Instance = node.source.accept(self)

        if isinstance(node.calling, AstCallExpr):
            return instance.call_method(node.calling.name, node.calling.params, self)
        if isinstance(node.calling, Token):
            return instance.get_atrribute((node.calling.lexeme))
        # TODO what are the other cases?

runner = Runner(builting, ctes)
root = hulk_parse(tokenize("""

    type Point(x, y) {
    x = x;
    y = y;

    getX() => self.x;
    getY() => y;

    setX(x) {self.x := x;}

    setY(y) {self.y := y;}

    }

    function tan(x) => sin(x) / cos(x);
    function operate(x, y) {
        print(x + y);
        print(x - y);
        print(x * y);
        print(x / y);
    }
    function show(x, y) => "(" @ x @ ", " @ y @ ")" ;
    
    let pt = new Point(6,4), xx = pt.setX(tan(0)) in let a = pt.getY() in print(show(pt.getX(), a));
"""))
# si una variable se llama newx da errorde parsing
root.accept(runner)
