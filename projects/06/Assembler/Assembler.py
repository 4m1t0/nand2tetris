import Code
import Parser
import SymbolTable
import sys


class Assembler:
    def __init__(self):
        self._parser = Parser.Parser()
        self._code = Code.Code()
        self._symbol_table = SymbolTable.SymbolTable()
        self._symbol_address = 16

    def assemble(self, input_file):
        self._firstParse(input_file)
        self._secondParse(input_file, self._createOutfile(input_file))

    def _createOutfile(self, input_file):
        if input_file.endswith('.asm'):
            return input_file.replace('.asm', '_generated.hack')
        else:
            print("Unexpected file.")
            sys.exit(1)

    def _firstParse(self, file):
        with open(file) as f:
            current_address = 0
            for line in f:
                command_type = self._parser.commandType(line)
                if command_type == self._parser.A_COMMAND \
                        or command_type == self._parser.C_COMMAND:
                    current_address += 1
                elif command_type == self._parser.L_COMMAND:
                    symbol = self._parser.symbol(line)
                    self._symbol_table.addEntry(symbol, current_address)

    def _secondParse(self, input_file, output_file):
        with open(input_file) as f:
            with open(output_file, 'w') as out:
                for line in f:
                    command_type = self._parser.commandType(line)
                    if command_type == self._parser.A_COMMAND:
                        symbol = self._parser.symbol(line)
                        address = self._getAddress(symbol)
                        binary = self._code.convertTypeA(address)
                        out.write(binary + '\n')
                    elif command_type == self._parser.C_COMMAND:
                        comp = self._parser.comp(line)
                        dest = self._parser.dest(line)
                        jump = self._parser.jump(line)
                        binary = self._code.convertTypeC(comp, dest, jump)
                        out.write(binary + '\n')
                    elif command_type == self._parser.L_COMMAND:
                        continue

    def _getAddress(self, symbol):
        if symbol.isdigit():
            return symbol
        else:
            if not self._symbol_table.contains(symbol):
                self._symbol_table.addEntry(symbol, self._symbol_address)
                self._symbol_address += 1
            return self._symbol_table.getAddress(symbol)


if len(sys.argv) != 2:
    print("Invalid usage")
    sys.exit(1)
assembler = Assembler()
assembler.assemble(sys.argv[1])
