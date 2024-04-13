from ast import *
from scope import Scope


class HulkSemanticError(Exception):
    pass


# noinspection PyPep8Naming
class SemanticChecker:

    def __init__(self):
        self.context = Scope()

    def visit_default(self, _):
        pass

    def visit_AstFile(self, node: AstFile):
        for _node in node.list:
            _node.accept(self)

    def visit_AstType(self, node: AstType):
        if isinstance(node.constructor, AstPrototype):
            params = [param.name for param in node.constructor.params]

            if 'self' in params:
                raise HulkSemanticError('\'self\' is an illegal parameter name in a type constructor')

            if len(params) != len(set(params)):
                raise HulkSemanticError(f'Duplicated parameter name in {node.constructor.name}')

        supertype = None

        if node.inherit:
            if isinstance(node.inherit, AstCallExpression):
                binding = node.inherit.binding

                if binding.prev:
                    raise HulkSemanticError('There are no modules in hulk, nor inner types (yet?)')

                supertype = binding.name
            else:
                supertype = node.inherit.lexeme

        if supertype in ['Number', 'String', 'Vector', 'Bool', 'Object', 'Unit']:
            raise HulkSemanticError(f'Cannot inherit from builtin type {supertype}')

        for member in node.block:
            self.context['inside_type_block'] = True
            member.accept(self)

    def visit_AstFunction(self, node: AstFunction):
        params = [param.name for param in node.prototype.params]

        if len(params) != len(set(params)):
            raise HulkSemanticError(f'Duplicated parameter name in {node.prototype.name}')

        local = self.context
        if 'inside_type_block' in self.context.local and 'self' not in params:
            self.context = Scope(local={'self_assignment_illegal': True})
            self.context['self_assignment_illegal'] = True

        node.block.accept(self)
        self.context = local

    def visit_AstDestructiveAssignment(self, node: AstDestructiveAssignment):
        if 'self_assignment_illegal' in self.context.local:
            if not node.binding.prev and node.binding.name == 'self':
                raise HulkSemanticError('assignment to plain \'self\' inside type block is illegal')

        node.expr.accept(self)

    def visit_AstVectorLiteral(self, node: AstVectorLiteral):
        for element in node.list:
            element.accept(self)

    def visit_AstAdd(self, node: AstAdd):
        node.left.accept(self)
        node.right.accept(self)

    def visit_AstSub(self, node: AstSub):
        node.left.accept(self)
        node.right.accept(self)

    def visit_AstStringConcat(self, node: AstStringConcat):
        node.left.accept(self)
        node.right.accept(self)

    def visit_AstMul(self, node: AstMul):
        node.left.accept(self)
        node.right.accept(self)

    def visit_AstDiv(self, node: AstDiv):
        node.left.accept(self)
        node.right.accept(self)

    def visit_AstRem(self, node: AstRem):
        node.left.accept(self)
        node.right.accept(self)

    def visit_AstPow(self, node: AstPow):
        node.left.accept(self)
        node.right.accept(self)

    def visit_AstAnd(self, node: AstAnd):
        node.left.accept(self)
        node.right.accept(self)

    def visit_AstOr(self, node: AstOr):
        node.left.accept(self)
        node.right.accept(self)

    def visit_AstUnarySub(self, node: AstUnarySub):
        node.operand.accept(self)

    def visit_AstNot(self, node: AstNot):
        node.operand.accept(self)

    def visit_AstLessThan(self, node: AstLessThan):
        node.left.accept(self)
        node.right.accept(self)

    def visit_AstLessEqual(self, node: AstLessEqual):
        node.left.accept(self)
        node.right.accept(self)

    def visit_AstGreaterThan(self, node: AstGreaterThan):
        node.left.accept(self)
        node.right.accept(self)

    def visit_AstGreaterEqual(self, node: AstGreaterEqual):
        node.left.accept(self)
        node.right.accept(self)

    def visit_AstNotEqual(self, node: AstNotEqual):
        node.left.accept(self)
        node.right.accept(self)

    def visit_AstEqual(self, node: AstEqual):
        node.left.accept(self)
        node.right.accept(self)

    def visit_AstWhileExpression(self, node: AstWhileExpression):
        node.expr.accept(self)
        node.block.accept(self)

    def visit_AstBranch(self, node: AstBranch):
        node.expr.accept(self)
        node.then.accept(self)
        # noinspection PyProtectedMember
        node._else.accept(self)

    def visit_AstBlockExpression(self, node: AstBlockExpression):
        for expr in node.list:
            expr.accept(self)

    def visit_AstLetExpression(self, node: AstLetExpression):
        for assignment in node.assignment_list:
            assignment.accept(self)

        node.expr.accept(self)

    def visit_AstIterator(self, node: AstIterator):
        node.expr.accept(self)

    def visit_AstForExpression(self, node: AstForExpression):
        node.iterator.accept(self)
        node.expr.accept(self)

    def visit_AstVectorComprehension(self, node: AstVectorComprehension):
        node.iterator.accept(self)
        node.expr.accept(self)

    def visit_AstAssignment(self, node: AstAssignment):
        node.expr.accept(self)

    def visit_AstIndexAccess(self, node: AstIndexAccess):
        node.expr.accept(self)

    def visit_AstCallExpression(self, node: AstCallExpression):
        for arg in node.args:
            arg.accept(self)

    def visit_AstTypeInstantiation(self, node: AstTypeInstantiation):
        for arg in node.args:
            arg.accept(self)

    def visit_AstDowncast(self, node: AstDowncast):
        node.expr.accept(self)

    def visit_AstTypeTest(self, node: AstTypeTest):
        node.expr.accept(self)


