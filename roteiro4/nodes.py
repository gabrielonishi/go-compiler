'''
Abriga os nós de operação do 
'''


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

    def evaluate():
        pass


class BinOp(Node):
    '''
    Binary Operation - podendo ser +, -, *, /
    Contém 2 filhos
    '''

    def evaluate(self):
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

    def evaluate(self):
        if self.value == '-':
            return -self.children[0].evaluate()
        elif self.value == '+':
            return self.children[0].evaluate()


class IntVal(Node):
    '''
    Integer Value - Representa um valor inteiro
    Não contém filhos
    '''

    def evaluate(self):
        return self.value


class NoOp():
    '''
    No Operation - Nó Dummy
    Não contém filhos
    '''

    def evaluate(self):
        pass
