from enum import Enum
from enums import Enums


class CompilationEngine:

    def __init__(self, input_file, tokenizer):
        self.indent_level = 0
        self.tokenizer = tokenizer

        self.output = open(input_file.replace('.jack', '_compiled.xml'), 'w')
        self.compileClass()
        self.output.close()

    def compileClass(self):
        """クラスをコンパイルする．
        """

        self._writeElementStart(TagName.CLASS)

        self.compileKeyword()
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
        if self.tokenizer.symbol() is Enums.Symbol.LESS_THAN_SIGN:
            symbol = '&lt;'
            self._writeElement(TagName.SYMBOL, symbol)
        elif self.tokenizer.symbol() is Enums.Symbol.GREATER_THAN_SIGN:
            symbol == '&gt;'
            self._writeElement(TagName.SYMBOL, symbol)
        elif self.tokenizer.symbol() is Enums.Symbol.AMPERSAND:
            symbol == '&amp;'
            self._writeElement(TagName.SYMBOL, symbol)
        else:
            self._writeElement(TagName.SYMBOL, self.tokenizer.symbol().value)

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
        self._writeElement(TagName.STRING_CONSTANT,
                           self.tokenizer.stringVal())

        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

    def compileClassVarDec(self):
        """スタティック宣言またはフィールド宣言をコンパイルする．
        """
        self._writeElementStart(TagName.CLASS_VAR_DEC)

        self.compileKeyword()
        if self.tokenizer.tokenType() is Enums.Token.KEYWORD \
            and self.tokenizer.keyword() in \
                (Enums.Keyword.INT,
                 Enums.Keyword.CHAR,
                 Enums.Keyword.BOOLEAN):
            self.compileKeyword()
        else:
            self.compileIdentifier()
        self.compileIdentifier()
        while self.tokenizer.tokenType() is Enums.Token.SYMBOL \
                and self.tokenizer.symbol() is Enums.Symbol.COMMA:
            self.compileSymbol()
            self.compileIdentifier()
        self.compileSymbol()

        self._writeElementEnd(TagName.CLASS_VAR_DEC)

    def compileSubroutine(self):
        """メソッド，ファンクション，コンストラクタをコンパイルする．
        """
        self._writeElementStart(TagName.SUBROUTINE_DEC)

        self.compileKeyword()
        if self.tokenizer.tokenType() is Enums.Token.KEYWORD \
                and self.tokenizer.keyword() is Enums.Keyword.VOID:
            self.compileKeyword()
        else:
            if self.tokenizer.tokenType() is Enums.Token.KEYWORD \
                and self.tokenizer.keyword() in \
                    (Enums.Keyword.INT,
                     Enums.Keyword.CHAR,
                     Enums.Keyword.BOOLEAN):
                self.compileKeyword()
            else:
                self.compileIdentifier()
        self.compileIdentifier()
        self.compileSymbol()
        self.compileParameterList()
        self.compileSymbol()

        self._writeElementStart(TagName.SUBROUTINE_BODY)

        self.compileSymbol()
        while self.tokenizer.tokenType() is Enums.Token.KEYWORD \
                and self.tokenizer.keyword() is Enums.Keyword.VAR:
            self.compileVarDec()
        self.compileStatements()
        self.compileSymbol()

        self._writeElementEnd(TagName.SUBROUTINE_BODY)

        self._writeElementEnd(TagName.SUBROUTINE_DEC)

    def compileParameterList(self):
        """パラメータのリスト（空の可能性もある）をコンパイルする．"()" は含まない．
        """
        self._writeElementStart(TagName.PARAMETER_LIST)

        while self.tokenizer.tokenType() is Enums.Token.KEYWORD \
            and self.tokenizer.keyword() in (
                Enums.Keyword.INT, Enums.Keyword.CHAR,
                Enums.Keyword.BOOLEAN):
            if self.tokenizer.tokenType() is Enums.Token.KEYWORD \
                and self.tokenizer.keyword() in \
                    (Enums.Keyword.INT,
                     Enums.Keyword.CHAR,
                     Enums.Keyword.BOOLEAN):
                self.compileKeyword()
            else:
                self.compileIdentifier()
            self.compileIdentifier()

            while self.tokenizer.tokenType() is Enums.Token.SYMBOL \
                    and self.tokenizer.symbol() is Enums.Symbol.COMMA:
                self.compileSymbol()
                if self.tokenizer.tokenType() is Enums.Token.KEYWORD \
                    and self.tokenizer.keyword() in \
                        (Enums.Keyword.INT,
                         Enums.Keyword.CHAR,
                         Enums.Keyword.BOOLEAN):
                    self.compileKeyword()
                else:
                    self.compileIdentifier()
                self.compileIdentifier()

        self._writeElementEnd(TagName.PARAMETER_LIST)

    def compileVarDec(self):
        """var宣言をコンパイルする．
        """
        self._writeElementStart(TagName.VAR_DEC)

        self.compileKeyword()  # var
        if self.tokenizer.tokenType() is Enums.Token.KEYWORD \
            and self.tokenizer.keyword() in \
                (Enums.Keyword.INT,
                 Enums.Keyword.CHAR,
                 Enums.Keyword.BOOLEAN):
            self.compileKeyword()
        else:
            self.compileIdentifier()
        self.compileIdentifier()
        while self.tokenizer.tokenType() is Enums.Token.SYMBOL \
                and self.tokenizer.symbol() is Enums.Symbol.COMMA:
            self.compileSymbol()
            self.compileIdentifier()
        self.compileSymbol()

        self._writeElementEnd(TagName.VAR_DEC)

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

    def compileDo(self):
        """do文をコンパイルする．
        """
        self._writeElementStart(TagName.DO_STATEMENT)

        self.compileKeyword()  # do

        self.compileIdentifier()
        if self.tokenizer.tokenType() is Enums.Token.SYMBOL \
                and self.tokenizer.symbol() is Enums.Symbol.PERIOD:
            self.compileSymbol()  # .
            self.compileIdentifier()

        self.compileSymbol()  # (
        self.compileExpressionList()
        self.compileSymbol()  # )

        self.compileSymbol()  # ;

        self._writeElementEnd(TagName.DO_STATEMENT)

    def compileLet(self):
        """let文をコンパイルする．
        """
        self._writeElementStart(TagName.LET_STATEMENT)

        self.compileKeyword()
        self.compileIdentifier()
        while self.tokenizer.tokenType() is not Enums.Token.SYMBOL \
            or (self.tokenizer.tokenType() is Enums.Token.SYMBOL
                and self.tokenizer.symbol() is not Enums.Symbol.EQUAL):
            self.compileSymbol()
            self.compileExpression()
            self.compileSymbol()
        self.compileSymbol()
        self.compileExpression()
        self.compileSymbol()

        self._writeElementEnd(TagName.LET_STATEMENT)

    def compileWhile(self):
        """while文をコンパイルする．
        """
        self._writeElementStart(TagName.WHILE_STATEMENT)

        self.compileKeyword()  # while
        self.compileSymbol()  # (
        self.compileExpression()  # 式
        self.compileSymbol()  # )
        self.compileSymbol()  # {
        self.compileStatements()  # 文
        self.compileSymbol()  # }

        self._writeElementEnd(TagName.WHILE_STATEMENT)

    def compileReturn(self):
        """return文をコンパイルする．
        """
        self._writeElementStart(TagName.RETURN_STATEMENT)

        self.compileKeyword()  # return
        while self.tokenizer.tokenType() is not Enums.Token.SYMBOL \
            or (self.tokenizer.tokenType() is Enums.Token.SYMBOL
                and self.tokenizer.symbol() is not Enums.Symbol.SEMI_COLON):
            self.compileExpression()  # 式
        self.compileSymbol()  # ;

        self._writeElementEnd(TagName.RETURN_STATEMENT)

    def compileIf(self):
        """if文をコンパイルする．else文を扱う可能性がある．
        """
        self._writeElementStart(TagName.IF_STATEMENT)

        self.compileKeyword()  # if
        self.compileSymbol()  # (
        self.compileExpression()  # 式
        self.compileSymbol()  # )
        self.compileSymbol()  # {
        self.compileStatements()  # 文
        self.compileSymbol()  # }

        if self.tokenizer.tokenType() is Enums.Token.KEYWORD \
                and self.tokenizer.keyword() is Enums.Keyword.ELSE:
            self.compileKeyword()  # else
            self.compileSymbol()  # {
            self.compileStatements()  # 文
            self.compileSymbol()  # }

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
            self.compileSymbol()
            self.compileTerm()

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
            self.compileIntegerConstant()
        elif self.tokenizer.tokenType() is Enums.Token.STRING_CONST:
            self.compileStringConstant()
        elif self.tokenizer.tokenType() is Enums.Token.KEYWORD:
            if self.tokenizer.keyword() in \
                    (Enums.Keyword.TRUE, Enums.Keyword.FALSE,
                     Enums.Keyword.NULL, Enums.Keyword.THIS):
                self.compileKeyword()
        elif self.tokenizer.tokenType() is Enums.Token.IDENTIFIER:
            self.compileIdentifier()

            if self.tokenizer.tokenType() is Enums.Token.SYMBOL and \
                    self.tokenizer.symbol() is Enums.Symbol.LEFT_SQUARE_BRACKET:
                self.compileSymbol()
                self.compileExpression()
                self.compileSymbol()
            elif self.tokenizer.tokenType() is Enums.Token.SYMBOL and \
                    self.tokenizer.symbol() is Enums.Symbol.LEFT_ROUND_BRACKET:
                self.compileSymbol()
                self.compileExpressionList()
                self.compileSymbol()
            elif self.tokenizer.tokenType() is Enums.Token.SYMBOL and \
                    self.tokenizer.symbol() is Enums.Symbol.PERIOD:
                self.compileSymbol()
                self.compileIdentifier()
                self.compileSymbol()
                self.compileExpressionList()
                self.compileSymbol()
        elif self.tokenizer.tokenType() is Enums.Token.SYMBOL and \
                self.tokenizer.symbol() is Enums.Symbol.LEFT_ROUND_BRACKET:
            self.compileSymbol()
            self.compileExpression()
            self.compileSymbol()
        elif self.tokenizer.tokenType() is Enums.Token.SYMBOL and \
                self.tokenizer.symbol() in (Enums.Symbol.HYPHEN, Enums.Symbol.TILDE):
            self.compileSymbol()
            self.compileTerm()

        self._writeElementEnd(TagName.TERM)

    def compileExpressionList(self):
        """コンマで分離された式のリスト（空の可能性もある）をコンパイルする．
        """
        self._writeElementStart(TagName.EXPRESSION_LIST)

        while self.tokenizer.tokenType() is not Enums.Token.SYMBOL \
            or (self.tokenizer.tokenType() is Enums.Token.SYMBOL
                and self.tokenizer.symbol() is not Enums.Symbol.RIGHT_ROUND_BRACKET):
            self.compileExpression()

            while self.tokenizer.tokenType() is not Enums.Token.SYMBOL \
                or (self.tokenizer.tokenType() is Enums.Token.SYMBOL
                    and self.tokenizer.symbol() is Enums.Symbol.COMMA):
                self.compileSymbol()
                self.compileExpression()

        self._writeElementEnd(TagName.EXPRESSION_LIST)

    def _writeElement(self, tag_name, value):
        """要素を書き出す．

        Args:
            tag_name (TagName): タグ名
            value (string): 値
        """
        indent = '  ' * self.indent_level
        self.output.write('%s<%s> %s </%s>\n' %
                          (indent, tag_name.value, value, tag_name.value))

    def _writeElementStart(self, tag_name):
        """開始要素を書き出す．

        Args:
            tag_name (TagName): タグ名
        """
        indent = '  ' * self.indent_level
        self.output.write('%s<%s>\n' % (indent, tag_name.value))
        self.indent_level += 1

    def _writeElementEnd(self, tag_name):
        """終了要素を書き出す．

        Args:
            tag_name (TagName): タグ名
        """
        self.indent_level -= 1
        indent = '  ' * self.indent_level
        self.output.write('%s</%s>\n' % (indent, tag_name.value))


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
