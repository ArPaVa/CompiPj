import math
import random

from ast import *
from lexer import Token, Terminal
from scope import Scope

global_scope = Scope({
    'E': math.e,
    'PI': math.pi,
    'sqrt': math.sqrt,
    'sin': math.sin,
    'cos': math.cos,
    'exp': math.exp,
    'log': math.log,
    'rand': random.random,
    'print': print,
    'Number': float,
    'String': str,
    'Object': object,
    'Bool': bool,
    'Unit': type(None),
    'Vector': list
})


class Func:

    # noinspection PyShadowingNames
    def __init__(self, runtime, name, resolved_type, params, block):
        self.name = name
        self.runtime = runtime
        self.resolved_type = resolved_type
        self.closure = runtime.scope
        self.params = params
        self.block = block

    def __call__(self, *args, **kwargs):
        local = self.runtime.scope
        self.runtime.scope = Scope(parent=self.closure)

        names = [param.accept(self.runtime) for param in self.params]

        for i in range(len(args)):
            self.runtime.scope[names[i]] = args[i]

        if '#super' in self.closure.local and self.name in self.closure['#super'].attrs.local:
            self.runtime.scope.bind('base', self.closure['#super'].attrs[self.name])

        result = self.block.accept(self.runtime)
        self.runtime.scope = local

        return result


class Type:

    # noinspection PyShadowingNames
    def __init__(self, runtime, constructor, block, inherit):
        self.block = block
        self.runtime = runtime
        self.constructor = constructor
        self.supertype = None
        self.super_args = []

        if isinstance(constructor, AstPrototype):
            self.name = constructor.name
        else:
            self.name = constructor.lexeme

        if inherit:
            if isinstance(inherit, AstCallExpression):
                self.supertype = inherit.binding.accept(self.runtime)
                self.super_args = inherit.args
            else:
                self.supertype = self.runtime.scope[inherit.lexeme]

    def __call__(self, *args, **kwargs):
        local = self.runtime.scope
        self.runtime.scope = Scope(parent=self.runtime.scope)

        if isinstance(self.constructor, AstPrototype):
            names = [param.accept(self.runtime) for param in self.constructor.params]

            for i in range(len(args)):
                self.runtime.scope[names[i]] = args[i]

            self.runtime.scope = Scope(parent=self.runtime.scope)

        if self.supertype:
            supertype = self.supertype(*[arg.accept(self.runtime) for arg in self.super_args])
            self.runtime.scope = Scope(parent=supertype.attrs)
            self.runtime.scope.bind('#super', supertype)

        instance = HulkObject(self.runtime.scope, self)
        self.runtime.scope.bind('self', instance)

        for member in self.block:
            member.accept(self.runtime)

        self.runtime.scope = local
        return instance

    def __instancecheck__(self, instance):
        return self.__subclasscheck__(instance.type)

    def __subclasscheck__(self, subclass):
        return subclass is self or self.__subclasscheck__(subclass.supertype) \
            if subclass.supertype else False


class Protocol:

    def __init__(self, runtime, methods, extends):
        self.runtime = runtime
        self.methods = methods
        self.extends = extends

    def __instancecheck__(self, instance):
        if isinstance(instance, list):
            return True

        for name, return_type, param_types in self.methods:
            if name not in instance.attrs.local:
                return False

            subclass_method = instance.attrs[name]
            if not isinstance(subclass_method, Func):
                return False

            resolved_return_type = self.runtime.scope[return_type.lexeme] \
                if return_type else object

            if not issubclass(subclass_method.resolved_type.return_type, resolved_return_type):
                return False

            if len(subclass_method.resolved_type.param_types) != len(param_types):
                return False

            for i in range(len(param_types)):
                resolved_param_type = self.runtime.scope[param_types[i].lexeme] \
                    if param_types[i] else object

                if not issubclass(resolved_param_type, subclass_method.resolved_type.param_types[i]):
                    return False

        if self.extends:
            extends = self.runtime.scope[self.extends.lexeme]
            return extends.__instancecheck__(instance)

        return True


class HulkObject:

    # noinspection PyShadowingBuiltins
    def __init__(self, attrs, type):
        self.attrs = attrs
        self.type = type


