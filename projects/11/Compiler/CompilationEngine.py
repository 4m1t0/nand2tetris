from enum import Enum
from enums import Enums
import SymbolTable
import VMWriter


class CompilationEngine:

    def __init__(self, input_file, tokenizer):
        self.indent_level = 0
        self.tokenizer = tokenizer
        self.symbol_table = SymbolTable.SymbolTable()
        self.label_count = 0

        self.vm_output_path = input_file.replace('.jack', '.vm')
        self.writer = VMWriter.VMWriter(self.vm_output_path, 'w')
        self.xml_output = open(input_file.replace(
            '.jack', '.xml'), 'w')

        self.compileClass()
        self.xml_output.close()

    def compileClass(self):
        """クラスをコンパイルする．
        """
        self._writeElementStart(TagName.CLASS)

        self.compileKeyword()

        self.class_name = self.tokenizer.identifier()
        self.compileIdentifier()

        self.compileSymbol()
        while self.tokenizer.tokenType() is Enums.Token.KEYWORD \
            and self.tokenizer.keyword() in \
                (Enums.Keyword.STATIC, Enums.Keyword.FIELD):
            self.compileClassVarDec()
        while self.tokenizer.tokenType() is Enums.Token.KEYWORD \
            and self.tokenizer.keyword() in \
                (Enums.Keyword.CONSTRUCTOR, Enums.Keyword.FUNCTION,
                 Enums.Keyword.METHOD):
            self.compileSubroutine()
        self.compileSymbol()

        self._writeElementEnd(TagName.CLASS)

    def compileKeyword(self):
        """キーワードをコンパイルする．
        """
        self._writeElement(TagName.KEYWORD, self.tokenizer.keyword().value)

        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

    def compileSymbol(self):
        symbol = self.tokenizer.symbol()
        if self.tokenizer.symbol() is Enums.Symbol.LESS_THAN_SIGN:
            self._writeElement(TagName.SYMBOL, '&lt;')
        elif self.tokenizer.symbol() is Enums.Symbol.GREATER_THAN_SIGN:
            self._writeElement(TagName.SYMBOL, '&gt;')
        elif self.tokenizer.symbol() is Enums.Symbol.AMPERSAND:
            self._writeElement(TagName.SYMBOL, '&amp;')
        else:
            self._writeElement(TagName.SYMBOL, symbol.value)

        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

    def compileIdentifier(self):
        """識別子（identifier）をコンパイルする．
        """
        self._writeElement(TagName.IDENTIFIER,
                           self.tokenizer.identifier())

        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

    def compileIntegerConstant(self):
        """整数の定数をコンパイルする．
        """
        self._writeElement(TagName.INTEGER_CONSTANT,
                           self.tokenizer.intVal())

        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

    def compileStringConstant(self):
        """文字列の定数をコンパイルする．
        """
        string_val = self.tokenizer.stringVal()
        self._writeElement(TagName.STRING_CONSTANT, string_val)
        self.writer.writePush(Enums.Segment.CONST, len(string_val))
        self.writer.writeCall('String.new', 1)

        for i in range(len(string_val)):
            self.writer.writePush(Enums.Segment.CONST, ord(string_val[i]))
            self.writer.writeCall('String.appendChar', 2)

        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

    def compileType(self):
        """型をコンパイルする．
        """
        type = None
        if self.tokenizer.tokenType() is Enums.Token.KEYWORD \
            and self.tokenizer.keyword() in \
                (Enums.Keyword.INT,
                 Enums.Keyword.CHAR,
                 Enums.Keyword.BOOLEAN):
            type = self.tokenizer.keyword()
            self.compileKeyword()
        else:
            type = self.tokenizer.identifier()
            self.compileIdentifier()
        return type

    def compileClassVarDec(self):
        """スタティック宣言またはフィールド宣言をコンパイルする．
        """
        self._writeElementStart(TagName.CLASS_VAR_DEC)

        kind = Enums.Kind(self.tokenizer.keyword().value)
        self.compileKeyword()
        type = self.compileType()
        self.compileVarName(type, kind, declaration=True)

        while not (self.tokenizer.tokenType() is Enums.Token.SYMBOL
                   and self.tokenizer.symbol() is Enums.Symbol.SEMI_COLON):
            self.compileSymbol()
            self.compileVarName(
                type, kind, declaration=True)
        self.compileSymbol()

        self._writeElementEnd(TagName.CLASS_VAR_DEC)

    def compileSubroutine(self):
        """メソッド，ファンクション，コンストラクタをコンパイルする．
        """
        self.symbol_table.startSubroutine()

        self._writeElementStart(TagName.SUBROUTINE_DEC)

        subroutine_keyword = self.tokenizer.keyword()
        if subroutine_keyword is Enums.Keyword.METHOD:
            self.symbol_table.define(
                'this', self.class_name, Enums.Kind.ARGUMENT)
        self.compileKeyword()

        if self.tokenizer.tokenType() is Enums.Token.KEYWORD \
                and self.tokenizer.keyword() is Enums.Keyword.VOID:
            self.compileKeyword()
        else:
            self.compileType()

        function_name = '%s.%s' % (
            self.class_name, self.tokenizer.identifier())
        self.compileIdentifier()
        self.compileSymbol()
        self.compileParameterList()
        self.compileSymbol()

        # Body
        self._writeElementStart(TagName.SUBROUTINE_BODY)
        self.compileSymbol()  # {

        self.writer.writeFunction(function_name, 0)
        if subroutine_keyword is Enums.Keyword.CONSTRUCTOR:
            self.writer.writePush(Enums.Segment.CONST,
                                  self.symbol_table.varCount(Enums.Kind.FIELD))
            self.writer.writeCall('Memory.alloc', 1)
            self.writer.writePop(Enums.Segment.POINTER, 0)
        elif subroutine_keyword is Enums.Keyword.METHOD:
            self.writer.writePush(Enums.Segment.ARGUMENT, 0)
            self.writer.writePop(Enums.Segment.POINTER, 0)

        n_locals = 0
        while self.tokenizer.tokenType() is Enums.Token.KEYWORD \
                and self.tokenizer.keyword() is Enums.Keyword.VAR:
            n_var = self.compileVarDec()
            n_locals += n_var

        if n_locals:
            self.writer.close()
            f = open(self.vm_output_path, 'r')
            new_lines = f.read().replace('%s 0' % function_name, '%s %d' %
                                         (function_name, n_locals))
            f.close()

            f = open(self.vm_output_path, 'w')
            f.write(new_lines)
            f.close()

            self.writer = VMWriter.VMWriter(self.vm_output_path, 'a')

        self.compileStatements()
        self.compileSymbol()

        self._writeElementEnd(TagName.SUBROUTINE_BODY)

        self._writeElementEnd(TagName.SUBROUTINE_DEC)

    def compileParameterList(self):
        """パラメータのリスト（空の可能性もある）をコンパイルする．"()" は含まない．
        """
        self._writeElementStart(TagName.PARAMETER_LIST)

        if (self.tokenizer.tokenType() is Enums.Token.KEYWORD
            and self.tokenizer.keyword() in (
                Enums.Keyword.INT, Enums.Keyword.CHAR,
                Enums.Keyword.BOOLEAN)) \
                or self.tokenizer.tokenType() is Enums.Token.IDENTIFIER:
            type = self.compileType()
            self.compileVarName(type, Enums.Kind.ARGUMENT, declaration=True)

            while self.tokenizer.tokenType() is Enums.Token.SYMBOL \
                    and self.tokenizer.symbol() is Enums.Symbol.COMMA:
                self.compileSymbol()
                type = self.compileType()
                self.compileVarName(
                    type, Enums.Kind.ARGUMENT, declaration=True)

        self._writeElementEnd(TagName.PARAMETER_LIST)

    def compileVarDec(self):
        """var宣言をコンパイルする．
        """
        self._writeElementStart(TagName.VAR_DEC)

        self.compileKeyword()  # var
        type = self.compileType()
        self.compileVarName(type, Enums.Kind.VAR, declaration=True)

        n_var = 1
        while self.tokenizer.tokenType() is Enums.Token.SYMBOL \
                and self.tokenizer.symbol() is Enums.Symbol.COMMA:
            n_var += 1
            self.compileSymbol()
            self.compileVarName(type, Enums.Kind.VAR, declaration=True)
        self.compileSymbol()

        self._writeElementEnd(TagName.VAR_DEC)
        return n_var

    def compileVarName(self, type=None, kind=None, declaration=False, let=False, call=False):
        name = self.tokenizer.identifier()
        if declaration:
            self.symbol_table.define(name, type, kind)
        elif let:
            pass
        elif call:
            pass
        else:
            kind = self.symbol_table.kindOf(name)
            segment = None
            if kind is Enums.Kind.ARGUMENT:
                segment = Enums.Segment.ARGUMENT
            elif kind is Enums.Kind.FIELD:
                segment = Enums.Segment.THIS
            elif kind is Enums.Kind.STATIC:
                segment = Enums.Segment.STATIC
            elif kind is Enums.Kind.VAR:
                segment = Enums.Segment.LOCAL
            else:
                raise Exception('Unexpected kind: %s' % kind)
            index = self.symbol_table.indexOf(name)
            self.writer.writePush(segment, index)

        self._writeIdentifier(name, declaration)
        self.tokenizer.advance()

    def compileStatements(self):
        """一連の文ををコンパイルする．"{}" は含まない．
        """
        self._writeElementStart(TagName.STATEMENTS)

        while self.tokenizer.tokenType() is Enums.Token.KEYWORD \
            and self.tokenizer.keyword() in \
                (Enums.Keyword.LET, Enums.Keyword.IF,
                 Enums.Keyword.WHILE, Enums.Keyword.DO,
                 Enums.Keyword.RETURN):
            if self.tokenizer.keyword() is Enums.Keyword.LET:
                self.compileLet()
            elif self.tokenizer.keyword() is Enums.Keyword.IF:
                self.compileIf()
            elif self.tokenizer.keyword() is Enums.Keyword.WHILE:
                self.compileWhile()
            elif self.tokenizer.keyword() is Enums.Keyword.DO:
                self.compileDo()
            elif self.tokenizer.keyword() is Enums.Keyword.RETURN:
                self.compileReturn()

        self._writeElementEnd(TagName.STATEMENTS)

    def compileSubroutineCall(self):
        name = self.tokenizer.identifier()
        n_args = 0

        kind = self.symbol_table.kindOf(name)
        if self.symbol_table.kindOf(name) is not Enums.Kind.NONE:
            type = self.symbol_table.typeOf(name)
            index = self.symbol_table.indexOf(name)
            n_args += 1
            if kind is Enums.Kind.STATIC:
                self.writer.writePush(Enums.Segment.STATIC, index)
            elif kind is Enums.Kind.FIELD:
                self.writer.writePush(Enums.Segment.THIS, index)
            elif kind is Enums.Kind.ARGUMENT:
                self.writer.writePush(Enums.Segment.ARGUMENT, index)
            elif kind is Enums.Kind.VAR:
                self.writer.writePush(Enums.Segment.LOCAL, index)

            self.compileVarName(call=True)
            self.compileSymbol()
            name = '%s.%s' % (type, self.tokenizer.identifier())
            self.compileIdentifier()
        else:
            self.compileIdentifier()
            if self.tokenizer.tokenType() is Enums.Token.SYMBOL \
                    and self.tokenizer.symbol() is Enums.Symbol.PERIOD:
                self.compileSymbol()  # .
                name = '%s.%s' % (name, self.tokenizer.identifier())
                self.compileIdentifier()
            else:
                self.writer.writePush(Enums.Segment.POINTER, 0)
                name = '%s.%s' % (self.class_name, name)
                n_args += 1

        self.compileSymbol()  # (
        n_args += self.compileExpressionList()
        self.compileSymbol()  # )

        self.writer.writeCall(name, n_args)

    def compileDo(self):
        """do文をコンパイルする．
        """
        self._writeElementStart(TagName.DO_STATEMENT)

        self.compileKeyword()  # do
        self.compileSubroutineCall()
        self.compileSymbol()  # ;

        self.writer.writePop(Enums.Segment.TEMP, 0)
        self._writeElementEnd(TagName.DO_STATEMENT)

    def compileLet(self):
        """let文をコンパイルする．
        """
        self._writeElementStart(TagName.LET_STATEMENT)

        self.compileKeyword()
        name = self.tokenizer.identifier()
        self.compileVarName(let=True)
        kind = self.symbol_table.kindOf(name)
        index = self.symbol_table.indexOf(name)

        if (self.tokenizer.tokenType() is Enums.Token.SYMBOL
                and self.tokenizer.symbol() is not Enums.Symbol.EQUAL):
            self.compileSymbol()
            self.compileExpression()
            self.compileSymbol()

            if kind is Enums.Kind.STATIC:
                self.writer.writePush(Enums.Segment.STATIC, index)
            elif kind is Enums.Kind.FIELD:
                self.writer.writePush(Enums.Segment.THIS, index)
            elif kind is Enums.Kind.ARGUMENT:
                self.writer.writePush(Enums.Segment.ARGUMENT, index)
            elif kind is Enums.Kind.VAR:
                self.writer.writePush(Enums.Segment.LOCAL, index)
            self.writer.writeArithmetic(Enums.Command.ADD)

            self.compileSymbol()
            self.compileExpression()
            self.writer.writePop(Enums.Segment.TEMP, 0)
            self.writer.writePop(Enums.Segment.POINTER, 1)
            self.writer.writePush(Enums.Segment.TEMP, 0)
            self.writer.writePop(Enums.Segment.THAT, 0)
        else:
            self.compileSymbol()
            self.compileExpression()
            if kind is Enums.Kind.STATIC:
                self.writer.writePop(Enums.Segment.STATIC, index)
            elif kind is Enums.Kind.FIELD:
                self.writer.writePop(Enums.Segment.THIS, index)
            elif kind is Enums.Kind.ARGUMENT:
                self.writer.writePop(Enums.Segment.ARGUMENT, index)
            elif kind is Enums.Kind.VAR:
                self.writer.writePop(Enums.Segment.LOCAL, index)

        self.compileSymbol()

        self._writeElementEnd(TagName.LET_STATEMENT)

    def compileWhile(self):
        """while文をコンパイルする．
        """
        self._writeElementStart(TagName.WHILE_STATEMENT)

        label_loop = 'WHILE_LOOP_%d' % self.label_count
        label_end = 'WHILE_END_%d' % self.label_count
        self.label_count += 1

        self.writer.writeLabel(label_loop)
        self.compileKeyword()  # while
        self.compileSymbol()  # (
        self.compileExpression()  # 式
        self.writer.writeArithmetic(Enums.Command.NOT)
        self.writer.writeIf(label_end)
        self.compileSymbol()  # )
        self.compileSymbol()  # {
        self.compileStatements()  # 文
        self.compileSymbol()  # }
        self.writer.writeGoto(label_loop)
        self.writer.writeLabel(label_end)

        self._writeElementEnd(TagName.WHILE_STATEMENT)

    def compileReturn(self):
        """return文をコンパイルする．
        """
        self._writeElementStart(TagName.RETURN_STATEMENT)

        self.compileKeyword()  # return
        if self.tokenizer.tokenType() is not Enums.Token.SYMBOL \
            or (self.tokenizer.tokenType() is Enums.Token.SYMBOL
                and self.tokenizer.symbol() is not Enums.Symbol.SEMI_COLON):
            self.compileExpression()  # 式
        else:
            self.writer.writePush(Enums.Segment.CONST, 0)
        self.compileSymbol()  # ;

        self.writer.writeReturn()
        self._writeElementEnd(TagName.RETURN_STATEMENT)

    def compileIf(self):
        """if文をコンパイルする．else文を扱う可能性がある．
        """
        self._writeElementStart(TagName.IF_STATEMENT)

        label_else = 'IF_ELSE_%d' % self.label_count
        label_end = 'IF_END_%d' % self.label_count
        self.label_count += 1

        self.compileKeyword()  # if
        self.compileSymbol()  # (
        self.compileExpression()  # 式
        self.writer.writeArithmetic(Enums.Command.NOT)
        self.writer.writeIf(label_else)
        self.compileSymbol()  # )
        self.compileSymbol()  # {
        self.compileStatements()  # 文
        self.compileSymbol()  # }
        self.writer.writeGoto(label_end)

        self.writer.writeLabel(label_else)
        if self.tokenizer.tokenType() is Enums.Token.KEYWORD \
                and self.tokenizer.keyword() is Enums.Keyword.ELSE:
            self.compileKeyword()  # else
            self.compileSymbol()  # {
            self.compileStatements()  # 文
            self.compileSymbol()  # }
        self.writer.writeLabel(label_end)

        self._writeElementEnd(TagName.IF_STATEMENT)

    def compileExpression(self):
        """式をコンパイルする．
        """
        self._writeElementStart(TagName.EXPRESSION)

        self.compileTerm()
        while self.tokenizer.tokenType() is Enums.Token.SYMBOL \
            and self.tokenizer.symbol() in \
            (Enums.Symbol.PLUS_SIGN,
             Enums.Symbol.HYPHEN,
             Enums.Symbol.ASTERISK,
             Enums.Symbol.SLASH,
             Enums.Symbol.AMPERSAND,
             Enums.Symbol.VERTICAL_LINE,
             Enums.Symbol.LESS_THAN_SIGN,
             Enums.Symbol.GREATER_THAN_SIGN,
             Enums.Symbol.EQUAL):
            symbol = self.tokenizer.symbol()
            self.compileSymbol()
            self.compileTerm()

            if symbol is Enums.Symbol.PLUS_SIGN:
                self.writer.writeArithmetic(Enums.Command.ADD)
            elif symbol is Enums.Symbol.HYPHEN:
                self.writer.writeArithmetic(Enums.Command.SUB)
            elif symbol is Enums.Symbol.ASTERISK:
                self.writer.writeCall('Math.multiply', 2)
            elif symbol is Enums.Symbol.SLASH:
                self.writer.writeCall('Math.divide', 2)
            elif symbol is Enums.Symbol.AMPERSAND:
                self.writer.writeArithmetic(Enums.Command.AND)
            elif symbol is Enums.Symbol.VERTICAL_LINE:
                self.writer.writeArithmetic(Enums.Command.OR)
            elif symbol is Enums.Symbol.LESS_THAN_SIGN:
                self.writer.writeArithmetic(Enums.Command.LT)
            elif symbol is Enums.Symbol.GREATER_THAN_SIGN:
                self.writer.writeArithmetic(Enums.Command.GT)
            elif symbol is Enums.Symbol.EQUAL:
                self.writer.writeArithmetic(Enums.Command.EQ)

        self._writeElementEnd(TagName.EXPRESSION)

    def compileTerm(self):
        """termをコンパイルする．
        このルーチンはやや複雑であり，構文解析のルールには複数の選択肢が存在し，現トークンだけからは決定できない場合がある．
        具体的に言うと，もし現トークンが識別子であれば，このルーチンは，それが変数，配列宣言，サブルーチン呼び出しのいずれかを識別しなければならない．

        そのためには，ひとつ先のトークンを読み込み，
        そのトークンが "[" か "(" か "." のどれに該当するかを調べれば，現トークンの種類を決定することができる．

        他のトークンの場合は現トークンに含まないので先読みを行う必要はない．
        """
        self._writeElementStart(TagName.TERM)

        if self.tokenizer.tokenType() is Enums.Token.INT_CONST:
            self.writer.writePush(Enums.Segment.CONST, self.tokenizer.intVal())
            self.compileIntegerConstant()
        elif self.tokenizer.tokenType() is Enums.Token.STRING_CONST:
            self.compileStringConstant()
        elif self.tokenizer.tokenType() is Enums.Token.KEYWORD:
            if self.tokenizer.keyword() is Enums.Keyword.TRUE:
                self.writer.writePush(Enums.Segment.CONST, 1)
                self.writer.writeArithmetic(Enums.Command.NEG)
            elif self.tokenizer.keyword() is Enums.Keyword.FALSE:
                self.writer.writePush(Enums.Segment.CONST, 0)
            elif self.tokenizer.keyword() is Enums.Keyword.NULL:
                self.writer.writePush(Enums.Segment.CONST, 0)
            elif self.tokenizer.keyword() is Enums.Keyword.THIS:
                self.writer.writePush(Enums.Segment.POINTER, 0)
            self.compileKeyword()
        elif self.tokenizer.tokenType() is Enums.Token.IDENTIFIER:
            name = self.tokenizer.identifier()
            if self.symbol_table.kindOf(name) is not Enums.Kind.NONE:
                self.compileVarName(declaration=False)
            else:
                self.compileIdentifier()

            if self.tokenizer.tokenType() is Enums.Token.SYMBOL and \
                self.tokenizer.symbol() is \
                    Enums.Symbol.LEFT_SQUARE_BRACKET:
                self.compileSymbol()
                self.compileExpression()
                self.compileSymbol()
                self.writer.writeArithmetic(Enums.Command.ADD)
                self.writer.writePop(Enums.Segment.POINTER, 1)
                self.writer.writePush(Enums.Segment.THAT, 0)
            elif self.tokenizer.tokenType() is Enums.Token.SYMBOL and \
                self.tokenizer.symbol() is \
                    Enums.Symbol.LEFT_ROUND_BRACKET:
                self.compileSymbol()
                n_args = self.compileExpressionList()
                self.compileSymbol()
                self.writer.writeCall(name, n_args)
            elif self.tokenizer.tokenType() is Enums.Token.SYMBOL and \
                    self.tokenizer.symbol() is Enums.Symbol.PERIOD:
                self.compileSymbol()

                n_args = 0
                if self.symbol_table.kindOf(name) is not Enums.Kind.NONE:
                    name = self.symbol_table.typeOf(name)
                    n_args = 1

                name = '%s.%s' % (name, self.tokenizer.identifier())
                self.compileIdentifier()
                self.compileSymbol()
                n_args += self.compileExpressionList()
                self.compileSymbol()
                self.writer.writeCall(name, n_args)
        elif self.tokenizer.tokenType() is Enums.Token.SYMBOL and \
            self.tokenizer.symbol() is \
                Enums.Symbol.LEFT_ROUND_BRACKET:
            self.compileSymbol()
            self.compileExpression()
            self.compileSymbol()
        # TODO: この分岐が死にルートっぽい
        elif self.tokenizer.tokenType() is Enums.Token.SYMBOL and \
            self.tokenizer.symbol() in (
                Enums.Symbol.HYPHEN, Enums.Symbol.TILDE):
            symbol = self.tokenizer.symbol()
            self.compileSymbol()
            self.compileTerm()
            if symbol is Enums.Symbol.HYPHEN:
                self.writer.writeArithmetic(Enums.Command.NEG)
            if symbol is Enums.Symbol.TILDE:
                self.writer.writeArithmetic(Enums.Command.NOT)

        self._writeElementEnd(TagName.TERM)

    def compileExpressionList(self):
        """コンマで分離された式のリスト（空の可能性もある）をコンパイルする．
        """
        self._writeElementStart(TagName.EXPRESSION_LIST)

        n_args = 0
        if self.tokenizer.tokenType() is not Enums.Token.SYMBOL \
            or (self.tokenizer.tokenType() is Enums.Token.SYMBOL
                and self.tokenizer.symbol() is not Enums.Symbol.RIGHT_ROUND_BRACKET):
            n_args = 1
            self.compileExpression()

            while self.tokenizer.tokenType() is Enums.Token.SYMBOL \
                    and self.tokenizer.symbol() is Enums.Symbol.COMMA:
                self.compileSymbol()
                self.compileExpression()
                n_args += 1

        self._writeElementEnd(TagName.EXPRESSION_LIST)
        return n_args

    def _writeElement(self, tag_name, value):
        """要素を書き出す．

        Args:
            tag_name (TagName): タグ名
            value (string): 値
        """
        indent = '  ' * self.indent_level
        self.xml_output.write('%s<%s> %s </%s>\n' %
                              (indent, tag_name.value, value, tag_name.value))

    def _writeElementStart(self, tag_name):
        """開始要素を書き出す．

        Args:
            tag_name (TagName): タグ名
        """
        indent = '  ' * self.indent_level
        self.xml_output.write('%s<%s>\n' % (indent, tag_name.value))
        self.indent_level += 1

    def _writeElementEnd(self, tag_name):
        """終了要素を書き出す．

        Args:
            tag_name (TagName): タグ名
        """
        self.indent_level -= 1
        indent = '  ' * self.indent_level
        self.xml_output.write('%s</%s>\n' % (indent, tag_name.value))

    def _writeIdentifier(self, name, declaration):
        type = self.symbol_table.typeOf(name)
        kind = self.symbol_table.kindOf(name)
        index = self.symbol_table.indexOf(name)
        info = 'declaration: %s, type: %s, kind: %s, index: %s' % (
            declaration, type, kind, index)

        indent = '  ' * self.indent_level
        self.xml_output.write('%s<identifier> %s </identifier> %s\n' %
                              (indent, name, info))


class TagName(Enum):
    KEYWORD = 'keyword'
    SYMBOL = 'symbol'
    INTEGER_CONSTANT = 'integerConstant'
    STRING_CONSTANT = 'stringConstant'
    IDENTIFIER = 'identifier'
    CLASS = 'class'
    CLASS_VAR_DEC = 'classVarDec'
    SUBROUTINE_DEC = 'subroutineDec'
    PARAMETER_LIST = 'parameterList'
    SUBROUTINE_BODY = 'subroutineBody'
    VAR_DEC = 'varDec'
    STATEMENTS = 'statements'
    WHILE_STATEMENT = 'whileStatement'
    IF_STATEMENT = 'ifStatement'
    RETURN_STATEMENT = 'returnStatement'
    LET_STATEMENT = 'letStatement'
    DO_STATEMENT = 'doStatement'
    EXPRESSION = 'expression'
    TERM = 'term'
    EXPRESSION_LIST = 'expressionList'
