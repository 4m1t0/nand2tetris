from collections import deque
from enums import Enums
import re
import sys


class JackTokenizer:

    def __init__(self, input_file):
        """入力ファイルを開き，トークン化を行う準備をする．

        Args:
            input_file (string): ファイルパス
        """
        self.tokens = deque([])
        for line in self._deleteCommentsAndEmptyLines(input_file):
            while line:
                double_quote_index = line.find('"')
                space_index = line.find(' ')
                if line.startswith('"'):
                    index = line.find('"', 1)
                    self.tokens.append(line[0:index+1])
                    line = line[index+1:].strip()
                elif double_quote_index != -1 and space_index != 1 \
                        and double_quote_index < space_index:
                    self.tokens.extend(self._tokenize(
                        line[0:double_quote_index]))
                    line = line[double_quote_index:].strip()
                elif space_index != -1:
                    self.tokens.extend(self._tokenize(line[0:space_index]))
                    line = line[space_index:].strip()
                else:
                    self.tokens.extend(self._tokenize(line))
                    line = ''

        self.current_token = ''
        self.advance()

    def _deleteCommentsAndEmptyLines(self, input_file):
        """コメントや空文字など不要なものを削除する．

        Args:
            input_file (File): ファイル

        Returns:
            list: コメントや空文字削除済みの文字列のリスト
        """
        _input_file = open(input_file, 'r')
        # 1行コメントのみ，空文字の行は無視
        # コード内の1行コメントはコメントを削除
        _lines = [line.split("//")[0].strip()
                  for line in _input_file.readlines()
                  if line.split("//")[0].strip()]
        _input_file.close()

        # 複数行コメントの削除
        __lines = []
        multi_line_comment_flag = False
        multi_line_comment_start_pattern = re.compile(r'.*\/\*')
        multi_line_comment_end_pattern = re.compile(r'.*\*\/')
        for line in _lines:
            if multi_line_comment_start_pattern.match(line):
                multi_line_comment_flag = True
            if multi_line_comment_end_pattern.match(line):
                multi_line_comment_flag = False
                continue
            if not multi_line_comment_flag:
                __lines.append(line)

        return __lines

    tokenizer_regex = re.compile(r'[\{\}\(\)\[\]\.,;\+\-\*\/&\|<>=~]')

    def _tokenize(self, s):
        """入力された文字列のトークン化を行う．

        Args:
            s (string): トークン化対象の文字列

        Returns:
            list: トークンのリスト
        """
        tokens = []
        while s:
            if JackTokenizer.tokenizer_regex.search(s):
                index = JackTokenizer.tokenizer_regex.search(s).start()

                if index != 0:
                    tokens.append(s[0:index])

                tokens.append(s[index:index+1])
                s = s[index+1:]
            else:
                tokens.append(s)
                s = ''

        return tokens

    def hasMoreTokens(self):
        """入力にまだトークンは存在するか？
        """
        return True if len(self.tokens) else False

    def advance(self):
        """入力から次のトークンを取得し，それを現トークンとする．
        このルーチンはhasMoreTokens()がtrueの場合のみ呼び出すことができる．
        また，最初は現トークンは設定されていない．
        """
        self.current_token = self.tokens.popleft()

    int_const_regex = re.compile(r'[0-9]+$')
    identifier_regex = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')
    string_regex = re.compile(r'^"[^"\n]*"$')

    def tokenType(self):
        """現トークンの種類を返す．

        Returns:
            Token: 現在のトークン
        """
        if self.current_token in [keyword.value for keyword in Enums.Keyword]:
            return Enums.Token.KEYWORD
        elif self.current_token in [symbol.value for symbol in Enums.Symbol]:
            return Enums.Token.SYMBOL
        elif JackTokenizer.int_const_regex.match(self.current_token) \
                and int(self.current_token) <= 32627:
            return Enums.Token.INT_CONST
        elif JackTokenizer.identifier_regex.match(self.current_token):
            return Enums.Token.IDENTIFIER
        elif JackTokenizer.string_regex.match(self.current_token):
            return Enums.Token.STRING_CONST

        print('Invalid token: %s' % self.current_token)
        sys.exit(1)

    def keyword(self):
        """現トークンのキーワードを返す．このルーチンはtokenType()がKEYWORDの場合のみ呼び出すことができる．

        Returns:
            Keyword: 現トークンのキーワード
        """
        if self.tokenType() is not Enums.Token.KEYWORD:
            print('Invalid usage at keyword: %s' % self.current_token)
            sys.exit(1)
        return Enums.Keyword(self.current_token)

    def symbol(self):
        """現トークンの文字を返す，このルーチンはtokenType()がSYMBOLの場合のみ呼び出すことができる．

        Returns:
            string: 現トークンの文字
        """
        if self.tokenType() is not Enums.Token.SYMBOL:
            print('Invalid usage at symbol: %s' % self.current_token)
            sys.exit(1)
        return Enums.Symbol(self.current_token)

    def identifier(self):
        """現トークンの識別子（identifier）を返す，このルーチンはtokenType()がIDENTIFIERの場合のみ呼び出すことができる．

        Returns:
            string: 現トークンの識別子
        """
        if self.tokenType() is not Enums.Token.IDENTIFIER:
            print('Invalid usage at identifier: %s' % self.current_token)
            sys.exit(1)
        return self.current_token

    def intVal(self):
        """現トークンの整数の値を返す，このルーチンはtokenType()がINT_CONSTの場合のみ呼び出すことができる．

        Returns:
            int: 現トークンの整数の値
        """
        if self.tokenType() is not Enums.Token.INT_CONST:
            print('Invalid usage at intVal: %s' % self.current_token)
            sys.exit(1)
        return self.current_token

    def stringVal(self):
        """現トークンの文字列を返す，このルーチンはtokenType()がSTRING_CONSTの場合のみ呼び出すことができる．

        Returns:
            string: 現トークンの文字列
        """
        if self.tokenType() is not Enums.Token.STRING_CONST:
            print('Invalid usage at stringVal: %s' % self.current_token)
            sys.exit(1)
        return self.current_token[1:-1]