# noinspection PyPep8Naming
class Runtime:

    def __init__(self, scope):
        self.scope = scope

    def visit_AstFile(self, node: AstFile):
        for _node in node.list:
            _node.accept(self)

        if node.main:
            return node.main.accept(self)

    def visit_AstFunction(self, node: AstFunction):
        name, params, _ = node.prototype.accept(self)
        # noinspection PyUnresolvedReferences,PyProtectedMember
        self.scope.bind(name, Func(self, name, node._resolved_type, params, node.block))

    @staticmethod
    def visit_AstPrototype(node: AstPrototype):
        return node.name, node.params, node.type_annotation

    def visit_AstType(self, node: AstType):
        # noinspection PyShadowingBuiltins
        type = Type(self, node.constructor, node.block, node.inherit)
        self.scope.bind(type.name, type)

    def visit_AstProtocol(self, node: AstProtocol):
        methods = []

        for prototype in node.block:
            name, params, type_annotation = prototype.accept(self)
            methods.append((name, type_annotation, [param.type_annotation for param in params]))

        protocol = Protocol(self, methods, node.extends)
        self.scope.bind(node.name, protocol)

    @staticmethod
    def visit_AstNumericLiteral(node: AstNumericLiteral):
        return node.value

    @staticmethod
    def visit_AstBoolLiteral(node: AstBoolLiteral):
        return node.value

    @staticmethod
    def visit_AstStringLiteral(node: AstStringLiteral):
        return node.value

    def visit_AstVectorLiteral(self, node: AstVectorLiteral):
        return self.scope['Vector']([element.accept(self) for element in node.list])

    def visit_AstAdd(self, node: AstAdd):
        return node.left.accept(self) + node.right.accept(self)

    def visit_AstSub(self, node: AstSub):
        return node.left.accept(self) - node.right.accept(self)

    def visit_AstStringConcat(self, node: AstStringConcat):
        return str(node.left.accept(self)) + (' ' if node.extra else '') + str(node.right.accept(self))

    def visit_AstMul(self, node: AstMul):
        return node.left.accept(self) * node.right.accept(self)

    def visit_AstDiv(self, node: AstDiv):
        return node.left.accept(self) / node.right.accept(self)

    def visit_AstRem(self, node: AstRem):
        return node.left.accept(self) % node.right.accept(self)

    def visit_AstPow(self, node: AstPow):
        return node.left.accept(self) ** node.right.accept(self)

    def visit_AstAnd(self, node: AstAnd):
        return node.left.accept(self) and node.right.accept(self)

    def visit_AstOr(self, node: AstOr):
        return node.left.accept(self) or node.right.accept(self)

    def visit_AstUnarySub(self, node: AstUnarySub):
        return - node.operand.accept(self)

    def visit_AstNot(self, node: AstNot):
        return not node.operand.accept(self)

    def visit_AstLessThan(self, node: AstLessThan):
        return node.left.accept(self) < node.right.accept(self)

    def visit_AstLessEqual(self, node: AstLessEqual):
        return node.left.accept(self) <= node.right.accept(self)

    def visit_AstGreaterThan(self, node: AstGreaterThan):
        return node.left.accept(self) > node.right.accept(self)

    def visit_AstGreaterEqual(self, node: AstGreaterEqual):
        return node.left.accept(self) >= node.right.accept(self)

    def visit_AstNotEqual(self, node: AstNotEqual):
        return node.left.accept(self) != node.right.accept(self)

    def visit_AstEqual(self, node: AstEqual):
        return node.left.accept(self) == node.right.accept(self)

    def visit_AstWhileExpression(self, node: AstWhileExpression):
        result = None
        while node.expr.accept(self):
            result = node.block.accept(self)
        return result

    def visit_AstBranch(self, node: AstBranch):
        if node.expr.accept(self):
            return node.then.accept(self)
        # noinspection PyProtectedMember
        return node._else.accept(self)

    def visit_AstBlockExpression(self, node: AstBlockExpression):
        result = None
        for expr in node.list:
            result = expr.accept(self)
        return result

    def visit_AstLetExpression(self, node: AstLetExpression):
        local = self.scope

        for assignment in node.assignment_list:
            self.scope = Scope(parent=self.scope)
            assignment.accept(self)

        result = node.expr.accept(self)
        self.scope = local

        return result

    @staticmethod
    def visit_AstBinding(node: AstBinding):
        return node.name  # , node.type_annotation

    def visit_AstIterator(self, node: AstIterator):
        return node.binding.accept(self), node.expr.accept(self)

    def visit_AstForExpression(self, node: AstForExpression):
        name, iterator = node.iterator.accept(self)

        result = None
        self.scope = Scope(parent=self.scope)

        if isinstance(iterator, list):
            for element in iterator:
                self.scope[name] = element
                result = node.expr.accept(self)
            return result

        binding = f'#iter{id(node)}'
        cond = AstCallExpression(AstAccess(Token(-1, -1, Terminal.Identifier, 'next'),
                                           AstAccess(Token(-1, -1, Terminal.Identifier, binding))), [])

        block = AstLetExpression([
            AstAssignment(AstBinding(Token(-1, -1, Terminal.Identifier, name)),
                          AstCallExpression(AstAccess(Token(-1, -1, Terminal.Identifier, 'current'),
                                                      AstAccess(Token(-1, -1, Terminal.Identifier, binding))), []))],
            node.expr)

        self.scope.bind(binding, iterator)

        while cond.accept(self):
            result = block.accept(self)

        self.scope = self.scope.parent
        return result

    def visit_AstVectorComprehension(self, node: AstVectorComprehension):
        vector = []
        name, iterator = node.iterator.accept(self)

        self.scope = Scope(parent=self.scope)

        if isinstance(iterator, list):
            for element in iterator:
                self.scope[name] = element
                vector.append(node.expr.accept(self))
            return self.scope['Vector'](vector)

        binding = f'#iter{id(node)}'
        cond = AstCallExpression(AstAccess(Token(-1, -1, Terminal.Identifier, 'next'),
                                           AstAccess(Token(-1, -1, Terminal.Identifier, binding))), [])

        block = AstLetExpression([
            AstAssignment(AstBinding(Token(-1, -1, Terminal.Identifier, name)),
                          AstCallExpression(AstAccess(Token(-1, -1, Terminal.Identifier, 'current'),
                                                      AstAccess(Token(-1, -1, Terminal.Identifier, binding))), []))],
            node.expr)

        self.scope.bind(binding, iterator)

        while cond.accept(self):
            vector.append(block.accept(self))

        self.scope = self.scope.parent
        return self.scope['Vector'](vector)

    def visit_AstAssignment(self, node: AstAssignment):
        key = node.binding.accept(self)
        value = node.expr.accept(self)
        self.scope.bind(key, value)

    def visit_AstAccess(self, node: AstAccess):
        if not node.prev:
            return self.scope[node.name]

        prev = node.prev.accept(self)
        return prev.attrs[node.name]

        # if isinstance(prev, HulkObject):
        #     return prev.attrs[node.name]
        #
        # return getattr(prev, node.name)

    def visit_AstIndexAccess(self, node: AstIndexAccess):
        index = int(node.expr.accept(self))
        vector = node.binding.accept(self)
        return vector[index]

    def visit_AstCallExpression(self, node: AstCallExpression):
        func = node.binding.accept(self)
        return func(*[arg.accept(self) for arg in node.args])

    def visit_AstTypeInstantiation(self, node: AstTypeInstantiation):
        # noinspection PyShadowingBuiltins
        type = self.scope[node.type]
        return type(*[arg.accept(self) for arg in node.args])

    def visit_AstDestructiveAssignment(self, node: AstDestructiveAssignment):
        binding = node.binding
        value = node.expr.accept(self)

        if isinstance(binding, AstIndexAccess):
            index = int(binding.expr.accept(self))
            vector = binding.binding.accept(self)
            vector[index] = value

        elif not binding.prev:
            self.scope[binding.name] = value

        else:
            prev = binding.prev.accept(self)
            prev.attrs[binding.name] = value

            # if isinstance(prev, HulkObject):
            #     prev.attrs[binding.name] = value
            #
            # else:
            #     setattr(prev, binding.name, value)

        return value

    def visit_AstDowncast(self, node: AstDowncast):
        return node.expr.accept(self)

    def visit_AstTypeTest(self, node: AstTypeTest):
        return isinstance(node.expr.accept(self), self.scope[node.type.lexeme])


default_runtime = Runtime(global_scope)
