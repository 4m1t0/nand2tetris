from enums import Enums
import CodeWriter
import glob
import Parser
import sys


class VMTranslator:

    def __init__(self):
        super().__init__()

    def translate(self, input_files, output_file):
        writer = CodeWriter.CodeWriter(output_file)
        writer.writeInit()

        for input_file in input_files:
            self._translate(input_file, writer)

        writer.close()

    def _translate(self, input_file, writer):
        parser = Parser.Parser(input_file)
        writer.setFileName(input_file)

        while parser.hasMoreCommands():
            parser.advance()

            command = parser.commandType()
            if command == Enums.Command.C_ARITHMETIC:
                writer.writeArithmetic(parser.arg1())
            if command == Enums.Command.C_PUSH \
                    or command == Enums.Command.C_POP:
                writer.writePushPop(command, parser.arg1(), parser.arg2())
            if command == Enums.Command.C_LABEL:
                writer.writeLabel(parser.arg1())
            if command == Enums.Command.C_GOTO:
                writer.writeGoto(parser.arg1())
            if command == Enums.Command.C_IF:
                writer.writeIf(parser.arg1())
            if command == Enums.Command.C_CALL:
                writer.writeCall(parser.arg1(), parser.arg2())
            if command == Enums.Command.C_RETURN:
                writer.writeReturn()
            if command == Enums.Command.C_FUNCTION:
                writer.writeFunction(parser.arg1(), parser.arg2())


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
