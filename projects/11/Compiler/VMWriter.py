class VMWriter:

    def __init__(self, output_file, mode):
        self.file = open(output_file, mode)

    def writePush(self, segment, index):
        """pushコマンドを書く．

        Args:
            segment (Segment): セグメント（CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP）
            index (int): 整数
        """
        self.file.write('push %s %d\n' % (segment.value, index))

    def writePop(self, segment, index):
        """popコマンドを書く．

        Args:
            segment (Segment): セグメント（CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP）
            index (int): 整数
        """
        self.file.write('pop %s %d\n' % (segment.value, index))

    def writeArithmetic(self, command):
        """算術コマンドを書く．

        Args:
            command ([type]): 算術コマンド（ADD, SUB, NEG, EQ, GT, LT, AND, OR, NOT）
        """
        self.file.write('%s\n' % command.value)

    def writeLabel(self, label):
        """labelコマンドを書く．

        Args:
            label (string): label
        """
        self.file.write('label %s\n' % label)

    def writeGoto(self, label):
        """gotoコマンドを書く．

        Args:
            label (string): label
        """
        self.file.write('goto %s\n' % label)

    def writeIf(self, label):
        """if-gotoコマンドを書く．

        Args:
            label (string): label
        """
        self.file.write('if-goto %s\n' % label)

    def writeCall(self, name, nArgs):
        """callコマンドを書く．

        Args:
            name (string): 関数名
            nArgs (int): 引数の数
        """
        self.file.write('call %s %d\n' % (name, nArgs))

    def writeFunction(self, name, nLocals):
        """functionコマンドを書く．

        Args:
            name (string): 関数名
            nLocals (int): ローカル変数の個数
        """
        self.file.write('function %s %d\n' % (name, nLocals))

    def writeReturn(self):
        """returnコマンドを書く．
        """
        self.file.write('return\n')

    def close(self):
        """出力ファイルを閉じる．
        """
        self.file.close()
