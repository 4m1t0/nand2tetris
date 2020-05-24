from enums import Enums


class SymbolTable:

    def __init__(self):
        self.static_table = {}
        self.field_table = {}
        self.arg_table = {}
        self.var_table = {}

    def startSubroutine(self):
        """新しいサブルーチンのスコープを開始する．
        つまり，サブルーチンのシンボルテーブルをリセットする．
        """
        self.arg_table = {}
        self.var_table = {}

    def define(self, name, type, kind):
        """引数の名前，型，属性で指定された新しい識別子を定義し，それに実行インデックスを割り当てる．
        STATICとFIELD属性の識別子はクラスのスコープを持ち，ARGとVAR属性の識別子はサブルーチンのスコープを持つ．

        Args:
            name (string): 引数名
            type (string): 型
            kind (string): 属性（STATIC, FIELD, ARG, VAR）
        """
        if kind is Enums.Kind.STATIC:
            self.static_table[name] = (
                type, kind, self.varCount(Enums.Kind.STATIC))
        elif kind is Enums.Kind.FIELD:
            self.field_table[name] = (
                type, kind, self.varCount(Enums.Kind.FIELD))
        elif kind is Enums.Kind.ARGUMENT:
            self.arg_table[name] = (
                type, kind, self.varCount(Enums.Kind.ARGUMENT))
        elif kind is Enums.Kind.VAR:
            self.var_table[name] = (
                type, kind, self.varCount(Enums.Kind.VAR))
        else:
            raise Exception('Invalid Kind: %s' % kind)

    def varCount(self, kind):
        """引数で与えられた属性について，それが現在のスコープで与えられている数を返す．

        Args:
            kind (Kind): 属性（STATIC, FIELD, ARG, VAR）

        Returns:
            int: スコープ内における指定された属性の数
        """
        if kind is Enums.Kind.STATIC:
            return len(self.static_table.keys())
        elif kind is Enums.Kind.FIELD:
            return len(self.field_table.keys())
        elif kind is Enums.Kind.ARGUMENT:
            return len(self.arg_table.keys())
        elif kind is Enums.Kind.VAR:
            return len(self.var_table.keys())
        else:
            raise Exception('Invalid Kind: %s' % kind)

    def kindOf(self, name):
        """引数で与えられた名前の識別子を現在のスコープで探し，その属性を返す．
        その識別子が現在のスコープで見つからなければ，NONEを返す．

        Args:
            name (string): 識別子

        Returns:
            Kind: 属性（STATIC, FIELD, ARG, VAR）
        """
        if name in self.arg_table.keys():
            return self.arg_table[name][1]
        elif name in self.var_table.keys():
            return self.var_table[name][1]
        elif name in self.static_table.keys():
            return self.static_table[name][1]
        elif name in self.field_table.keys():
            return self.field_table[name][1]
        else:
            return Enums.Kind.NONE

    def typeOf(self, name):
        """引数で与えられた名前の識別子を現在のスコープで探し，その型を返す．

        Args:
            name (string): 識別子

        Returns:
            string: 型
        """
        if name in self.arg_table.keys():
            return self.arg_table[name][0]
        elif name in self.var_table.keys():
            return self.var_table[name][0]
        elif name in self.static_table.keys():
            return self.static_table[name][0]
        elif name in self.field_table.keys():
            return self.field_table[name][0]
        else:
            raise Exception('Invalid name: %s' % name)

    def indexOf(self, name):
        """引数で与えられた名前の識別子を現在のスコープで探し，そのインデックスを返す．

        Args:
            name (string): 識別子

        Returns:
            int: シンボルテーブルにおけるインデックス
        """
        if name in self.arg_table.keys():
            return self.arg_table[name][2]
        elif name in self.var_table.keys():
            return self.var_table[name][2]
        elif name in self.static_table.keys():
            return self.static_table[name][2]
        elif name in self.field_table.keys():
            return self.field_table[name][2]
        else:
            raise Exception('Invalid name: %s' % name)
