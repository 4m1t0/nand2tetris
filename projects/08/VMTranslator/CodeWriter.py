from enums import Enums
import sys


class CodeWriter:

    def __init__(self, output_file):
        """出力ファイルを開き，書き込む準備を行う

        Args:
            output_file (string): 出力ファイル名
        """
        self.output = open(output_file, 'w')
        self.static_var = output_file[:-3]
        self.label_ctr = [0, 0, 0, 0]  # EQ, GT, LT, call

    def setFileName(self, file_name):
        """CodeWriterモジュールに新しいVMファイルの変換が開始したことを知らせる．

        Args:
            file_name (string): 変換元のファイル（.vm）
        """
        return

    def writeArithmetic(self, command):
        """与えられた算術コマンドをアセンブリコードに変換し，それを書き込む

        Args:
            command (string): 算術コマンド
        """
        _command = command.upper()
        if Enums.Arithmetic[_command] is Enums.Arithmetic.ADD:
            self.output.write('@SP\n')
            self.output.write('M=M-1\n')
            self.output.write('A=M\n')
            self.output.write('D=M\n')
            self.output.write('A=A-1\n')
            self.output.write('M=D+M\n')
        if Enums.Arithmetic[_command] is Enums.Arithmetic.SUB:
            self.output.write('@SP\n')
            self.output.write('M=M-1\n')
            self.output.write('A=M\n')
            self.output.write('D=M\n')
            self.output.write('A=A-1\n')
            self.output.write('M=M-D\n')
        if Enums.Arithmetic[_command] is Enums.Arithmetic.EQ:
            self.output.write('@SP\n')
            self.output.write('M=M-1\n')
            self.output.write('A=M\n')
            self.output.write('D=M\n')
            self.output.write('A=A-1\n')
            self.output.write('D=M-D\n')
            # jump to EQTRUE# if result is equal(zero)
            self.output.write('@EQTRUE%s\n' % str(self.label_ctr[0]))
            self.output.write('D;JEQ\n')
            # result is not equal
            self.output.write('@SP\n')
            self.output.write('A=M-1\n')
            self.output.write('M=0\n')
            self.output.write('@EQEND%s\n' % str(self.label_ctr[0]))
            self.output.write('0;JMP\n')
            self.output.write('(EQTRUE%s)\n' % str(self.label_ctr[0]))
            self.output.write('@SP\n')
            self.output.write('A=M-1\n')
            self.output.write('M=-1\n')
            self.output.write('(EQEND%s)\n' % str(self.label_ctr[0]))

            self.label_ctr[0] += 1
        if Enums.Arithmetic[_command] is Enums.Arithmetic.GT:
            self.output.write('@SP\n')
            self.output.write('M=M-1\n')
            self.output.write('A=M\n')
            self.output.write('D=M\n')
            self.output.write('A=A-1\n')
            self.output.write('D=M-D\n')
            # jump to EQTRUE# if result is equal(zero)
            self.output.write('@GTTRUE%s\n' % str(self.label_ctr[1]))
            self.output.write('D;JGT\n')
            # result is not equal
            self.output.write('@SP\n')
            self.output.write('A=M-1\n')
            self.output.write('M=0\n')
            self.output.write('@GTEND%s\n' % str(self.label_ctr[1]))
            self.output.write('0;JMP\n')
            self.output.write('(GTTRUE%s)\n' % str(self.label_ctr[1]))
            self.output.write('@SP\n')
            self.output.write('A=M-1\n')
            self.output.write('M=-1\n')
            self.output.write('(GTEND%s)\n' % str(self.label_ctr[1]))

            self.label_ctr[1] += 1
        if Enums.Arithmetic[_command] is Enums.Arithmetic.LT:
            self.output.write('@SP\n')
            self.output.write('M=M-1\n')
            self.output.write('A=M\n')
            self.output.write('D=M\n')
            self.output.write('A=A-1\n')
            self.output.write('D=M-D\n')
            # jump to EQTRUE# if result is equal(zero)
            self.output.write('@LTTRUE%s\n' % str(self.label_ctr[2]))
            self.output.write('D;JLT\n')
            # result is not equal
            self.output.write('@SP\n')
            self.output.write('A=M-1\n')
            self.output.write('M=0\n')
            self.output.write('@LTEND%s\n' % str(self.label_ctr[2]))
            self.output.write('0;JMP\n')
            self.output.write('(LTTRUE%s)\n' % str(self.label_ctr[2]))
            self.output.write('@SP\n')
            self.output.write('A=M-1\n')
            self.output.write('M=-1\n')
            self.output.write('(LTEND%s)\n' % str(self.label_ctr[2]))

            self.label_ctr[2] += 1
        if Enums.Arithmetic[_command] is Enums.Arithmetic.AND:
            self.output.write('@SP\n')
            self.output.write('M=M-1\n')
            self.output.write('A=M\n')
            self.output.write('D=M\n')
            self.output.write('A=A-1\n')
            self.output.write('M=D&M\n')
        if Enums.Arithmetic[_command] is Enums.Arithmetic.OR:
            self.output.write('@SP\n')
            self.output.write('M=M-1\n')
            self.output.write('A=M\n')
            self.output.write('D=M\n')
            self.output.write('A=A-1\n')
            self.output.write('M=D|M\n')
        if Enums.Arithmetic[_command] is Enums.Arithmetic.NEG:
            self.output.write('@SP\n')
            self.output.write('M=M-1\n')
            self.output.write('A=M\n')
            self.output.write('M=-M\n')
            self.output.write('@SP\n')
            self.output.write('M=M+1\n')
        if Enums.Arithmetic[_command] is Enums.Arithmetic.NOT:
            self.output.write('@SP\n')
            self.output.write('M=M-1\n')
            self.output.write('A=M\n')
            self.output.write('M=!M\n')
            self.output.write('@SP\n')
            self.output.write('M=M+1\n')

    def writePushPop(self, command, segment, index):
        """C_PUSHまたはC_POPコマンドをアセンブリコードに変換し，それを書き込む

        Args:
            command (command): C_PUSH or C_POP
            segment (string): メモリセグメント
            index (int): インデックス
        """
        _segment = segment.upper()
        if command == Enums.Command.C_PUSH:
            if Enums.MemorySegment[_segment] is \
                    Enums.MemorySegment.CONSTANT:
                self.output.write('@%s\n' % index)
                self.output.write('D=A\n')
                self.output.write('@SP\n')
                self.output.write('A=M\n')
                self.output.write('M=D\n')
            elif Enums.MemorySegment[_segment] in [
                Enums.MemorySegment.ARGUMENT,
                Enums.MemorySegment.LOCAL,
                Enums.MemorySegment.THIS,
                Enums.MemorySegment.THAT,
                Enums.MemorySegment.POINTER,
                Enums.MemorySegment.TEMP
            ]:
                if Enums.MemorySegment[_segment] is \
                        Enums.MemorySegment.ARGUMENT:
                    self.output.write('@ARG\n')
                    self.output.write('D=M\n')
                if Enums.MemorySegment[_segment] is \
                        Enums.MemorySegment.LOCAL:
                    self.output.write('@LCL\n')
                    self.output.write('D=M\n')
                if Enums.MemorySegment[_segment] is \
                        Enums.MemorySegment.THIS:
                    self.output.write('@THIS\n')
                    self.output.write('A=D+M\n')
                if Enums.MemorySegment[_segment] is \
                        Enums.MemorySegment.THAT:
                    self.output.write('@THAT\n')
                    self.output.write('D=M\n')
                if Enums.MemorySegment[_segment] is \
                        Enums.MemorySegment.POINTER:
                    self.output.write('@R3\n')
                    self.file.write('D=A\n')
                if Enums.MemorySegment[_segment] is \
                        Enums.MemorySegment.TEMP:
                    self.output.write('@R5\n')
                    self.output.write('D=A\n')

                self.output.write('@%s\n' % index)
                self.output.write('A=D+A\n')
                self.output.write('D=M\n')
                self.output.write('@SP\n')
                self.output.write('A=M\n')
                self.output.write('M=D\n')
            elif Enums.MemorySegment[_segment] is \
                    Enums.MemorySegment.STATIC:
                self.output.write('@%s.%s\n' % (self.static_var, index))
                self.output.write('D=M\n')
                self.output.write('@SP\n')
                self.output.write('A=M\n')
                self.output.write('M=D\n')
            else:
                print("Invalid .vm format")
                sys.exit(1)

            self.output.write('@SP\n')
            self.output.write('M=M+1\n')
        if command == Enums.Command.C_POP:
            if Enums.MemorySegment[_segment] is \
                    Enums.MemorySegment.CONSTANT:
                self.output.write('@SP\n')
                self.output.write('M=M-1\n')
            elif Enums.MemorySegment[_segment] in [
                Enums.MemorySegment.ARGUMENT,
                Enums.MemorySegment.LOCAL,
                Enums.MemorySegment.THIS,
                Enums.MemorySegment.THAT,
                Enums.MemorySegment.POINTER,
                Enums.MemorySegment.TEMP
            ]:
                if Enums.MemorySegment[_segment] is \
                        Enums.MemorySegment.ARGUMENT:
                    self.output.write('@ARG\n')
                    self.output.write('D=M\n')
                if Enums.MemorySegment[_segment] is \
                        Enums.MemorySegment.LOCAL:
                    self.output.write('@LCL\n')
                    self.output.write('D=M\n')
                if Enums.MemorySegment[_segment] is \
                        Enums.MemorySegment.THIS:
                    self.output.write('@THIS\n')
                    self.output.write('D=M\n')
                if Enums.MemorySegment[_segment] is \
                        Enums.MemorySegment.THAT:
                    self.output.write('@THAT\n')
                    self.output.write('D=M\n')
                if Enums.MemorySegment[_segment] is \
                        Enums.MemorySegment.POINTER:
                    self.output.write('@R3\n')
                    self.output.write('D=A\n')
                if Enums.MemorySegment[_segment] is \
                        Enums.MemorySegment.TEMP:
                    self.output.write('@R5\n')
                    self.output.write('D=A\n')

                self.output.write('@%s\n' % index)
                self.output.write('D=D+A\n')
                self.output.write('@R13\n')
                self.output.write('M=D\n')
                self.output.write('@SP\n')
                self.output.write('M=M-1\n')
                self.output.write('A=M\n')
                self.output.write('D=M\n')
                self.output.write('@R13\n')
                self.output.write('A=M\n')
                self.output.write('M=D\n')
            elif Enums.MemorySegment[_segment] is \
                    Enums.MemorySegment.STATIC:
                self.output.write('@SP\n')
                self.output.write('M=M-1\n')
                self.output.write('A=M\n')
                self.output.write('D=M\n')
                self.output.write('@%s.%s\n' % (self.static_var, index))
                self.output.write('M=D\n')
            else:
                print("Invalid .vm format")
                sys.exit(1)

    def writeInit(self):
        """VMの初期化を行うアセンブリコードを書く．このコードは出力ファイルの戦闘に配置しなければならない．
        """
        self.output.write('@256\n')
        self.output.write('D=A\n')
        self.output.write('@SP\n')
        self.output.write('M=D\n')
        self.writeCall('Sys.init', 0)

    def writeLabel(self, label):
        """labelコマンドを行うアセンブリコードを書く．

        Args:
            label (string): ラベル
        """
        self.output.write('(' + label + ')\n')

    def writeGoto(self, label):
        """gotoコマンドを行うアセンブリコードを書く．

        Args:
            label (string): ラベル
        """
        self.output.write('@' + label + '\n')
        self.output.write('0;JMP\n')

    def writeIf(self, label):
        """if-gotoコマンドを行うアセンブリコードを書く．

        Args:
            label (string): ラベル
        """
        self.output.write('@SP\n')
        self.output.write('M=M-1\n')
        self.output.write('A=M\n')
        self.output.write('D=M\n')
        self.output.write('@' + label + '\n')
        self.output.write('D;JNE\n')

    def writeCall(self, functionName, numArgs):
        """callコマンドを行うアセンブリコードを書く．

        Args:
            functionName (string): 関数名
            numArgs (int): 引数の個数
        """
        self.output.write('@' + functionName + '.RETURN' +
                          str(self.label_ctr[3]) + '\n')
        self.output.write('D=A\n')
        self.output.write('@SP\n')
        self.output.write('A=M\n')
        self.output.write('M=D\n')
        self.output.write('@SP\n')
        self.output.write('M=M+1\n')

        self.output.write('@LCL\n')
        self.output.write('D=M\n')
        self.output.write('@SP\n')
        self.output.write('A=M\n')
        self.output.write('M=D\n')
        self.output.write('@SP\n')
        self.output.write('M=M+1\n')

        self.output.write('@ARG\n')
        self.output.write('D=M\n')
        self.output.write('@SP\n')
        self.output.write('A=M\n')
        self.output.write('M=D\n')
        self.output.write('@SP\n')
        self.output.write('M=M+1\n')

        self.output.write('@THIS\n')
        self.output.write('D=M\n')
        self.output.write('@SP\n')
        self.output.write('A=M\n')
        self.output.write('M=D\n')
        self.output.write('@SP\n')
        self.output.write('M=M+1\n')

        self.output.write('@THAT\n')
        self.output.write('D=M\n')
        self.output.write('@SP\n')
        self.output.write('A=M\n')
        self.output.write('M=D\n')
        self.output.write('@SP\n')
        self.output.write('M=M+1\n')

        self.output.write('@SP\n')
        self.output.write('D=M\n')
        self.output.write('@' + str(numArgs) + '\n')
        self.output.write('D=D-A\n')
        self.output.write('@5\n')
        self.output.write('D=D-A\n')
        self.output.write('@ARG\n')
        self.output.write('M=D\n')

        self.output.write('@SP\n')
        self.output.write('D=M\n')
        self.output.write('@LCL\n')
        self.output.write('M=D\n')

        self.output.write('@' + functionName + '\n')
        self.output.write('0;JMP\n')
        self.output.write('(' + functionName + '.RETURN' +
                          str(self.label_ctr[3]) + ')\n')

        self.label_ctr[3] += 1

    def writeReturn(self):
        """returnコマンドを行うアセンブリコードを書く．
        """
        self.output.write('@LCL\n')
        self.output.write('D=M\n')
        self.output.write('@FRAME\n')
        self.output.write('M=D\n')

        self.output.write('@FRAME\n')
        self.output.write('D=M\n')
        self.output.write('@5\n')
        self.output.write('D=D-A\n')
        self.output.write('A=D\n')
        self.output.write('D=M\n')
        self.output.write('@RET\n')
        self.output.write('M=D\n')

        self.output.write('@SP\n')
        self.output.write('M=M-1\n')
        self.output.write('A=M\n')
        self.output.write('D=M\n')
        self.output.write('@ARG\n')
        self.output.write('A=M\n')
        self.output.write('M=D\n')

        self.output.write('@ARG\n')
        self.output.write('D=M\n')
        self.output.write('@SP\n')
        self.output.write('M=D+1\n')

        self.output.write('@FRAME\n')
        self.output.write('M=M-1\n')
        self.output.write('A=M\n')
        self.output.write('D=M\n')
        self.output.write('@THAT\n')
        self.output.write('M=D\n')

        self.output.write('@FRAME\n')
        self.output.write('M=M-1\n')
        self.output.write('A=M\n')
        self.output.write('D=M\n')
        self.output.write('@THIS\n')
        self.output.write('M=D\n')

        self.output.write('@FRAME\n')
        self.output.write('M=M-1\n')
        self.output.write('A=M\n')
        self.output.write('D=M\n')
        self.output.write('@ARG\n')
        self.output.write('M=D\n')

        self.output.write('@FRAME\n')
        self.output.write('M=M-1\n')
        self.output.write('A=M\n')
        self.output.write('D=M\n')
        self.output.write('@LCL\n')
        self.output.write('M=D\n')

        self.output.write('@RET\n')
        self.output.write('A=M\n')
        self.output.write('0;JMP\n')

    def writeFunction(self, functionName, numLocals):
        """functionコマンドを行うアセンブリコードを書く．

        Args:
            functionName (string): 関数名
            numLocals (int): ローカル変数の個数
        """
        self.output.write('(' + functionName + ')\n')
        self.output.write('@' + str(numLocals) + '\n')
        self.output.write('D=A\n')
        self.output.write('@' + functionName + '.kcnt\n')
        self.output.write('M=D\n')

        self.output.write('(' + functionName + '.kloop)\n')

        self.output.write('@' + functionName + '.kcnt\n')
        self.output.write('D=M\n')
        self.output.write('@' + functionName + '.END\n')
        self.output.write('D;JLE\n')

        self.output.write('@0\n')
        self.output.write('D=A\n')
        self.output.write('@SP\n')
        self.output.write('A=M\n')
        self.output.write('M=D\n')
        self.output.write('@SP\n')
        self.output.write('M=M+1\n')

        self.output.write('@' + functionName + '.kcnt\n')
        self.output.write('M=M-1\n')

        self.output.write('@' + functionName + '.kloop\n')
        self.output.write('0;JMP\n')
        self.output.write('(' + functionName + '.END)\n')

    def close(self):
        self.output.close()
