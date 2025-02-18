class Parser:
    def __init__(self, input_file):
        """
        Opens the input file and gets ready to parse it.
        Args:
            input_file (str): Path to the .vm file
        """
        self.current_command = None
        self.current_command_type = None
        
        # Read and clean the input file
        with open(input_file, 'r') as file:
            # Remove comments and empty lines, strip whitespace
            self.commands = []
            for line in file:
                # Remove inline comments and trailing/leading whitespace
                line = line.split('//')[0].strip()
                # Skip empty lines and pure comment lines
                if line:
                    self.commands.append(line)
                    
        self.command_count = len(self.commands)
        self.current_command_idx = -1

    def has_more_commands(self):
        """Returns True if there are more commands to process."""
        return self.current_command_idx < self.command_count - 1

    def advance(self):
        """Reads the next command and makes it the current command."""
        self.current_command_idx += 1
        self.current_command = self.commands[self.current_command_idx]
        
        # Parse command type
        parts = self.current_command.split()
        command = parts[0]
        
        if command in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
            self.current_command_type = 'C_ARITHMETIC'
        elif command == 'push':
            self.current_command_type = 'C_PUSH'
        elif command == 'pop':
            self.current_command_type = 'C_POP'
        # Add other command types as needed

    def command_type(self):
        """Returns the type of the current command."""
        return self.current_command_type

    def arg1(self):
        """
        Returns the first argument of the current command.
        For C_ARITHMETIC, returns the command itself.
        Should not be called for C_RETURN.
        """
        if self.current_command_type == 'C_ARITHMETIC':
            return self.current_command.split()[0]
        else:
            return self.current_command.split()[1]

    def arg2(self):
        """
        Returns the second argument of the current command.
        Should be called only for C_PUSH, C_POP, C_FUNCTION, C_CALL
        """
        return int(self.current_command.split()[2]) 