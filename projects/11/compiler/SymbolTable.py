class SymbolTable:
    def __init__(self):
        self.class_table = {}  # For class-level symbols
        self.subroutine_table = {}  # For subroutine-level symbols
        self.class_index = {'STATIC': 0, 'FIELD': 0}
        self.subroutine_index = {'ARG': 0, 'VAR': 0}
        self.class_name = None  # Current class name
        
    def reset(self):
        """Starts a new subroutine scope (resets the subroutine symbol table)"""
        self.subroutine_table.clear()
        self.subroutine_index['ARG'] = 0
        self.subroutine_index['VAR'] = 0
        
    def define(self, name, type_, kind):
        """Defines a new identifier"""
        if kind in ['STATIC', 'FIELD']:
            self.class_table[name] = {'type': type_, 'kind': kind, 'index': self.class_index[kind]}
            self.class_index[kind] += 1
        else:  # ARG or VAR
            self.subroutine_table[name] = {'type': type_, 'kind': kind, 'index': self.subroutine_index[kind]}
            self.subroutine_index[kind] += 1
            
    def var_count(self, kind):
        """Returns the number of variables of the given kind"""
        if kind in ['STATIC', 'FIELD']:
            return self.class_index[kind]
        return self.subroutine_index[kind]
        
    def kind_of(self, name):
        """Returns the kind of the named identifier"""
        if name in self.subroutine_table:
            return self.subroutine_table[name]['kind']
        if name in self.class_table:
            return self.class_table[name]['kind']
        return None
        
    def type_of(self, name):
        """Returns the type of the named identifier"""
        if name in self.subroutine_table:
            return self.subroutine_table[name]['type']
        if name in self.class_table:
            return self.class_table[name]['type']
        return None
        
    def index_of(self, name):
        """Returns the index of the named identifier"""
        if name in self.subroutine_table:
            return self.subroutine_table[name]['index']
        if name in self.class_table:
            return self.class_table[name]['index']
        return None 