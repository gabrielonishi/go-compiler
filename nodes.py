from tables import SymbolTable, FuncTable, VarType


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

    def evaluate(self, symbol_table: SymbolTable) -> tuple:
        pass


class BinOp(Node):
    '''
    Binary Operation - podendo ser +, -, *, /

    value: None

    children: 2 
     - children[0]: termo 1
     - children[1]: termo 2
    '''

    def evaluate(self, symbol_table: SymbolTable) -> tuple:

        left_term_value, left_term_type = self.children[0].evaluate(
            symbol_table)
        right_term_value, right_term_type = self.children[1].evaluate(
            symbol_table)

        ARITHIMETIC_OPERATORS = ['+', '-', '*', '/']
        BOOLEAN_OPERATORS = ['||', '&&']
        RELATIONAL_OPERATORS = ['>', '<', '==']

        if self.value in ARITHIMETIC_OPERATORS:
            if (left_term_type == VarType.STRING or right_term_type == VarType.STRING):
                raise ValueError(
                    "Erro em nodes.BinOp.evaluate(): Não é possível fazer operações aritiméticas envolvendo strings")
            return_type = VarType.INT
            if self.value == '+':
                return_value = left_term_value + right_term_value
                return (return_value, return_type)
            elif self.value == '-':
                return_value = left_term_value - right_term_value
                return (return_value, return_type)
            elif self.value == '*':
                return_value = left_term_value * right_term_value
                return (return_value, return_type)
            elif self.value == '/':
                return_value = left_term_value // right_term_value
                return (return_value, return_type)

        elif self.value in BOOLEAN_OPERATORS:
            if (left_term_type != right_term_type):
                raise ValueError(
                    "Erro em nodes.BinOp.evaluate(): Não é possível fazer operações booleanas com tipos diferentes")

            return_type = VarType.INT
            if self.value == '||':
                return_value = left_term_value or right_term_value
                return (int(return_value), return_type)
            elif self.value == '&&':
                return_value = left_term_value and right_term_value
                return (int(return_value), return_type)

        elif self.value in RELATIONAL_OPERATORS:
            if (left_term_type != right_term_type):
                raise ValueError(
                    "Erro em nodes.BinOp.evaluate(): Não é possível fazer operações booleanas com tipos diferentes")
            return_type = VarType.INT
            if self.value == '==':
                return_value = left_term_value == right_term_value
                return (int(return_value), return_type)
            elif self.value == '>':
                return_value = left_term_value > right_term_value
                return (int(return_value), return_type)
            elif self.value == '<':
                return_value = left_term_value < right_term_value
                return (int(return_value), return_type)

        elif self.value == '.':
            return_type = VarType.STRING
            return_value = str(left_term_value) + str(right_term_value)
            return (return_value, return_type)
        else:
            raise ValueError("Erro fudeu")


class UnOp(Node):
    '''
    Unary Operation - podendo ser + ou -

    value: None

    children: 1 (qualquer tipo)
    '''

    def evaluate(self, symbol_table: SymbolTable) -> tuple:

        term_value, term_type = self.children[0].evaluate(symbol_table)

        if self.value == '-':
            return_value = (-term_value, term_type)
            return return_value
        elif self.value == '+':
            return_value = (term_value, term_type)
            return return_value
        elif self.value == '!':
            return_value = (not term_value, term_type)
            return return_value


class NoOp(Node):
    '''
    No Operation - Nó Dummy

    value: None

    children: []
    '''

    def evaluate(self, symbol_table: SymbolTable) -> None:
        return None


class IntVal(Node):
    '''
    Integer Value - Representa um valor inteiro

    value: Int

    children: []
    '''

    def evaluate(self, symbol_table: SymbolTable) -> tuple:
        return (self.value, VarType.INT)


class StringVal(Node):
    '''
    String Value - Representa uma string

    value: String

    children: []
    '''

    def evaluate(self, symbol_table: SymbolTable) -> tuple:
        return (self.value, VarType.STRING)