default_semantic_checker = SemanticChecker()


class Type:

    def __init__(self, name, attrs, param_types, supertype):
        self.__name__ = name
        self.attrs = attrs
        self.param_types = param_types
        self.supertype = supertype

    def __subclasscheck__(self, subclass):
        if subclass is self:
            return True

        if subclass is object:
            return True

        if subclass.supertype:
            return self.__subclasscheck__(subclass.supertype)

        return False


class Func:

    def __init__(self, return_type, param_types):
        self.return_type = return_type
        self.param_types = param_types


class VecType:

    def __init__(self, element_type):
        self.element_type = element_type
        self.attrs = {
            'next': Func(bool, []),
            'current': Func(element_type, [])
        }


class Protocol:

    def __init__(self, attrs, extends=None):
        self.attrs = attrs
        self.extends = extends

    def __subclasscheck__(self, subclass):
        for name in self.attrs.local.keys():
            if name not in subclass.attrs.local:
                return False

            method = self.attrs[name]
            subclass_method = subclass.attrs[name]

            if not isinstance(subclass_method, Func):
                return False

            if not issubclass(subclass_method.return_type, method.return_type):
                return False

            if len(subclass_method.param_types) != len(method.param_types):
                return False

            for i in range(len(method.param_types)):
                if not issubclass(method.param_types[i], subclass_method.param_types[i]):
                    return False

        if self.extends:
            return self.extends.__subclasscheck__(subclass)

        return True


global_context = Scope({
    'E': float,
    'PI': float,
    'sqrt': Func(float, [float]),
    'sin': Func(float, [float]),
    'cos': Func(float, [float]),
    'exp': Func(float, [float]),
    'log': Func(float, [float, float]),
    'rand': Func(float, []),
    'print': Func(type(None), [object]),
    'Number': float,
    'String': str,
    'Object': object,
    'Bool': bool,
    'Unit': type(None),
})


