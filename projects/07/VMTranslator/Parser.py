from collections import deque
from enums import Enums
import sys


class Parser:

    def __init__(self, input_file):
        """入力ファイルを開き，パースを行う準備をする

        Args:
            input_file (string): 入力ファイル名
        """
        _input_file = open(input_file, 'r')
        self.lines = deque(
            [line.split("//")[0].rstrip()
             for line in _input_file.readlines()
             if line.split("//")[0].rstrip()])
        _input_file.close()

        self.current_command = ('', '', '')

    def hasMoreCommands(self):
        """入力ファイルにさらにコマンドが存在するか？

        Returns:
            boolean: コマンドの存在有無
        """
        return True if len(self.lines) else False

    def advance(self):
        """入力から次のコマンドを読み，それを現コマンドとする．hasMoreCommandsがtrueのときのみ本ルーチンを呼ぶようにする．最初は現コマンドは空である．
        """
        operation = self.lines.popleft().split(' ')
        if len(operation) == 1:
            self.current_command = (operation[0], '', '')
            return
        elif len(operation) == 2:
            self.current_command = (operation[0], operation[1], '')
            return
        elif len(operation) == 3:
            self.current_command = (operation[0], operation[1], operation[2])
            return

        print("Invalid .vm format at Parser.advance()")
        sys.exit(1)

    def commandType(self):
        """現VMコマンドの種類を返す．算術コマンドは全てC_ARITHMETICが返される．

        Returns:
            Command: コマンドの種類
        """
        if self.current_command[0] in \
                ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
            return Enums.Command.C_ARITHMETIC
        if self.current_command[0] == 'push':
            return Enums.Command.C_PUSH
        if self.current_command[0] == 'pop':
            return Enums.Command.C_POP
        if self.current_command[0] == 'label':
            return Enums.Command.C_LABEL
        if self.current_command[0] == 'goto':
            return Enums.Command.C_GOTO
        if self.current_command[0] == 'if-goto':
            return Enums.Command.C_IF
        if self.current_command[0] == 'function':
            return Enums.Command.C_FUNCTION
        if self.current_command[0] == 'return':
            return Enums.Command.C_RETURN
        if self.current_command[0] == 'call':
            return Enums.Command.C_CALL

        print("Invalid .vm format at Parser.commandType()")
        sys.exit(1)

    def arg1(self):
        """現コマンドの最初の引数が返される．C_ARITHMETICの場合，コマンド自体が返される．現コマンドがC_RETURNの場合，本ルーチンは呼ばないようにする．

        Returns:
            string: コマンドの第1引数
        """
        return self.current_command[0] \
            if self.commandType() == Enums.Command.C_ARITHMETIC \
            else self.current_command[1]

    def arg2(self):
        """現コマンドの第2引数が返される．現コマンドがC_PUSH, C_POP, C_FUNCTIONの場合のみ本ルーチンを呼ぶようにする．

        Returns:
            int: 現コマンドの第2引数
        """
        return self.current_command[2]
