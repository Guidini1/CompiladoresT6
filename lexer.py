import enum
import sys

class Lexer:
    # Construtor do Lexer
    def __init__(self, source):
        self.source = source + '\n' 
        self.CharAtual = ''  
        self.PosAtual = -1    
        self.proximoChar()

    # Atualiza o CharAtual para o próximo (PosAtual = PosAtual + 1)
    def proximoChar(self):
        self.PosAtual += 1
        if self.PosAtual >= len(self.source):
            self.CharAtual = '\0'  
        else:
            self.CharAtual = self.source[self.PosAtual]

    # Verifica se ainda está nos limites do arquivo source (texte.txt)
    def checa(self):
        if self.PosAtual + 1 >= len(self.source):
            return '\0'
        return self.source[self.PosAtual+1]

    # Aborta a execução do programa caso tenha um erro léxico, que quebra pelo menos uma regra da gramática definida
    def abort(self, mensagem):
        sys.exit("Erro Lexico. " + mensagem)

    # Pega, identifica e retorna o token ou mensagem de erro
    def pegaToken(self):
        self.pulaEspacoBranco()
        self.pulaComentario()
        token = None

        if self.CharAtual == '+':
            token = Token(self.CharAtual, TokenTipo.MAIS)
        elif self.CharAtual == '-':
            token = Token(self.CharAtual, TokenTipo.MENOS)
        elif self.CharAtual == '*':
            token = Token(self.CharAtual, TokenTipo.VEZES)
        elif self.CharAtual == '/':
            token = Token(self.CharAtual, TokenTipo.IGUAL)
        elif self.CharAtual == '=':
            if self.checa() == '=':
                lastChar = self.CharAtual
                self.proximoChar()
                token = Token(lastChar + self.CharAtual, TokenTipo.IGUALIGUAL)
            else:
                token = Token(self.CharAtual, TokenTipo.IGUAL)
        elif self.CharAtual == '>':
            if self.checa() == '=':
                lastChar = self.CharAtual
                self.proximoChar()
                token = Token(lastChar + self.CharAtual, TokenTipo.MAISIGUAL)
            else:
                token = Token(self.CharAtual, TokenTipo.MAISQUE)
        elif self.CharAtual == '<':
            if self.checa() == '=':
                lastChar = self.CharAtual
                self.proximoChar()
                token = Token(lastChar + self.CharAtual, TokenTipo.MENOSIGUAL)
            else:
                token = Token(self.CharAtual, TokenTipo.MENOSQUE)
        elif self.CharAtual == '!':
            if self.checa() == '=':
                lastChar = self.CharAtual
                self.proximoChar()
                token = Token(lastChar + self.CharAtual, TokenTipo.DIFERENTE)
            else:
                self.abort("Esperado !=, recebeu !" + self.checa())

        elif self.CharAtual == '\"':
            self.proximoChar()
            PosInicio = self.PosAtual

            while self.CharAtual != '\"':
                if self.CharAtual == '\r' or self.CharAtual == '\n' or self.CharAtual == '\t' or self.CharAtual == '\\' or self.CharAtual == '%':
                    self.abort("Caractere ilegal na String.")
                self.proximoChar()

            TextoToken = self.source[PosInicio : self.PosAtual]
            token = Token(TextoToken, TokenTipo.STRING)

        elif self.CharAtual.isdigit():
            PosInicio = self.PosAtual
            while self.checa().isdigit():
                self.proximoChar()
            if self.checa() == '.': 
                self.proximoChar()
                if not self.checa().isdigit(): 
                    # Error!
                    self.abort("Caractere ilegal em Numero.")
                while self.checa().isdigit():
                    self.proximoChar()

            TextoToken = self.source[PosInicio : self.PosAtual + 1] 
            token = Token(TextoToken, TokenTipo.NUMERO)
        elif self.CharAtual.isalpha():
            PosInicio = self.PosAtual
            while self.checa().isalnum():
                self.proximoChar()

            TextoToken = self.source[PosInicio : self.PosAtual + 1]
            keyword = Token.checaSePalavraChave(TextoToken)
            if keyword == None: 
                token = Token(TextoToken, TokenTipo.IDENT)
            else:   
                token = Token(TextoToken, keyword)
        elif self.CharAtual == '\n':
            token = Token('\n', TokenTipo.NOVALINHA)
        elif self.CharAtual == '\0':
            token = Token('', TokenTipo.EOF)
        else:
            self.abort("Unknown token: " + self.CharAtual)

        self.proximoChar()
        return token

    # Ignora Espaços em Branco (espaço, tab, enter)
    def pulaEspacoBranco(self):
        while self.CharAtual == ' ' or self.CharAtual == '\t' or self.CharAtual == '\r':
            self.proximoChar()

    # Ignora comentários (partes no código que iniciam com #)
    def pulaComentario(self):
        if self.CharAtual == '#':
            while self.CharAtual != '\n':
                self.proximoChar()

# Define o que é um token
class Token:   
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText  
        self.kind = tokenKind  

    @staticmethod
    def checaSePalavraChave(tokenText):
        for kind in TokenTipo:
            if kind.name == tokenText and kind.value >= 100 and kind.value < 200:
                return kind
        return None

# Define os possíveis tipos de token que são aceitos
class TokenTipo(enum.Enum):
    EOF = -1
    NOVALINHA = 0
    NUMERO = 1
    IDENT = 2
    STRING = 3

    IMPRIME = 103
    ENTRADA = 104
    NUM = 105
    SE = 106
    ENTAO = 107
    FIMSE = 108
    ENQUANTO = 109
    REPETE = 110
    FIMENQUANTO = 111
    CONSTNUM = 112
    CONSTSTR = 113
    STR = 114

    IGUAL = 201  
    MAIS = 202
    MENOS = 203
    VEZES = 204
    BARRA = 205
    IGUALIGUAL = 206
    DIFERENTE = 207
    MENOSQUE = 208
    MENOSIGUAL = 209
    MAISQUE = 210
    MAISIGUAL = 211
