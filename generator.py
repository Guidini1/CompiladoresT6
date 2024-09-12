class Generator:
    def __init__(self, filename):
        self.filename = filename
        self.code = []
        self.indent_level = 0

    def gen(self, text):
        """ Adiciona um trecho de código ao final da linha atual. """
        if self.code:
            self.code[-1] += text
        else:
            # Caso não exista nenhuma linha ainda, adiciona uma nova linha com o texto
            self.code.append('    ' * self.indent_level + text)

    def genLine(self, text):
        """ Adiciona uma nova linha de código, apenas se não houver código na linha atual. """
        if not self.code or self.code[-1].strip():  # Verifica se a linha atual não está vazia
            if self.indent_level > 0:
                text = '    ' * self.indent_level + text
            self.code.append(text)
        else:
            # Se a linha atual estiver vazia, substitui pelo novo texto sem adicionar linha extra
            self.code[-1] = text

    def headerLine(self, text):
        """ Adiciona uma linha de código ao início da lista de código. """
        self.code.insert(0, text)

    def writeFile(self):
        """ Escreve o código gerado no arquivo especificado sem nova linha extra no final. """
        with open(self.filename, 'w') as f:
            f.write('\n'.join(self.code))

    def increaseIndent(self):
        """ Aumenta o nível de indentação. """
        self.indent_level += 1

    def decreaseIndent(self):
        """ Diminui o nível de indentação. """
        if self.indent_level > 0:
            self.indent_level -= 1