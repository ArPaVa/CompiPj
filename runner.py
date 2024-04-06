from hulk import hulk_parse
from lexer import tokenize, Token, Terminal
from scope import RunScope, Attribute, Method, Protocol, Type, Instance, Context
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
            ('built_in_next', 2 ): lambda vector, idx: idx < len(vector),
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

def create_builtin_protocols():
    iterable = AstProtocolDefinition(name=Token(-1,-1,Terminal.Identifier,"Iterable"),
                                     block=[AstProto(name=Token(-1,-1,Terminal.Identifier,'next'),
                                                    args=[], type_annotation=Token(-1,-1,Terminal.Identifier,'Boolean')),
                                            AstProto(name=Token(-1,-1,Terminal.Identifier,'current'),
                                                    args=[], type_annotation=Token(-1,-1,Terminal.Identifier,'Object'))])
    return [iterable]

def create_builtin_functions():
    range_function = AstFunction(proto=AstProto(name=Token(-1,-1,Terminal.Identifier,'range'),
                                                args=[AstBinding(name=Token(-1,-1,Terminal.Identifier,'min')), 
                                                      AstBinding(name=Token(-1,-1,Terminal.Identifier,'max'))]), 
                                block=AstTypeInstantiation(type=Token(-1,-1,Terminal.Identifier,'Range'),
                                                            params=[AstAccess(source=Token(-1,-1,Terminal.Identifier, 'min')),
                                                                    AstAccess(source=Token(-1,-1,Terminal.Identifier, 'max')),]))
    return [range_function]

