class Scope:

    def __init__(self, local=None, parent=None):
        if local is None:
            local = {}

        self.local = local
        self.parent = parent

    def __setitem__(self, key, value):
        self.local[key] = value

    def __getitem__(self, key):
        if key in self.local:
            return self.local[key]

        if self.parent:
            return self.parent[key]

        raise KeyError(f'trying to access non-existent \'{key}\'')

    def bind(self, key, value):
        if key in self.local:
            raise KeyError(f'\'{key}\' already defined in this scope')
        self.local[key] = value
