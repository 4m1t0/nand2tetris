from enums import Command
import CodeWriter
import glob
import Parser
import sys


class VMTranslator:

    def __init__(self):
        super().__init__()

    def translate(self, input_files, output_file):
        writer = CodeWriter.CodeWriter(output_file)
        for input_file in input_files:
            self._translate(input_file, writer)

        writer.close()

    def _translate(self, input_file, writer):
        parser = Parser.Parser(input_file)
        writer.setFileName(input_file)

        while parser.hasMoreCommands():
            parser.advance()

            command = parser.commandType()
            if command == Command.Command.C_ARITHMETIC:
                writer.writeArithmetic(parser.arg1())
            if command == Command.Command.C_PUSH \
                    or command == Command.Command.C_POP:
                writer.writePushPop(command, parser.arg1(), parser.arg2())


def _getInputFiles(input):
    input_files = [input] if input.endswith('.vm') \
        else glob.glob(input + '/*.vm')
    if len(input_files) == 0:
        print('Directory does not contain .vm files')
    return input_files


def _getOutputFile(output_file):
    return output_file


if len(sys.argv) != 3:
    print("Invalid usage")
    sys.exit(1)
input_files = _getInputFiles(sys.argv[1])
output_file = _getOutputFile(sys.argv[2])
translator = VMTranslator()
translator.translate(input_files, output_file)
