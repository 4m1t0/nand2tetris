import CompilationEngine
import glob
import JackTokenizer
import sys


class JackAnalyzer:

    def __init__(self):
        super().__init__()

    def analyze(self, input_files):
        for input_file in input_files:
            CompilationEngine.CompilationEngine(
                input_file, JackTokenizer.JackTokenizer(input_file))


def _getInputFiles(input):
    input_files = [input] if input.endswith('.jack') \
        else glob.glob(input + '/*.jack')
    if len(input_files) == 0:
        print('Directory does not contain .jack files')
    return input_files


def _getOutputFile(output_file):
    return output_file


if len(sys.argv) != 2:
    print("Invalid usage")
    sys.exit(1)
input_files = _getInputFiles(sys.argv[1])
analyzer = JackAnalyzer()
analyzer.analyze(input_files)
