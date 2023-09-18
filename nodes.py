'''
Abriga os nós de operação do 
'''


class SymbolTable():
    '''
    Serve como memória do compilador
    '''

    def __init__(self):
        self.symbol_table = {}

    def get(self, identifier):

        if identifier not in self.symbol_table:
            raise ValueError(f'ERRO EM SymbolTable: Variável {self.identifier} sem atribuição')
        
        return self.symbol_table[identifier]

    def set(self, identifier, value):
        self.symbol_table[identifier] = value


class Node():
    '''
    Classe base para nós representando operações

    Atributos:
     - value: varia de nó para nó
     - children: lista de nós

    Métodos: 
     - Evaluate(): varia de nó para nó
    '''

    def __init__(self, value, children: list):
        self.value = value
        self.children = children

    def evaluate(symbol_table: SymbolTable):
        pass


class BinOp(Node):
    '''
    Binary Operation - podendo ser +, -, *, /
    
    Contém 2 filhos
    '''

    def evaluate(self, symbol_table: SymbolTable):
        if self.value == '+':
            return self.children[0].evaluate() + self.children[1].evaluate()
        elif self.value == '-':
            return self.children[0].evaluate() - self.children[1].evaluate()
        elif self.value == '*':
            return self.children[0].evaluate() * self.children[1].evaluate()
        elif self.value == '/':
            return self.children[0].evaluate() // self.children[1].evaluate()


class UnOp(Node):
    '''
    Unary Operation - podendo ser + ou -

    Contém apenas um filho
    '''

    def evaluate(self, symbol_table: SymbolTable):
        if self.value == '-':
            return -self.children[0].evaluate()
        elif self.value == '+':
            return self.children[0].evaluate()


class IntVal(Node):
    '''
    Integer Value - Representa um valor inteiro

    Não contém filhos
    '''

    def evaluate(self, symbol_table: SymbolTable):
        return self.value


class NoOp(Node):
    '''
    No Operation - Nó Dummy

    Não contém filhos
    '''

    def evaluate(self, symbol_table: SymbolTable):
        return None


class Identifier(Node):
    '''
    Identificador - Variável à qual é atribuido um valor

    Não contém filhos
    '''

    def evaluate(self, symbol_table: SymbolTable):
        return symbol_table.get(identifier=self.value)


class Print(Node):
    '''
    Print

    Contém apenas um filho
    '''

    def evaluate(self, symbol_table: SymbolTable):
        print(self.children[0].evaluate())


class Block(Node):
    '''
    Bloco
    Contém n filhos (um por linha com instruções do programa)

    Não possui value
    '''

    def evaluate(self):
        for child in self.children:
            child.evaluate()


class Assignment(Node):
    '''
    Representa variável

    Possui 2 filhos:
     - children[0] -> identifier
     - children[1] -> ast
    '''
    def evaluate(self, symbol_table: SymbolTable):
        variable = self.children[0].value()
        ast_result = self.children[1]
        symbol_table.set(identifier=variable, value=ast_result)