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

    def get_table(self):
        return self.symbol_table


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

    def evaluate(self, symbol_table: SymbolTable):
        pass


class BinOp(Node):
    '''
    Binary Operation - podendo ser +, -, *, /
    
    Contém 2 filhos
    '''

    def evaluate(self, symbol_table: SymbolTable):
        if self.value == '+':
            return self.children[0].evaluate(symbol_table) + self.children[1].evaluate(symbol_table)
        elif self.value == '-':
            return self.children[0].evaluate(symbol_table) - self.children[1].evaluate(symbol_table)
        elif self.value == '*':
            return self.children[0].evaluate(symbol_table) * self.children[1].evaluate(symbol_table)
        elif self.value == '/':
            return self.children[0].evaluate(symbol_table) // self.children[1].evaluate(symbol_table)


class UnOp(Node):
    '''
    Unary Operation - podendo ser + ou -

    Contém apenas um filho
    '''

    def evaluate(self, symbol_table: SymbolTable):
        if self.value == '-':
            return -self.children[0].evaluate(symbol_table)
        elif self.value == '+':
            return self.children[0].evaluate(symbol_table)


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
        print(self.children[0].evaluate(symbol_table))


class Block(Node):
    '''
    Bloco
    Contém n filhos (um por linha com instruções do programa)

    Não possui value
    '''

    def evaluate(self, symbol_table: SymbolTable):
        for child in self.children:
            child.evaluate(symbol_table)


class Assignment(Node):
    '''
    Representa variável

    Possui 2 filhos:F
     - children[0] -> identifier
     - children[1] -> ast
    '''
    def evaluate(self, symbol_table: SymbolTable):
        variable = self.children[0].value
        ast_result = self.children[1].evaluate(symbol_table)
        symbol_table.set(identifier=variable, value=ast_result)