class Identifier(Node):
    '''
    Identificador - Variável à qual é atribuido um valor

    value: qualquer tipo

    children: []
    '''

    def evaluate(self, symbol_table: SymbolTable) -> tuple:
        return symbol_table.get(identifier=self.value)


class Print(Node):
    '''
    Print

    value: None

    children: 1
    '''

    def evaluate(self, symbol_table: SymbolTable) -> None:
        result_value, _ = self.children[0].evaluate(symbol_table)
        print(result_value)


class Program(Node):
    '''
    Representa o programa como um todo. Deve ser chamado apenas
    uma vez pelo parser.

    value: None

    children: n (um por linha com instruções do programa)
    '''

    def evaluate(self, symbol_table: SymbolTable) -> tuple:
        for statement in self.children:
            statement.evaluate(symbol_table)


class Block(Node):
    '''
    Bloco de instruções (for, if)

    value: None

    children: n (um por linha com instruções do programa)
    '''

    def evaluate(self, symbol_table: SymbolTable) -> tuple:
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

    def evaluate(self, symbol_table: SymbolTable) -> tuple:
        variable = self.children[0].value
        ast_result_value, ast_type_value = self.children[1].evaluate(
            symbol_table)
        symbol_table.set(identifier=variable,
                         value=ast_result_value, var_type=ast_type_value)


class VarDec(Node):
    '''
    Variable Declaration - Adiciona uma variável à SymbolTable

    value: Tipo da variável

    children: Pode ter 1 ou 2
     - children[0] -> Nó Identifier
     - children[1] -> boolExpression
    '''

    def evaluate(self, symbol_table: SymbolTable) -> None:
        identifier_node = self.children[0]
        identifier = identifier_node.value
        declared_var_type = self.value
        if len(self.children) == 1:
            SymbolTable.create_empty(
                symbol_table, identifier=identifier, declared_var_type=declared_var_type)
        elif len(self.children) == 2:
            variable = self.children[1].evaluate(symbol_table)
            SymbolTable.create(symbol_table, identifier=identifier, variable=variable,
                               declared_var_type=declared_var_type)


class FuncDec(Node):
    '''
    Representa componentes de uma função

    value: None
    children: n + 2 filhos
     - children[0]: VarDec do nome da função
     - children[1]: Block
     - children[n]: VarDec do argumento

    evaluate: Instancia função na func_table
    '''

    def evaluate(self, symbol_table: SymbolTable) -> None:
        function_name_var_dec_node = self.children[0]
        function_name_identifier_node = function_name_var_dec_node.children[0]
        function_name = function_name_identifier_node.value

        FuncTable.set(function_name=function_name, func_dec_node=self)


class Return(Node):
    '''
    Retorna dentro de uma função

    value: None
    children: Não se sabe 
    '''

    def evaluate(self, symbol_table: SymbolTable) -> Node:
        result_node = self.children[0]
        return result_node.evaluate(symbol_table)


class Scanln(Node):
    '''
    Input de variável no terminal

    value: None

    children: []
    '''

    def evaluate(self, symbol_table: SymbolTable) -> tuple:
        return (int(input()), VarType.INT)


class If(Node):
    '''
    Condicional

    value: None

    children: 2 ou 3
     - children[0] -> condicional
     - children[1] -> bloco a ser executado se true
     - children[2] -> bloco a ser executado no else (opcional)
    '''

    def evaluate(self, symbol_table: SymbolTable) -> tuple:
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

    def evaluate(self, symbol_table: SymbolTable) -> tuple:
        # Atualiza symbol table
        self.children[0].evaluate(symbol_table)
        while (self.children[1].evaluate(symbol_table) == (1, VarType.INT)):
            # print(self.children[3].evaluate(symbol_table))
            self.children[3].evaluate(symbol_table)
            self.children[2].evaluate(symbol_table)
