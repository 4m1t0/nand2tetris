class Parser:
    A_COMMAND = 'A'
    C_COMMAND = 'C'
    L_COMMAND = 'L'

    def __init__(self, *args, **kwargs):
        self._a_command_signature = '@'
        self._c_command_signature_semicologne = ';'
        self._c_command_signature_equal = '='
        self._l_command_signature = '('
        self._comment_signature = '//'

    def commandType(self, command):
        _command = self._format(command)
        if _command.startswith(self._a_command_signature):
            return Parser.A_COMMAND
        if not _command.startswith('//') \
                and (self._c_command_signature_semicologne in _command
                     or self._c_command_signature_equal in _command):
            return Parser.C_COMMAND
        if _command.startswith(self._l_command_signature):
            return Parser.L_COMMAND

    def symbol(self, command):
        _command = self._format(command)
        if self.commandType(command) == Parser.A_COMMAND:
            return _command[1:]
        if self.commandType(command) == Parser.C_COMMAND:
            return _command[1]
        if self.commandType(command) == Parser.L_COMMAND:
            return _command[1:-1]

    def comp(self, command):
        _command = self._format(command).split(' ')[0]
        return _command.split(self._c_command_signature_equal)[1] \
            if self._c_command_signature_equal in _command \
            else _command.split(self._c_command_signature_semicologne)[0]

    def dest(self, command):
        _command = self._format(command).split(' ')[0]
        return _command.split(self._c_command_signature_equal)[0] \
            if self._c_command_signature_equal in _command \
            else ''

    def jump(self, command):
        _command = self._format(command).split(' ')[0]
        return _command.split(self._c_command_signature_semicologne)[1] \
            if self._c_command_signature_semicologne in _command \
            else ''

    def _format(self, command):
        if command.startswith(self._comment_signature):
            return ''
        return command.split(self._comment_signature)[0].strip() \
            if self._comment_signature in command \
            else command.strip()
