from ast import *
from scope import Scope

global_context = Scope({
    'E': float,
    'PI': float,
    'sqrt': float,
    'sin': float,
    'cos': float,
    'exp': float,
    'log': float,
    'rand': float,
    'print': object,
    'import': float,
    'Number': float,
    'String': str,
    'Object': object,
    'Bool': bool
})


class Type:

    def __init__(self, attrs, param_types, supertype):
        self.attrs = attrs
        self.param_types = param_types
        self.supertype = supertype

    def __subclasscheck__(self, subclass):
        if subclass is self:
            return True

        if subclass and subclass.supertype:
            return self.__subclasscheck__(subclass.supertype)

        return False


# noinspection PyPep8Naming
class Check:

    def __init__(self, scope):
        self.scope = scope

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
        vec = [elem.accept(self) for elem in node.list]

        if len(vec):
            resolved_type = vec[0]

            for i in range(len(vec)):
                if resolved_type is not vec[i]:
                    raise TypeError(f'type mismatch, all elements in a vector must be same type')

        return vec[0]

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

        if left is not str or left is not float or right is not str or right is not float:
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

    def visit_AstDowncast(self, node: AstDowncast):
        return self.scope[node.type.lexeme]

    def visit_AstWhileExpression(self, node: AstWhileExpression):
        cond = node.expr.accept(self)

        if cond is not bool:
            raise TypeError(f'condition must be boolean, got {cond.__name__}')

        return node.block.accept(self)

    def visit_AstBlockExpression(self, node: AstBlockExpression):
        result = None
        for expr in node.list:
            result = expr.accept(self)
        return result

    def visit_AstFile(self, node: AstFile):
        for top_level in node.top_level:
            top_level.accept(self)

        if node.main:
            return node.main.accept(self)

    def visit_AstLetExpression(self, node: AstLetExpression):
        local = self.scope

        for assignment in node.assignment_list:
            self.scope = Scope(parent=self.scope)
            assignment.accept(self)

        result = node.expr.accept(self)
        self.scope = local

        return result

    def visit_AstAssignment(self, node: AstAssignment):
        name, type_annotation = node.binding.accept(self)

        resolved_type = node.expr.accept(self)
        static_type = resolved_type

        if type_annotation:
            static_type = self.scope[type_annotation.lexeme]

            if not issubclass(resolved_type, static_type):
                raise TypeError(f'expected {static_type.__name__}, got {resolved_type.__name__}')

        self.scope.bind(name, static_type)

    @staticmethod
    def visit_AstBinding(node: AstBinding):
        return node.name, node.type_annotation

    def visit_AstIterator(self, node: AstIterator):
        return node.binding, node.expr.accept(self)

    def visit_AstDestructiveAssignment(self, node: AstDestructiveAssignment):
        prev_type = node.binding.accept(self)
        resolved_type = node.expr.accept(self)

        if not issubclass(resolved_type, prev_type):
            raise TypeError(f'type mismatch, expecting {prev_type.__name__}, got {resolved_type.__name__}')

        return resolved_type

    def visit_AstForExpression(self, node: AstForExpression):
        binding, iterator = node.iterator.accept(self)
        name, type_annotation = binding.accept(self)

        # TODO: iterator.next() and type_annotation
        resolved_type = self.scope[type_annotation.lexeme] if type_annotation else object

        self.scope = Scope(parent=self.scope)
        self.scope.bind(name, resolved_type)

        result = node.expr.accept(self)
        self.scope = self.scope.parent

        return result

    def visit_AstVectorComprehension(self, node: AstVectorComprehension):
        binding, iterator = node.iterator.accept(self)
        name, type_annotation = binding.accept(self)

        # TODO: iterator.next() and type_annotation
        resolved_type = self.scope[type_annotation.lexeme] if type_annotation else object

        self.scope = Scope(parent=self.scope)
        self.scope.bind(name, resolved_type)

        result = node.expr.accept(self)
        self.scope = self.scope.parent

        return result

    def visit_AstBranch(self, node: AstBranch):
        cond = node.expr.accept(self)
        then = node.then.accept(self)
        else_ = node.else_.accept(self)

        if cond is not bool:
            raise TypeError(f'if condition must be boolean, got {cond.__name__}')

        # TODO: type system hole
        if then is not else_:
            return object

    def visit_AstIndexAccess(self, node: AstIndexAccess):
        index_type = node.expr.accept(self)

        if index_type is not float:
            raise TypeError(f'type mismatch, expecting Number, got {index_type.__name__}')

        vector_type = node.binding.accept(self)
        return vector_type

    def visit_AstAccess(self, node: AstAccess):
        if not node.prev:
            return self.scope[node.name]

        prev = node.prev.accept(self)

        if hasattr(prev, 'attrs'):
            return prev.attrs[node.name]

        return object

    def visit_AstTypeInstantiation(self, node: AstTypeInstantiation):
        resolved_type = self.scope[node.type]
        if not isinstance(resolved_type, Type):
            raise TypeError(f'attempting to instantiate non-existent type')

        if len(resolved_type.param_types) != len(node.args):
            raise TypeError(f'wrong number of arguments')

        arg_types = [arg.accept(self) for arg in node.args]

        for i in range(len(arg_types)):
            if not issubclass(arg_types[i], resolved_type.param_types[i]):
                raise TypeError(f'type mismatch, expecting {resolved_type.param_types[i]}, got {arg_types[i]}')

        return resolved_type

    def visit_AstType(self, node: AstType):
        local = self.scope

        params = []
        resolved_supertype = None

        if node.inherit:
            if isinstance(node.inherit, AstCallExpression):
                supertype = node.inherit.binding.name

            else:
                supertype = node.inherit.lexeme

            resolved_supertype = self.scope[supertype]
            self.scope = Scope(parent=resolved_supertype.attrs)

        if isinstance(node.constructor, AstPrototype):
            type_name = node.constructor.name
            params = node.constructor.params

            for param in params:
                name, type_annotation = param.accept(self)
                self.scope.bind(name, self.scope[type_annotation.lexeme] if type_annotation else object)

        else:
            type_name = node.constructor.lexeme

        self.scope = Scope(parent=self.scope)

        param_types = [param.type_annotation for param in params]
        param_types = [self.scope[param_type.lexeme] if param_type else object for param_type in param_types]

        # noinspection PyShadowingBuiltins
        type = Type(self.scope, param_types, resolved_supertype)

        self.scope.bind('self', type)

        for member in node.block:
            member.accept(self)

        self.scope = local
        self.scope.bind(type_name, type)

    def visit_AstProtocol(self, node: AstProtocol):
        # TODO: type system hole
        self.scope.bind(node.name, object)

    @staticmethod
    def visit_AstPrototype(node: AstPrototype):
        return node.name, node.params, node.type_annotation

    def visit_AstFunction(self, node: AstFunction):
        name, params, type_annotation = node.prototype.accept(self)
        # TODO: type system hole
        self.scope.bind(name, self.scope[type_annotation.lexeme] if type_annotation else object)

    def visit_AstCallExpression(self, node: AstCallExpression):
        func = node.binding.accept(self)
        # TODO: type system hole
        return func


default_check = Check(global_context)
