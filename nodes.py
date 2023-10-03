class SymbolTable():
    '''
    Serve como memória do compilador
    '''

    def __init__(self):
        self.symbol_table = {}

    def get(self, identifier):

        if identifier not in self.symbol_table:
            raise ValueError(
                f'ERRO EM SymbolTable: Variável {self.identifier} sem atribuição')

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

    value: None

    children: 2 (children[0] operação children[1])
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
        elif self.value == '||':
            return self.children[0].evaluate(symbol_table) or self.children[1].evaluate(symbol_table)
        elif self.value == '&&':
            return self.children[0].evaluate(symbol_table) and self.children[1].evaluate(symbol_table)
        elif self.value == '==':
            return self.children[0].evaluate(symbol_table) == self.children[1].evaluate(symbol_table)
        elif self.value == '>':
            return self.children[0].evaluate(symbol_table) > self.children[1].evaluate(symbol_table)
        elif self.value == '<':
            return self.children[0].evaluate(symbol_table) < self.children[1].evaluate(symbol_table)
        elif self.value == '^':
            return self.children[0].evaluate(symbol_table) ** self.children[1].evaluate(symbol_table)


class UnOp(Node):
    '''
    Unary Operation - podendo ser + ou -

    value: None

    children: 1 (qualquer tipo)
    '''

    def evaluate(self, symbol_table: SymbolTable):
        if self.value == '-':
            return -self.children[0].evaluate(symbol_table)
        elif self.value == '+':
            return self.children[0].evaluate(symbol_table)
        elif self.value == '!':
            return not self.children[0].evaluate(symbol_table)


class IntVal(Node):
    '''
    Integer Value - Representa um valor inteiro

    value: Int

    children: []
    '''

    def evaluate(self, symbol_table: SymbolTable):
        return self.value


class NoOp(Node):
    '''
    No Operation - Nó Dummy

    value: None

    children: []
    '''

    def evaluate(self, symbol_table: SymbolTable):
        return None


class Identifier(Node):
    '''
    Identificador - Variável à qual é atribuido um valor

    value: qualquer tipo

    children: []
    '''

    def evaluate(self, symbol_table: SymbolTable):
        return symbol_table.get(identifier=self.value)


class Print(Node):
    '''
    Print

    value: None

    children: 1
    '''

    def evaluate(self, symbol_table: SymbolTable):
        print(self.children[0].evaluate(symbol_table))


class Program(Node):
    '''
    Representa o programa como um todo. Deve ser chamado apenas
    uma vez pelo parser.

    value: None

    children: n (um por linha com instruções do programa)
    '''

    def evaluate(self, symbol_table: SymbolTable):
        for statement in self.children:
            statement.evaluate(symbol_table)

class Block(Node):
    '''
    Bloco de instruções (for, if)

    value: None

    children: n (um por linha com instruções do programa)
    '''

    def evaluate(self, symbol_table: SymbolTable):
        for child in self.children:
            child.evaluate(symbol_table)


class Assignment(Node):
    '''
    Representa variável

    value: None

    children: 2
     - children[0] -> identifier
     - children[1] -> ast
    '''

    def evaluate(self, symbol_table: SymbolTable):
        variable = self.children[0].value
        ast_result = self.children[1].evaluate(symbol_table)
        symbol_table.set(identifier=variable, value=ast_result)


class Scanln(Node):
    '''
    Input de variável no terminal

    value: None

    children: []
    '''
    def evaluate(self, symbol_table: SymbolTable):
        return int(input())

class If(Node):
    '''
    Condicional

    value: None

    children: 2 ou 3
     - children[0] -> condicional
     - children[1] -> bloco a ser executado se true
     - children[2] -> bloco a ser executado no else (opcional)
    '''

    def evaluate(self, symbol_table: SymbolTable):
        condition = self.children[0]
        true_block = self.children[1]
        if condition.evaluate(symbol_table):
            true_block.evaluate(symbol_table)
        elif len(self.children) == 3:
            else_block = self.children[2]
            else_block.evaluate(symbol_table)
    

class For(Node):
    '''
    Loop de for

    value: None

    children: 4
     - children[0] -> variável de iteração
     - children[1] -> condição
     - children[2] -> incremento
     - children[3] -> bloco
    '''

    def evaluate(self, symbol_table: SymbolTable):
        self.children[0].evaluate(symbol_table)
        while(self.children[1].evaluate(symbol_table)):
            self.children[3].evaluate(symbol_table)
            self.children[2].evaluate(symbol_table)
