class VMWriter:
    def __init__(self, output_file):
        self.output = open(output_file, 'w')
        
    def write_push(self, segment, index):
        """Writes a VM push command"""
        self.output.write(f'push {segment.lower()} {index}\n')
        
    def write_pop(self, segment, index):
        """Writes a VM pop command"""
        self.output.write(f'pop {segment.lower()} {index}\n')
        
    def write_arithmetic(self, command):
        """Writes a VM arithmetic command"""
        self.output.write(f'{command.lower()}\n')
        
    def write_label(self, label):
        """Writes a VM label command"""
        self.output.write(f'label {label}\n')
        
    def write_goto(self, label):
        """Writes a VM goto command"""
        self.output.write(f'goto {label}\n')
        
    def write_if(self, label):
        """Writes a VM if-goto command"""
        self.output.write(f'if-goto {label}\n')
        
    def write_call(self, name, n_args):
        """Writes a VM call command"""
        self.output.write(f'call {name} {n_args}\n')
        
    def write_function(self, name, n_locals):
        """Writes a VM function command"""
        self.output.write(f'function {name} {n_locals}\n')
        
    def write_return(self):
        """Writes a VM return command"""
        self.output.write('return\n')
        
    def close(self):
        """Closes the output file"""
        self.output.close() 