def create_builtin_type():
    range_type = AstTypeDefinition(constructor=AstProto(name=Token(-1,-1,Terminal.Identifier,'Range'),
                                                        args=[AstBinding(name=Token(-1,-1,Terminal.Identifier,'min'),type_annotation=Token(-1,-1,Terminal.Identifier, 'Number')),
                                                                AstBinding(name=Token(-1,-1,Terminal.Identifier,'max'),type_annotation=Token(-1,-1,Terminal.Identifier, 'Number'))]),
                                    block=[AstAssignment(name=AstBinding(name=Token(-1,-1,Terminal.Identifier,'min')), expr=AstAccess(source=Token(-1,-1,Terminal.Identifier,'min'))),
                                        AstAssignment(name=AstBinding(name=Token(-1,-1,Terminal.Identifier,'max')), expr=AstAccess(source=Token(-1,-1,Terminal.Identifier,'max'))),
                                        AstAssignment(name=AstBinding(name=Token(-1,-1,Terminal.Identifier,'current')), expr=AstSub(left=AstAccess(source=Token(-1,-1,Terminal.Identifier,'min')),
                                                                                                    right=AstNumericLiteral(Token(-1,-1,Terminal.Number, 1)))),
                                        AstFunction(proto=AstProto(name=Token(-1,-1,Terminal.Identifier,'next'),args=[],type_annotation=Token(-1,-1,Terminal.Identifier, 'Boolean')), 
                                                    block=AstLessThan(left=AstDestructiveAssignment(name=AstAccess(source=AstAccess(source=Token(-1,-1,Terminal.Identifier,'self')),
                                                                                                                    calling=Token(-1,-1,Terminal.Identifier,'current')),
                                                                                                    expr=AstAdd(left=AstAccess(source=AstAccess(source=Token(-1,-1,Terminal.Identifier,'self')),
                                                                                                                               calling=Token(-1,-1,Terminal.Identifier,'current')),
                                                                                                                right=AstNumericLiteral(Token(-1,-1,Terminal.Number, 1)))),
                                                                        right=AstAccess(source=Token(-1,-1,Terminal.Identifier,'max')))),
                                        AstFunction(proto=AstProto(name=Token(-1,-1,Terminal.Identifier,'current'),args=[],type_annotation=Token(-1,-1,Terminal.Identifier, 'Number')), 
                                                    block=AstAccess(source=AstAccess(source=Token(-1,-1,Terminal.Identifier,'self')),
                                                                    calling=Token(-1,-1,Terminal.Identifier,'current'))),
                                        ])
    vector = AstTypeDefinition(constructor=AstProto(name=Token(-1,-1,Terminal.Identifier,'Vector'),
                                                    args=[AstBinding(name=Token(-1,-1,Terminal.Identifier,'vector'))]),
                                block=[AstAssignment(name=AstBinding(name=Token(-1,-1,Terminal.Identifier,'vector')), expr=AstAccess(source=Token(-1,-1,Terminal.Identifier,'vector'))),
                                       AstAssignment(name=AstBinding(name=Token(-1,-1,Terminal.Identifier,'index')), expr=AstUnarySub(expr=AstNumericLiteral(Token(-1,-1,Terminal.Number,1)))),
                                        AstFunction(proto=AstProto(name=Token(-1,-1,Terminal.Identifier,'next'),args=[],type_annotation=Token(-1,-1,Terminal.Identifier, 'Boolean')), 
                                                    block=AstBlockExpr([AstDestructiveAssignment(name=AstAccess(source=AstAccess(source=Token(-1,-1,Terminal.Identifier,'self')),
                                                                                                                calling=Token(-1,-1,Terminal.Identifier,'index')),
                                                                                                expr=AstAdd(left=AstAccess(source=AstAccess(source=Token(-1,-1,Terminal.Identifier,'self')),
                                                                                                                               calling=Token(-1,-1,Terminal.Identifier,'index')),
                                                                                                            right=AstNumericLiteral(Token(-1,-1,Terminal.Number, 1)))),
                                                                        AstCallExpr(token=Token(-1,-1,Terminal.Identifier,'built_in_next'),
                                                                                    params=[AstAccess(source=AstAccess(source=Token(-1,-1,Terminal.Identifier,'self')),
                                                                                                    calling=Token(-1,-1,Terminal.Identifier,'vector')),
                                                                                            AstAccess(source=AstAccess(source=Token(-1,-1,Terminal.Identifier,'self')),
                                                                                                    calling=Token(-1,-1,Terminal.Identifier,'index'))
                                                                                            ])])),
                                        AstFunction(proto=AstProto(name=Token(-1,-1,Terminal.Identifier,'current'),args=[],type_annotation=Token(-1,-1,Terminal.Identifier, 'Object')), 
                                                    block=AstIndexAccess(source=AstAccess(source=AstAccess(Token(-1,-1,Terminal.Identifier,'self')),
                                                                                        calling=Token(-1,-1,Terminal.Identifier,'vector')),
                                                                        expr=AstAccess(source=Token(-1,-1,Terminal.Identifier,'index'))
                                                                        ))
                                        ])
    return [range_type, vector]

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
        for t in create_builtin_type():
            self.visit_AstTypeDefinition(t)
        for p in create_builtin_protocols():
            self.visit_AstProtocolDefinition(p)
        for f in create_builtin_functions():
            self.visit_AstFunction(f)

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
        methods = []
        for m_decl in node.block:
            methods.append((m_decl.name, [a.name for a in m_decl.args], m_decl.type_annotation.lexeme))
        return self.context.create_protocol(node.name, methods, node.extends if node.extends == None else node.extends.lexeme)
    
    def visit_AstTypeDefinition(self, node):
        node.constructor # AstProto(with type args) or Identifier
        node.block # type attributes + type methods(is a list)
        node.inherit # Identifier or CallExpression or None
        if isinstance(node.constructor, AstProto):
            type = self.context.create_type(node.constructor.name, [arg.name for arg in node.constructor.args])
        else: 
            type = self.context.create_type(node.constructor.lexeme)

        if node.inherit != None:
            parent_name = None
            parent_type_args = None
            if isinstance(node.inherit, AstCallExpr):
                # Then the parent type have type_args
                parent_name = node.inherit.name
                parent_type_args = node.inherit.params
            else:
                parent_name = node.inherit.lexeme

            type.set_parent(self.context.get_type(parent_name), parent_type_args)

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
    
    def visit_AstAssignment(self, node): 
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
    
    def visit_AstBlockExpr(self, node): 
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
        
    def visit_AstAnd(self, node): 
        return bool(node.left.accept(self)) and bool(node.right.accept(self))
        
    def visit_AstOr(self, node): 
        return bool(node.left.accept(self)) or bool(node.right.accept(self))

    def visit_AstNot(self, node): 
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
    
    def visit_AstForExpr(self, node):
        # let iterable = range(0, 10) in
        # while (iterable.next())
        #     let x = iterable.current() in
        #         // code that uses `x`

        for_scope = self.scope.create_child_scope()
        iter_inst = node.iterator.expr.accept(self)

        if isinstance(iter_inst, Instance):
            if not iter_inst.type.implents_protocol(self.context.get_protocol('Iterable')):
                raise Exception(f"A for loop only works on an instance of Iterable. {iter_inst.type} is not iterable")
        else:
            # vector??
            pass
        for_scope.assign_variable("0iterable", iter_inst)
        
        cond = AstAccess(source=AstAccess(Token(-1,-1,Terminal.Identifier,'0iterable')),
                             calling=AstCallExpr(Token(-1,-1,Terminal.Identifier,"next"),[]))
        block = AstLetExpr(assignment_list=[AstAssignment(name=AstBinding(name=Token(-1,-1,Terminal.Identifier,node.iterator.name.name)),
                                                        expr=AstAccess(source=AstAccess(Token(-1,-1,Terminal.Identifier,'0iterable')),
                                                                       calling=AstCallExpr(Token(-1,-1,Terminal.Identifier,"current"),[])) )],
                            expr=node.expr)
        self.scope = for_scope
        while cond.accept(self):
            ret = block.accept(self)
        self.scope = for_scope.parent
        return ret
    
    def visit_AstIterator(self, node): 
        # Has not been necesary until now, but in case of need to implement it, look at AstForExpr or AstVectorComprehension
        raise NotImplementedError()
    
    def visit_AstDowncast(self, node): #TODO
        raise NotImplementedError()
    
    def visit_AstTypeInstantiation(self, node): 
        type: Type = self.context.get_type(node.type)
        inst = Instance(type, self.scope.get_global_scope(), self, None if len(node.params)==0 else node.params)
        return inst
    
    def visit_AstVectorLiteral(self, node): 
        vector = []
        for elem in node.elements:
            vector.append(elem.accept(self))
        v_type: Type = self.context.get_type('Vector')
        v_instance = Instance(v_type, self.scope.get_global_scope(), self, [vector])
        return v_instance
    
    def visit_AstVectorComprehension(self, node): 
        # let iterable = rangeComprehens(0, 10) in
        # while (iterable.next())
        #     let x = iterable.current() in
        #         // code that uses `x`
        
        vector = []
        comprhs_scope = self.scope.create_child_scope()
        iter_inst = node.iterator.expr.accept(self)

        if isinstance(iter_inst, Instance):
            if not iter_inst.type.implents_protocol(self.context.get_protocol('Iterable')):
                raise Exception(f"A for loop only works on an instance of Iterable. {iter_inst.type} is not iterable")
        
        comprhs_scope.assign_variable("0iterable", iter_inst)
        
        cond = AstAccess(source=AstAccess(Token(-1,-1,Terminal.Identifier,'0iterable')),
                             calling=AstCallExpr(Token(-1,-1,Terminal.Identifier,"next"),[]))
        block = AstLetExpr(assignment_list=[AstAssignment(name=AstBinding(name=Token(-1,-1,Terminal.Identifier,node.iterator.name.name)),
                                                        expr=AstAccess(source=AstAccess(Token(-1,-1,Terminal.Identifier,'0iterable')),
                                                                       calling=AstCallExpr(Token(-1,-1,Terminal.Identifier,"current"),[])) )],
                            expr=node.expr)
        self.scope = comprhs_scope
        while cond.accept(self):
            ret = block.accept(self)
            vector.append(ret)
        self.scope = comprhs_scope.parent
        
        v_type: Type = self.context.get_type('Vector')
        v_instance = Instance(v_type, self.scope.get_global_scope(), self, [vector])
        return v_instance
    
    def visit_AstCallExpr(self, node):
        args = node.params
        func = self.builting.get((node.name,len(args)), None)
        if func:
            args_list = []
            for arg in args:
                value = arg.accept(self)
                if isinstance(value, Instance) and value.type.name == "Vector":
                    value = value.get_atrribute('vector')
                args_list.append(value)
            return func(*args_list)
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

    def visit_AstIndexAccess(self, node): 
        index = node.expr.accept(self)
        index = int(index)
        instance:Instance = node.source.accept(self)
        if isinstance(instance, list):
            return instance[index]
        
        if isinstance(instance, Instance) and instance.type.name == "Vector":
            return instance.get_atrribute('vector')[index]
    
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
            # only possible if access_source is self
            ok, inst, inst_scope = self.scope.get_variable_info('self')
            if ok:
                return instance.get_atrribute((node.calling.lexeme))
            raise Exception(f"Type attribute {node.calling.lexeme} is not accesible outside of the type")


# runner = Runner(builting, ctes)

# root = hulk_parse(tokenize("""
#     {
#         print(sin(2 * PI) ^ 2 + cos(3 * PI / log(4, 64)));
#         let newx = 1 in newx * 2;
#     }
# """))

# print(root.accept(runner))
