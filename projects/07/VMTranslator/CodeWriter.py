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
        self.label_ctr = [0, 0, 0]  # EQ, GT, LT

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
            self._writeCodes([
                '@SP',
                'M=M-1',
                'A=M',
                'D=M',
                'A=A-1',
                'M=D+M'
            ])
        if Enums.Arithmetic[_command] is Enums.Arithmetic.SUB:
            self._writeCodes([
                '@SP',
                'M=M-1',
                'A=M',
                'D=M',
                'A=A-1',
                'M=M-D'
            ])
        if Enums.Arithmetic[_command] is Enums.Arithmetic.EQ:
            self._writeCodes([
                '@SP',
                'M=M-1',
                'A=M',
                'D=M',
                'A=A-1',
                'D=M-D',
                # jump to EQTRUE# if result is equal(zero)
                '@EQTRUE%d' % self.label_ctr[0],
                'D;JEQ',
                # result is not equal
                '@SP',
                'A=M-1',
                'M=0',
                '@EQEND%d' % self.label_ctr[0],
                '0;JMP',
                '(EQTRUE%d)' % self.label_ctr[0],
                '@SP',
                'A=M-1',
                'M=-1',
                '(EQEND%d)' % self.label_ctr[0]
            ])

            self.label_ctr[0] += 1
        if Enums.Arithmetic[_command] is Enums.Arithmetic.GT:
            self._writeCodes([
                '@SP',
                'M=M-1',
                'A=M',
                'D=M',
                'A=A-1',
                'D=M-D',
                # jump to EQTRUE# if result is equal(zero)
                '@GTTRUE%d' % self.label_ctr[1],
                'D;JGT',
                # result is not equal
                '@SP',
                'A=M-1',
                'M=0',
                '@GTEND%d' % self.label_ctr[1],
                '0;JMP',
                '(GTTRUE%d)' % self.label_ctr[1],
                '@SP',
                'A=M-1',
                'M=-1',
                '(GTEND%d)' % self.label_ctr[1]
            ])

            self.label_ctr[1] += 1
        if Enums.Arithmetic[_command] is Enums.Arithmetic.LT:
            self._writeCodes([
                '@SP',
                'M=M-1',
                'A=M',
                'D=M',
                'A=A-1',
                'D=M-D',
                # jump to EQTRUE# if result is equal(zero)
                '@LTTRUE%d' % self.label_ctr[2],
                'D;JLT',
                # result is not equal
                '@SP',
                'A=M-1',
                'M=0',
                '@LTEND%d' % self.label_ctr[2],
                '0;JMP',
                '(LTTRUE%d)' % self.label_ctr[2],
                '@SP',
                'A=M-1',
                'M=-1',
                '(LTEND%d)' % self.label_ctr[2]
            ])

            self.label_ctr[2] += 1
        if Enums.Arithmetic[_command] is Enums.Arithmetic.AND:
            self._writeCodes([
                '@SP',
                'M=M-1',
                'A=M',
                'D=M',
                'A=A-1',
                'M=D&M'
            ])
        if Enums.Arithmetic[_command] is Enums.Arithmetic.OR:
            self._writeCodes([
                '@SP',
                'M=M-1',
                'A=M',
                'D=M',
                'A=A-1',
                'M=D|M'
            ])
        if Enums.Arithmetic[_command] is Enums.Arithmetic.NEG:
            self._writeCodes([
                '@SP',
                'M=M-1',
                'A=M',
                'M=-M',
                '@SP',
                'M=M+1'
            ])
        if Enums.Arithmetic[_command] is Enums.Arithmetic.NOT:
            self._writeCodes([
                '@SP',
                'M=M-1',
                'A=M',
                'M=!M',
                '@SP',
                'M=M+1'
            ])

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
                self._writeCodes([
                    '@%d' % index,
                    'D=A',
                    '@SP',
                    'A=M',
                    'M=D'
                ])
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
                    self._writeCodes([
                        '@ARG',
                        'D=M'
                    ])
                if Enums.MemorySegment[_segment] is \
                        Enums.MemorySegment.LOCAL:
                    self._writeCodes([
                        '@LCL',
                        'D=M'
                    ])
                if Enums.MemorySegment[_segment] is \
                        Enums.MemorySegment.THIS:
                    self._writeCodes([
                        '@THIS',
                        'A=D+M'
                    ])
                if Enums.MemorySegment[_segment] is \
                        Enums.MemorySegment.THAT:
                    self._writeCodes([
                        '@THAT',
                        'D=M'
                    ])
                if Enums.MemorySegment[_segment] is \
                        Enums.MemorySegment.POINTER:
                    self._writeCodes([
                        '@R3',
                        'D=A'
                    ])
                if Enums.MemorySegment[_segment] is \
                        Enums.MemorySegment.TEMP:
                    self._writeCodes([
                        '@R5',
                        'D=A'
                    ])

                self._writeCodes([
                    '@%d' % index,
                    'A=D+A',
                    'D=M',
                    '@SP',
                    'A=M',
                    'M=D'
                ])
            elif Enums.MemorySegment[_segment] is \
                    Enums.MemorySegment.STATIC:
                self._writeCodes([
                    '@%s.%d' % (self.static_var, index),
                    'D=M',
                    '@SP',
                    'A=M',
                    'M=D'
                ])
            else:
                print("Invalid .vm format")
                sys.exit(1)

            self._writeCodes([
                '@SP',
                'M=M+1'
            ])
        if command == Enums.Command.C_POP:
            if Enums.MemorySegment[_segment] is \
                    Enums.MemorySegment.CONSTANT:
                self._writeCodes([
                    '@SP',
                    'M=M-1'
                ])
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
                    self._writeCodes([
                        '@ARG',
                        'D=M'
                    ])
                if Enums.MemorySegment[_segment] is \
                        Enums.MemorySegment.LOCAL:
                    self._writeCodes([
                        '@LCL',
                        'D=M'
                    ])
                if Enums.MemorySegment[_segment] is \
                        Enums.MemorySegment.THIS:
                    self._writeCodes([
                        '@THIS',
                        'D=M'
                    ])
                if Enums.MemorySegment[_segment] is \
                        Enums.MemorySegment.THAT:
                    self._writeCodes([
                        '@THAT',
                        'D=M'
                    ])
                if Enums.MemorySegment[_segment] is \
                        Enums.MemorySegment.POINTER:
                    self._writeCodes([
                        '@R3',
                        'D=A'
                    ])
                if Enums.MemorySegment[_segment] is \
                        Enums.MemorySegment.TEMP:
                    self._writeCodes([
                        '@R5',
                        'D=A'
                    ])

                self._writeCodes([
                    '@%d' % index,
                    'D=D+A',
                    '@R13',
                    'M=D',
                    '@SP',
                    'M=M-1',
                    'A=M',
                    'D=M',
                    '@R13',
                    'A=M',
                    'M=D'
                ])
            elif Enums.MemorySegment[_segment] is \
                    Enums.MemorySegment.STATIC:
                self._writeCodes([
                    '@SP',
                    'M=M-1',
                    'A=M',
                    'D=M',
                    '@%s.%d' % (self.static_var, index),
                    'M=D'
                ])
            else:
                print("Invalid .vm format")
                sys.exit(1)

    def _writeCodes(self, codes):
        for code in codes:
            self.output.write(code + '\n')

    def close(self):
        self.output.close()
