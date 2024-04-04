from m_ast import AstNode
from collections import OrderedDict

class Scope:
    def __init__(self, parent=None):
        self.local_vars = []
        self.local_funcs = []
        self.parent = parent
        self.children = []
        self.var_index_at_parent = 0 if parent is None else len(parent.local_vars) 
        self.func_index_at_parent = 0 if parent is None else len(parent.local_funcs) 
        
    def create_child_scope(self):
        child_scope = Scope(self)
        self.children.append(child_scope)
        return child_scope
    
    ### Semantic Check
    def define_variable(self, vname):
        """ Add a variable name to the local scope if it has not been defined before in this scope."""
        if vname in self.local_vars:
            return False
            raise Exception(f"var {vname} already defined in the current scope.")
        self.local_vars.append(vname)
        return True
    
    def define_variable_destructive(self, vname):
        """ Add a variable name to the local scope if it has been defined before in any parent scope."""
        if self.is_var_defined(vname):
            self.local_vars.append(vname)
            return True
        return False
        raise Exception(f"var {vname} is not defined previously, so it cannot have a destructive assignment.")
    
    def define_function(self, fname, params):
        """ Add a function name to the local scope if it has not been defined before.

            params is a list of names (str)
        """
        for fn, n in self.local_funcs:
            if fn == fname:
                return False
                raise Exception(f"function {fname} already defined in the current scope.")
        fn_scope = self.create_child_scope()
        for p in params:
            fn_scope.define_variable(p)
        self.local_funcs.append((fname, len(params))) 
        return True
    
    def is_var_defined(self, vname, until=None):
        """ Returns True if vname exists in current scope or any parent scope"""
        if until:
            local_vars = self.local_vars[:until]
        else: local_vars = self.local_vars

        if vname in local_vars:
            return True
        if self.parent != None:
            return self.parent.is_var_defined(vname, until=self.var_index_at_parent)
        return False
    
    def is_func_defined(self, fname, n, until=None):
        """ Returns True if fname with n params exists in current scope or any parent scope"""
        if until:
            local_funcs = self.local_funcs[:until]
        else: local_funcs = self.local_funcs
        
        if (fname, n) in self.local_funcs: # TODO test!!!!!!!!!!!
            return True
        if self.parent != None:
            return self.parent.is_func_defined(fname, n, until=self.func_index_at_parent)
        return False

    def is_local_var(self, vname):
        return vname in self.local_vars
    
    def is_local_func(self, fname, n):
        return (fname, n) in self.local_funcs

    # def get_local_variable_info(self, vname):
    #     # Your code here!!!
    #     return
    
    # def get_local_function_info(self, fname, n):
    #     # Your code here!!!
    #     return

class RunScope(Scope):
    def __init__(self, parent=None):
        self.local_vars = {}
        self.local_funcs = {}
        self.parent = parent
        self.children = []
        self.var_index_at_parent = 0 if parent is None else len(parent.local_vars) 
        self.func_index_at_parent = 0 if parent is None else len(parent.local_funcs) 
        
    def create_child_scope(self):
        child_scope = RunScope(self)
        self.children.append(child_scope)
        return child_scope
    
    ### Run Check
    def assign_variable(self, vname, vvalue):
        """Add a variable name, value to the local scope if it has not been defined before in this scope. """
        if vname in self.local_vars.keys():
            return False
            raise Exception(f"var {vname} already defined in the current scope.")
        self.local_vars[vname] = vvalue
        return True
    
    def assign_variable_destructive(self, vname, vvalue):
        """Add a new value for vname in the local scope if it has been defined before in any parent scope."""
        exists, value = self.get_variable_info(vname)
        if exists:
            self.local_vars[vname] = vvalue
            return True
        return False
        raise Exception(f"var {vname} is not defined previously, so it cannot have a destructive assignment.")
        
    def assign_function(self, fname, params, expr: AstNode):
        """ Add a function (name, len(params)):[params, expr] to the local scope if it has not been defined before.

            params is a list of names (str) """
        for fn, n in self.local_funcs.keys():
            if fn == fname:
                return False
                raise Exception(f"function {fname} already defined in the current scope.")
        self.local_funcs[(fname, len(params))] = (params, expr)
        return True
        
    def get_variable_info(self, vname):
        """ If vname exists in current scope or any parent scope return it's value in the first ocurrency bottom-up"""
        if vname in self.local_vars.keys():
            return True, self.local_vars[vname]
        
        if self.parent != None:
            return self.parent.get_variable_info(vname)
        return False, None
    
    def get_function_info(self, fname, n):
        """ If fname exists return it's [params, expr] """
        if (fname, n) in self.local_funcs.keys():
            return True, self.local_funcs[(fname, n)]
        
        if self.parent != None:
            return self.parent.get_function_info(fname, n)
        return False, None

class Attribute:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Method:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __eq__(self, other):
        return other.name == self.name and len(other.params) == len(self.params) 

class Type:
    def __init__(self, type_name:str, type_args=None):
        self.name = type_name
        self.type_args = type_args
        self.base = None
        self.attributes = []
        self.methods = []

    def set_parent(self, parent):
        if self.base is not None:
            raise Exception(f'Parent type is already set for {self.name}.')
        self.base = parent
        self.inherits = True

    def get_attribute(self, name:str):
        for attr in self.attributes:
            attr:Attribute
            if attr.name == name:
                return attr
        raise Exception(f'Attribute "{name}" is not defined in {self.name}.')

    def define_attribute(self, name:str, value):
        if name in (attr.name for attr in self.attributes):
            raise Exception(f'Attribute "{name}" is already defined in {self.name}.')
        attribute = Attribute(name, value)
        self.attributes.append(attribute)
        return attribute

    def get_method(self, name:str):
        for method in self.methods:
            method:Method
            if method.name == name:
                return method
        if self.base is None:
            raise Exception(f'Method "{name}" is not defined in {self.name}.')
        
        try:
            return self.parent.get_method(name)
        except:
            raise Exception(f'Method "{name}" is not defined in {self.name}.')

    def define_method(self, name:str, param_names:list, body):
        if name in (method.name for method in self.methods):
            raise Exception(f'Method "{name}" already defined in {self.name}')

        method = Method(name, param_names, body)
        self.methods.append(method)
        return method

    def all_attributes(self):
        plain = OrderedDict() if self.base is None else self.base.all_attributes()
        for attr in self.attributes:
            plain[attr.name] = (attr, self)
        return plain

    def all_methods(self):
        plain = OrderedDict() if self.base is None else self.base.all_methods()
        for method in self.methods:
            plain[method.name] = (method, self)
        return plain

    # def conforms_to(self, other):
    #     return other.bypass() or self == other or self.parent is not None and self.parent.conforms_to(other)

    # def bypass(self):
    #     return False

class Instance:
    def __init__(self, type_name:str, type_args=None):
        self.type = type_name
        self.type_args = type_args

    def get_atrribute(self, name:str):
        pass
    def call_method(self, name:str, args:list):
        pass


class Context:
    def __init__(self):
        self.types = {}

    def create_type(self, name:str):
        if name in self.types:
            raise Exception(f'Type with the same name ({name}) already in context.')
        typex = self.types[name] = Type(name)
        return typex

    def get_type(self, name:str):
        try:
            return self.types[name]
        except KeyError:
            raise Exception(f'Type "{name}" is not defined.')
        