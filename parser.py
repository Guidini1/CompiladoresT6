import sys
from lexer import TokenTipo

class Parser:
    def __init__(self, lexer, generator):
        self.lexer = lexer
        self.generator = generator

        self.simbolos = set()
        self.constsnum = set()
        self.constsstring = set()
        self.strings = set()

        self.TokenAtual = None
        self.checaToken = None
        self.proximoToken()
        self.proximoToken()

    def checkToken(self, kind):
        return kind == self.TokenAtual.kind

    def match(self, kind):
        if not self.checkToken(kind):
            self.abort(f"1 Esperado -{self.TokenAtual.text}-{kind.name}, recebeu {self.TokenAtual.kind.name}")
        self.proximoToken()

    def proximoToken(self):
        self.TokenAtual = self.checaToken
        self.checaToken = self.lexer.pegaToken()

    def ehOperadorComparacao(self):
        return self.checkToken(TokenTipo.MAISQUE) or self.checkToken(TokenTipo.MAISIGUAL) or self.checkToken(TokenTipo.MENOSQUE) or self.checkToken(TokenTipo.MENOSIGUAL) or self.checkToken(TokenTipo.IGUALIGUAL) or self.checkToken(TokenTipo.DIFERENTE)

    def abort(self, mensagem):
        sys.exit("Erro! " + mensagem)

    def programa(self):
        while self.checkToken(TokenTipo.NOVALINHA):
            self.proximoToken()

        while not self.checkToken(TokenTipo.EOF):
            self.declaracao()

    def declaracao(self):
        if self.checkToken(TokenTipo.IMPRIME):
            self.proximoToken()
            if self.checkToken(TokenTipo.STRING):
                self.generator.genLine(f"print({self.TokenAtual.text})")
                self.proximoToken()
            else:
                # Gera o print em uma única linha
                self.generator.gen("print(")   # Não gera quebra de linha aqui
                self.expressao()
                self.generator.gen(")")        # Gera o fechamento do parêntese na mesma linha
                self.generator.genLine("")     # Adiciona uma quebra de linha depois de fechar o print

        elif self.checkToken(TokenTipo.SE):
            self.proximoToken()
            self.generator.gen("if ")
            self.comparacao()
            self.match(TokenTipo.ENTAO)
            self.generator.gen(":")  # Adiciona o ':' na mesma linha do if
            self.nl()  # Pula para a próxima linha
            self.generator.increaseIndent()
            while not self.checkToken(TokenTipo.FIMSE):
                self.declaracao()
            self.generator.decreaseIndent()
            self.match(TokenTipo.FIMSE)
            self.nl()


        elif self.checkToken(TokenTipo.ENQUANTO):
            self.proximoToken()
            self.generator.gen("while ")
            self.comparacao()
            self.match(TokenTipo.REPETE)
            self.nl()
            self.generator.genLine(":")
            self.generator.increaseIndent()
            while not self.checkToken(TokenTipo.FIMENQUANTO):
                self.declaracao()
            self.generator.decreaseIndent()
            self.match(TokenTipo.FIMENQUANTO)
            self.nl()

        elif self.checkToken(TokenTipo.NUM):
            self.proximoToken()
            if self.TokenAtual.text in self.constsnum or self.TokenAtual.text in self.constsstring:
                self.abort(f"Não pode atribuir um valor para a constante: {self.TokenAtual.text}")
            elif self.TokenAtual.text in self.strings:
                self.abort(f"Não pode atribuir um número para a string: {self.TokenAtual.text}")
            if self.TokenAtual.text not in self.simbolos:
                self.simbolos.add(self.TokenAtual.text)
                self.generator.genLine(f'{self.TokenAtual.text} = ')

            self.match(TokenTipo.IDENT)
            self.match(TokenTipo.IGUAL)
            if self.checkToken(TokenTipo.STRING):
                self.abort(f"Não pode atribuir uma string para um número: {self.TokenAtual.text}")
            self.expressao()
            self.generator.genLine("")

        elif self.checkToken(TokenTipo.STR):
            self.proximoToken()
            if self.TokenAtual.text in self.constsnum or self.TokenAtual.text in self.constsstring:
                self.abort(f"Não pode atribuir um valor para a constante: {self.TokenAtual.text}")
            elif self.TokenAtual.text in self.simbolos:
                self.abort(f"Não pode atribuir uma string para um número: {self.TokenAtual.text}")
            elif self.TokenAtual.text not in self.strings:
                self.strings.add(self.TokenAtual.text)
                self.generator.genLine(f'{self.TokenAtual.text} = ')

            self.match(TokenTipo.IDENT)
            self.match(TokenTipo.IGUAL)
            if self.checkToken(TokenTipo.NUMERO):
                self.abort(f"Não pode atribuir um número para uma string: {self.TokenAtual.text}")
            self.expressao()
            self.generator.genLine("")

        elif self.checkToken(TokenTipo.CONSTNUM):
            self.proximoToken()
            if self.TokenAtual.text in self.simbolos or self.TokenAtual.text in self.strings:
                self.abort(f"Variável já existe: {self.TokenAtual.text}")
            if self.TokenAtual.text in self.constsnum:
                self.abort(f"Constante já existe: {self.TokenAtual.text}")
            self.constsnum.add(self.TokenAtual.text)
            self.generator.genLine(f"const {self.TokenAtual.text} = ")
            self.match(TokenTipo.IDENT)
            if self.checkToken(TokenTipo.STRING):
                self.abort(f"Não pode atribuir uma string constante para um número constante: {self.TokenAtual.text}")
            self.expressao()
            self.generator.genLine("")

        elif self.checkToken(TokenTipo.CONSTSTR):
            self.proximoToken()
            if self.TokenAtual.text in self.simbolos or self.TokenAtual.text in self.strings:
                self.abort(f"Variável já existe: {self.TokenAtual.text}")
            if self.TokenAtual.text in self.constsstring:
                self.abort(f"Constante já existe: {self.TokenAtual.text}")
            self.constsstring.add(self.TokenAtual.text)
            self.generator.genLine(f"const {self.TokenAtual.text} = ")
            self.match(TokenTipo.IDENT)
            if self.checkToken(TokenTipo.NUMERO):
                self.abort(f"Não pode atribuir um número constante para uma string constante: {self.TokenAtual.text}")
            self.expressao()
            self.generator.genLine("")

        elif self.checkToken(TokenTipo.ENTRADA):
            self.proximoToken()
            if self.TokenAtual.text in self.constsnum or self.TokenAtual.text in self.constsstring:
                self.abort(f"Não pode atribuir um valor para a constante: {self.TokenAtual.text}")
            if self.TokenAtual.text not in self.simbolos:
                self.simbolos.add(self.TokenAtual.text)
                self.generator.genLine(f'{self.TokenAtual.text} = ')

            self.generator.genLine(f'{self.TokenAtual.text} = input()')
            self.match(TokenTipo.IDENT)

        else:
            self.abort(f"Declaração inválida em {self.TokenAtual.text} ({self.TokenAtual.kind.name})")

        self.nl()


    def comparacao(self):
        self.expressao()
        if self.ehOperadorComparacao():
            self.generator.gen(self.TokenAtual.text)
            self.proximoToken()
            self.expressao()
        while self.ehOperadorComparacao():
            self.generator.gen(self.TokenAtual.text)
            self.proximoToken()
            self.expressao()

    def expressao(self):
        self.termo()
        while self.checkToken(TokenTipo.MAIS) or self.checkToken(TokenTipo.MENOS):
            self.generator.gen(self.TokenAtual.text)
            self.proximoToken()
            self.termo()

    def termo(self):
        self.unario()
        while self.checkToken(TokenTipo.VEZES) or self.checkToken(TokenTipo.BARRA):
            self.generator.gen(self.TokenAtual.text)
            self.proximoToken()
            self.unario()

    def unario(self):
        if self.checkToken(TokenTipo.MAIS) or self.checkToken(TokenTipo.MENOS):
            self.generator.gen(self.TokenAtual.text)
            self.proximoToken()
        self.primario()

    def primario(self):
        if self.checkToken(TokenTipo.NUMERO):
            self.generator.gen(self.TokenAtual.text)
            self.proximoToken()
        elif self.checkToken(TokenTipo.STRING):
            self.generator.gen(f"\"{self.TokenAtual.text}\"")
            self.proximoToken()
        elif self.checkToken(TokenTipo.IDENT):
            if self.TokenAtual.text not in self.simbolos and self.TokenAtual.text not in self.strings and self.TokenAtual.text not in self.constsnum and self.TokenAtual.text not in self.constsstring:
                self.abort("16 Variável ou constante não declarada: " + self.TokenAtual.text)
            self.generator.gen(self.TokenAtual.text)
            self.proximoToken()
        elif self.checkToken(TokenTipo.NOVALINHA):
            self.proximoToken()
        else:
            self.abort("17 Expressão inválida: " + self.TokenAtual.text)

    def nl(self):
        while self.checkToken(TokenTipo.NOVALINHA):
            self.proximoToken()