# noinspection PyPep8Naming
class TypeChecker:

    def __init__(self, context):
        self.context = context

    def visit_AstFile(self, node: AstFile):
        for _node in node.list:
            _node.accept(self)

        if node.main:
            node.main.accept(self)

    @staticmethod
    def visit_AstNumericLiteral(node: AstNumericLiteral):
        return float

    @staticmethod
    def visit_AstBoolLiteral(node: AstBoolLiteral):
        return bool

    @staticmethod
    def visit_AstStringLiteral(node: AstStringLiteral):
        return str

    def visit_AstVectorLiteral(self, node: AstVectorLiteral):
        vec = [element.accept(self) for element in node.list]

        if len(vec):
            resolved_type = vec[0]

            for i in range(len(vec)):
                if resolved_type is not vec[i]:
                    raise TypeError(f'type mismatch, all elements in a vector must be same type')

        return VecType(vec[0])

    def visit_AstAdd(self, node: AstAdd):
        left = node.left.accept(self)
        right = node.right.accept(self)
        if left is not float or right is not float:
            raise TypeError(f'illegal operation (+) between {left.__name__} and {right.__name__}')

        return float

    def visit_AstSub(self, node: AstSub):
        left = node.left.accept(self)
        right = node.right.accept(self)
        if left is not float or right is not float:
            raise TypeError(f'illegal operation (-) between {left.__name__} and {right.__name__}')

        return float

    def visit_AstStringConcat(self, node: AstStringConcat):
        left = node.left.accept(self)
        right = node.right.accept(self)

        if (left is not str and left is not float) or (right is not str and right is not float):
            raise TypeError(f'illegal operation (@) between {left.__name__} and {right.__name__}')

        return str

    def visit_AstMul(self, node: AstMul):
        left = node.left.accept(self)
        right = node.right.accept(self)
        if left is not float or right is not float:
            raise TypeError(f'illegal operation (*) between {left.__name__} and {right.__name__}')

        return float

    def visit_AstDiv(self, node: AstDiv):
        left = node.left.accept(self)
        right = node.right.accept(self)
        if left is not float or right is not float:
            raise TypeError(f'illegal operation (/) between {left.__name__} and {right.__name__}')

        return float

    def visit_AstRem(self, node: AstRem):
        left = node.left.accept(self)
        right = node.right.accept(self)
        if left is not float or right is not float:
            raise TypeError(f'illegal operation (%) between {left.__name__} and {right.__name__}')

        return float

    def visit_AstPow(self, node: AstPow):
        left = node.left.accept(self)
        right = node.right.accept(self)
        if left is not float or right is not float:
            raise TypeError(f'illegal operation (^) between {left.__name__} and {right.__name__}')

        return float

    def visit_AstAnd(self, node: AstAnd):
        left = node.left.accept(self)
        right = node.right.accept(self)
        if left is not bool or right is not bool:
            raise TypeError(f'illegal operation (&) between {left.__name__} and {right.__name__}')

        return bool

    def visit_AstOr(self, node: AstOr):
        left = node.left.accept(self)
        right = node.right.accept(self)
        if left is not bool or right is not bool:
            raise TypeError(f'illegal operation (|) between {left.__name__} and {right.__name__}')

        return bool

    def visit_AstUnarySub(self, node: AstUnarySub):
        op = node.operand.accept(self)
        if op is not float:
            raise TypeError(f'illegal operation (unary -) on {op.__name__}')

        return float

    def visit_AstNot(self, node: AstNot):
        op = node.operand.accept(self)
        if op is not bool:
            raise TypeError(f'illegal operation (!) on {op.__name__}')

        return bool

    def visit_AstLessThan(self, node: AstLessThan):
        left = node.left.accept(self)
        right = node.right.accept(self)
        if left is not float or right is not float:
            raise TypeError(f'illegal operation (<) between {left.__name__} and {right.__name__}')

        return bool

    def visit_AstLessEqual(self, node: AstLessEqual):
        left = node.left.accept(self)
        right = node.right.accept(self)
        if left is not float or right is not float:
            raise TypeError(f'illegal operation (<=) between {left.__name__} and {right.__name__}')

        return bool

    def visit_AstGreaterThan(self, node: AstGreaterThan):
        left = node.left.accept(self)
        right = node.right.accept(self)
        if left is not float or right is not float:
            raise TypeError(f'illegal operation (>) between {left.__name__} and {right.__name__}')

        return bool

    def visit_AstGreaterEqual(self, node: AstGreaterEqual):
        left = node.left.accept(self)
        right = node.right.accept(self)
        if left is not float or right is not float:
            raise TypeError(f'illegal operation (>=) between {left.__name__} and {right.__name__}')

        return bool

    def visit_AstNotEqual(self, node: AstNotEqual):
        left = node.left.accept(self)
        right = node.right.accept(self)
        if left is not float or right is not float:
            raise TypeError(f'illegal operation (!=) between {left.__name__} and {right.__name__}')

        return bool

    def visit_AstEqual(self, node: AstEqual):
        left = node.left.accept(self)
        right = node.right.accept(self)
        if left is not float or right is not float:
            raise TypeError(f'illegal operation (==) between {left.__name__} and {right.__name__}')

        return bool

    @staticmethod
    def visit_AstTypeTest(node: AstTypeTest):
        return bool

    def visit_AstWhileExpression(self, node: AstWhileExpression):
        cond = node.expr.accept(self)

        if cond is not bool:
            raise TypeError(f'condition must be Bool, got {cond.__name__}')

        return node.block.accept(self)

    def visit_AstBlockExpression(self, node: AstBlockExpression):
        result = None
        for expr in node.list:
            result = expr.accept(self)
        return result

    def visit_AstDestructiveAssignment(self, node: AstDestructiveAssignment):
        prev_type = node.binding.accept(self)
        resolved_type = node.expr.accept(self)

        if not issubclass(resolved_type, prev_type):
            raise TypeError(f'type mismatch, expecting {prev_type.__name__}, got {resolved_type.__name__}')

        return resolved_type

    def visit_AstIndexAccess(self, node: AstIndexAccess):
        index_type = node.expr.accept(self)

        if index_type is not float:
            raise TypeError(f'type mismatch, expecting Number, got {index_type.__name__}')

        vector_type = node.binding.accept(self)
        return vector_type.element_type

    def visit_AstType(self, node: AstType):
        local = self.context

        params = []
        resolved_type = None

        if node.inherit:
            if isinstance(node.inherit, AstCallExpression):
                supertype = node.inherit.binding.name
            else:
                supertype = node.inherit.lexeme

            resolved_type = self.context[supertype]
            self.context = Scope(parent=resolved_type.attrs)

        if isinstance(node.constructor, AstPrototype):
            type_name = node.constructor.name
            params = node.constructor.params

            for param in params:
                name, type_annotation = param.accept(self)
                self.context.bind(name, self.context[type_annotation.lexeme] if type_annotation else object)
        else:
            type_name = node.constructor.lexeme

        param_types = [param.type_annotation for param in params]
        param_types = [self.context[param_type.lexeme] if param_type else object for param_type in param_types]

        # noinspection PyShadowingBuiltins
        type = Type(type_name, self.context, param_types, resolved_type)

        self.context = Scope(parent=self.context)
        self.context.bind('self', type)

        for member in node.block:
            member.accept(self)
            type.attrs = self.context

        type.attrs = self.context
        self.context = local

        self.context.bind(type_name, type)

    def visit_AstDowncast(self, node: AstDowncast):
        return self.context[node.type.lexeme]

    def visit_AstLetExpression(self, node: AstLetExpression):
        local = self.context

        for assignment in node.assignment_list:
            self.context = Scope(parent=self.context)
            assignment.accept(self)

        result = node.expr.accept(self)
        self.context = local

        return result

    @staticmethod
    def visit_AstBinding(node: AstBinding):
        return node.name, node.type_annotation

    def visit_AstTypeInstantiation(self, node: AstTypeInstantiation):
        resolved_type = self.context[node.type]
        if not isinstance(resolved_type, Type):
            raise TypeError(f'attempting to instantiate non-existent type')

        if len(resolved_type.param_types) != len(node.args):
            raise TypeError(f'wrong number of arguments instantiating {node.type}')

        arg_types = [arg.accept(self) for arg in node.args]

        for i in range(len(arg_types)):
            if not issubclass(arg_types[i], resolved_type.param_types[i]):
                raise TypeError(f'type mismatch, expecting {resolved_type.param_types[i]}, got {arg_types[i]}')

        return resolved_type

    def visit_AstAssignment(self, node: AstAssignment):
        name, type_annotation = node.binding.accept(self)

        resolved_type = node.expr.accept(self)
        static_type = resolved_type

        if type_annotation:
            static_type = self.context[type_annotation.lexeme]

            if not issubclass(resolved_type, static_type):
                raise TypeError(f'expected {static_type.__name__}, got {resolved_type.__name__}')

        self.context.bind(name, static_type)

    def visit_AstIterator(self, node: AstIterator):
        return node.binding, node.expr.accept(self)

    def visit_AstForExpression(self, node: AstForExpression):
        binding, iterator = node.iterator.accept(self)
        name, type_annotation = binding.accept(self)

        next_method = iterator.attrs['next']
        current_method = iterator.attrs['current']

        if next_method.return_type is not bool:
            raise TypeError(f'condition must be Bool, got {next_method.return_type.__name__}')

        resolved_type = current_method.return_type
        static_type = resolved_type

        if type_annotation:
            static_type = self.context[type_annotation.lexeme]

            if not issubclass(resolved_type, static_type):
                raise TypeError(f'expected {static_type.__name__}, got {resolved_type.__name__}')

        self.context = Scope(parent=self.context)
        self.context.bind(name, static_type)

        result = node.expr.accept(self)
        self.context = self.context.parent

        return result

    def visit_AstVectorComprehension(self, node: AstVectorComprehension):
        binding, iterator = node.iterator.accept(self)
        name, type_annotation = binding.accept(self)

        next_method = iterator.attrs['next']
        current_method = iterator.attrs['current']

        if next_method.return_type is not bool:
            raise TypeError(f'condition must be Bool, got {next_method.return_type.__name__}')

        resolved_type = current_method.return_type
        static_type = resolved_type

        if type_annotation:
            static_type = self.context[type_annotation.lexeme]

            if not issubclass(resolved_type, static_type):
                raise TypeError(f'expected {static_type.__name__}, got {resolved_type.__name__}')

        self.context = Scope(parent=self.context)
        self.context.bind(name, static_type)

        result = node.expr.accept(self)
        self.context = self.context.parent

        return VecType(result)

    def visit_AstBranch(self, node: AstBranch):
        cond = node.expr.accept(self)
        then = node.then.accept(self)
        # noinspection PyProtectedMember
        else_ = node._else.accept(self)

        if cond is not bool:
            raise TypeError(f'if condition must be Bool, got {cond.__name__}')

        if then is not else_:
            return object

        return then

    def visit_AstAccess(self, node: AstAccess):
        if not node.prev:
            return self.context[node.name]

        prev = node.prev.accept(self)
        return prev.attrs[node.name]

    def visit_AstPrototype(self, node: AstPrototype):
        name, params, type_annotation = node.name, node.params, node.type_annotation

        param_types = [param.type_annotation for param in params]
        param_types = [self.context[param_type.lexeme] if param_type else object for param_type in param_types]

        self.context = Scope(parent=self.context)
        for i in range(len(params)):
            self.context.bind(params[i].name, param_types[i])
    
        static_type = self.context[type_annotation.lexeme]

        node._resolved_type = Func(static_type, param_types)
        self.context.bind(name, node._resolved_type)
        return node.name, node.params, node.type_annotation

    def visit_AstFunction(self, node: AstFunction):
        name, params, type_annotation = node.prototype.name, node.prototype.params, node.prototype.type_annotation

        param_types = [param.type_annotation for param in params]
        param_types = [self.context[param_type.lexeme] if param_type else object for param_type in param_types]

        self.context = Scope(parent=self.context)
        for i in range(len(params)):
            self.context.bind(params[i].name, param_types[i])
    
        return_type = node.block.accept(self)
        static_type = return_type

        if type_annotation:
            static_type = self.context[type_annotation.lexeme]

            if not issubclass(return_type, static_type):
                raise TypeError(f'expected {static_type.__name__}, got {return_type.__name__}')


        node._resolved_type = Func(static_type, param_types)
        self.context.bind(name, node._resolved_type)

    def visit_AstCallExpression(self, node: AstCallExpression):
        func = node.binding.accept(self)
        arg_types = [arg.accept(self) for arg in node.args]

        for i in range(len(arg_types)):
            if not issubclass(arg_types[i], func.param_types[i]):
                raise TypeError(f'type mismatch, expecting {func.param_types[i]}, got {arg_types[i]}')

        return func.return_type

    def visit_AstProtocol(self, node: AstProtocol):
        self.context = Scope(parent=self.context)

        for method in node.block:
            method.accept(self)

        extends = None
        if node.extends:
            extends = self.context[node.extends.lexeme]

        protocol = Protocol(self.context, extends)

        self.context = self.context.parent
        self.context.bind(node.name, protocol)


default_type_checker = TypeChecker(global_context)
