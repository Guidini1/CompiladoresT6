import enum
import sys

# Classe responsável por fazer a análise léxica do código-fonte
class Lexer:
    # Construtor da classe Lexer
    def __init__(self, source):
        self.source = source + '\n'  # Adiciona uma nova linha ao final do código-fonte para evitar erros de leitura no final
        self.CharAtual = ''  # Caractere atual que está sendo processado
        self.PosAtual = -1   # Posição atual no código-fonte
        self.proximoChar()   # Avança para o primeiro caractere

    # Avança para o próximo caractere no código-fonte
    def proximoChar(self):
        self.PosAtual += 1  # Incrementa a posição atual
        if self.PosAtual >= len(self.source):  # Se a posição atual exceder o tamanho do código-fonte
            self.CharAtual = '\0'  # Define o caractere atual como fim de arquivo (EOF)
        else:
            self.CharAtual = self.source[self.PosAtual]  # Caso contrário, obtém o próximo caractere

    # Verifica o próximo caractere sem avançar a posição atual
    def checa(self):
        if self.PosAtual + 1 >= len(self.source):  # Se o próximo caractere estiver fora do limite do código-fonte
            return '\0'  # Retorna fim de arquivo (EOF)
        return self.source[self.PosAtual + 1]  # Caso contrário, retorna o próximo caractere

    # Função de erro que encerra o programa caso ocorra um erro léxico
    def abort(self, mensagem):
        sys.exit("Erro Lexico. " + mensagem)  # Exibe a mensagem de erro e encerra o programa

    # Função que identifica e retorna o próximo token encontrado
    def pegaToken(self):
        self.pulaEspacoBranco()  # Ignora espaços em branco
        self.pulaComentario()  # Ignora comentários
        token = None  # Inicializa o token como None

        # Identificação de operadores e símbolos
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
                token = Token(lastChar + self.CharAtual, TokenTipo.IGUALIGUAL)  # Verifica igualdade (==)
            else:
                token = Token(self.CharAtual, TokenTipo.IGUAL)  # Atribuição simples (=)
        elif self.CharAtual == '>':
            if self.checa() == '=':
                lastChar = self.CharAtual
                self.proximoChar()
                token = Token(lastChar + self.CharAtual, TokenTipo.MAISIGUAL)  # Maior ou igual (>=)
            else:
                token = Token(self.CharAtual, TokenTipo.MAISQUE)  # Apenas maior que (>)
        elif self.CharAtual == '<':
            if self.checa() == '=':
                lastChar = self.CharAtual
                self.proximoChar()
                token = Token(lastChar + self.CharAtual, TokenTipo.MENOSIGUAL)  # Menor ou igual (<=)
            else:
                token = Token(self.CharAtual, TokenTipo.MENOSQUE)  # Apenas menor que (<)
        elif self.CharAtual == '!':
            if self.checa() == '=':
                lastChar = self.CharAtual
                self.proximoChar()
                token = Token(lastChar + self.CharAtual, TokenTipo.DIFERENTE)  # Diferente (!=)
            else:
                self.abort("Esperado !=, recebeu !" + self.checa())  # Erro se '!' não for seguido de '='

        # Tratamento de strings
        elif self.CharAtual == '\"':
            self.proximoChar()  # Avança para o primeiro caractere da string
            PosInicio = self.PosAtual  # Marca a posição inicial da string

            # Continua até encontrar o final da string
            while self.CharAtual != '\"':
                # Verifica se há algum caractere ilegal dentro da string
                if self.CharAtual in ['\r', '\n', '\t', '\\', '%']:
                    self.abort("Caractere ilegal na String.")  # Se encontrar, aborta o programa
                self.proximoChar()

            # Extrai o texto da string
            TextoToken = self.source[PosInicio : self.PosAtual]
            token = Token(TextoToken, TokenTipo.STRING)  # Retorna o token do tipo STRING

        # Tratamento de números (inteiros ou decimais)
        elif self.CharAtual.isdigit():
            PosInicio = self.PosAtual  # Marca a posição inicial do número
            while self.checa().isdigit():
                self.proximoChar()  # Avança enquanto o próximo caractere for um dígito
            if self.checa() == '.':  # Verifica se é um número decimal
                self.proximoChar()
                if not self.checa().isdigit():
                    self.abort("Caractere ilegal em Numero.")  # Se após o ponto não houver dígitos, gera erro
                while self.checa().isdigit():
                    self.proximoChar()

            TextoToken = self.source[PosInicio : self.PosAtual + 1]  # Extrai o texto do número
            token = Token(TextoToken, TokenTipo.NUMERO)  # Retorna o token do tipo NUMERO

        # Tratamento de identificadores e palavras-chave
        elif self.CharAtual.isalpha():
            PosInicio = self.PosAtual  # Marca a posição inicial do identificador
            while self.checa().isalnum():
                self.proximoChar()  # Avança enquanto o próximo caractere for alfanumérico

            TextoToken = self.source[PosInicio : self.PosAtual + 1]  # Extrai o texto do identificador
            keyword = Token.checaSePalavraChave(TextoToken)  # Verifica se é uma palavra-chave
            if keyword is None: 
                token = Token(TextoToken, TokenTipo.IDENT)  # Se não for palavra-chave, trata como identificador
            else:   
                token = Token(TextoToken, keyword)  # Se for palavra-chave, retorna o token correspondente

        # Tratamento de nova linha
        elif self.CharAtual == '\n':
            token = Token('\n', TokenTipo.NOVALINHA)  # Token de nova linha

        # Tratamento do fim do arquivo
        elif self.CharAtual == '\0':
            token = Token('', TokenTipo.EOF)  # Token de fim de arquivo (EOF)

        # Caso nenhum dos casos anteriores, gera um erro
        else:
            self.abort("Unknown token: " + self.CharAtual)

        self.proximoChar()  # Avança para o próximo caractere
        return token  # Retorna o token identificado

    # Ignora espaços em branco no código-fonte
    def pulaEspacoBranco(self):
        while self.CharAtual in [' ', '\t', '\r']:
            self.proximoChar()  # Avança enquanto houver espaços em branco

    # Ignora comentários no código (comentários iniciam com '#')
    def pulaComentario(self):
        if self.CharAtual == '#':
            while self.CharAtual != '\n':  # Avança até o final da linha
                self.proximoChar()

# Classe que define um token
class Token:   
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText  # O texto do token
        self.kind = tokenKind  # O tipo do token

    # Função estática que verifica se um token é uma palavra-chave
    @staticmethod
    def checaSePalavraChave(tokenText):
        for kind in TokenTipo:
            if kind.name == tokenText and 100 <= kind.value < 200:  # Verifica se o valor está no intervalo de palavras-chave
                return kind
        return None

# Enumeração que define os tipos de tokens que podem ser gerados pelo Lexer
class TokenTipo(enum.Enum):
    EOF = -1  # Fim de arquivo
    NOVALINHA = 0  # Nova linha
    NUMERO = 1  # Número
    IDENT = 2  # Identificador
    STRING = 3  # String

    # Palavras-chave (valores entre 100 e 199)
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

    # Operadores e símbolos (valores acima de 200)
    IGUAL = 201  # '='
    MAIS = 202  # '+'
    MENOS = 203  # '-'
    VEZES = 204  # '*'
    BARRA = 205  # '/'
    IGUALIGUAL = 206  # '=='
    DIFERENTE = 207  # '!='
    MENOSQUE = 208  # '<'
    MENOSIGUAL = 209  # '<='
    MAISQUE = 210  # '>'
    MAISIGUAL = 211  # '>='
