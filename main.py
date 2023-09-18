import typing
import sys
from enum import Enum, auto
from nodes import Node, IntVal, NoOp, UnOp, BinOp


class PrePro():
    '''
    Data pre-process: Faz o pré-processameto dos dados, removendo comentários
    '''

    @staticmethod
    def filter(source: str):
        clean_code = ''
        i = 0
        while i < len(source):
            if source[i:i+2] == '//':
                while i < len(source) and source[i] != '\n':
                    i += 1
            elif source[i:i+2] == '/*':
                # espera dar source[i] == '*' and source[i+1] == '/'
                while i < len(source) and source[i:i+1] == '*/':
                    i += 1
            elif source[i] != '\n':
                clean_code += source[i]
            i += 1
        return clean_code


class TokenType(Enum):
    '''
    Classe para armazenar o tipo de token como uma variável
    '''
    EOF = auto()
    INT = auto()
    PLUS = auto()
    MINUS = auto()
    MULT = auto()
    DIV = auto()
    BRACKET = auto()
    LINEFEED = auto()
    ATTRIBUTE = auto()
    PRINT = auto()
    IDENTIFIER = auto()



class Token:
    '''
    Encapsula informações definidoras de um token
    '''

    def __init__(self, value: typing.Union[int, str], type: TokenType) -> None:
        self.value = value
        self.type = type


class Tokenizer:
    '''
    Transforma uma sequência de caracteres em tokens
    Análise léxica do programa

    Métodos:
    __init__(source): Inicializa o tokenizer a partir de uma expressão
    select_next(): Devolve o próximo token da expressão, alterando a posição de análise
    '''

    OPERATORS = ['-', '+', '*', '/', '(', ')']
    RESERVED_KEYWORDS = ['println']

    def __init__(self, source: str) -> None:
        self.source = source
        self.position = 0
        self.next = None

    def select_next(self) -> None:
        '''Lê o próximo token e atualiza o atributo next'''

        if len(self.source) == self.position:
            self.next = Token(value='"', type=TokenType.EOF)
        elif self.source[self.position] in Tokenizer.OPERATORS:
            if self.source[self.position] == '-':
                self.next = Token(value='-', type=TokenType.MINUS)
            elif self.source[self.position] == '+':
                self.next = Token(value='+', type=TokenType.PLUS)
            elif self.source[self.position] == '*':
                self.next = Token(value='*', type=TokenType.MULT)
            elif self.source[self.position] == '/':
                self.next = Token(value='/', type=TokenType.DIV)
            elif self.source[self.position] == '(':
                self.next = Token(value='(', type=TokenType.BRACKET)
            elif self.source[self.position] == ')':
                self.next = Token(value=')', type=TokenType.BRACKET)
            elif self.source[self.position] == '\n':
                self.next = Token(value='\n', type=TokenType.LINEFEED)
            elif self.source[self.position] == '=':
                self.next = Token(value='=', type=TokenType.ATTRIBUTE)
            self.position += 1
        elif self.source[self.position].isdigit():
            this_value = ''
            while self.position != len(self.source) and self.source[self.position].isdigit():
                this_value += self.source[self.position]
                self.position += 1
            self.next = Token(value=int(this_value), type=TokenType.INT)
        elif self.source[self.position].isalpha():
            this_identifier = ''
            while self.position != len(self.source) and (self.source[self.position].isalnum() or
                                                         self.source[self.position] == '_'):
                this_identifier += self.source[self.position]
                self.position += 1 
            if(this_identifier in Tokenizer.RESERVED_KEYWORDS):
                # Vai ter que mudar no futuro
                self.next = Token(value='print', type=TokenType.PRINT)
            else:
                self.next = Token(value=this_identifier, type=TokenType.IDENTIFIER)
        elif self.source[self.position].isspace():
            self.position += 1
            Parser.tokenizer.select_next()
        else:
            raise ValueError(
                f"TOKENIZER ERRO: Caractere {self.source[self.position]} não esperado na posição {self.position}")


class Parser:
    '''
    Classe estática que analisa a estrutura da expressão e realiza operações.
    Análise sintática do programa

    Métodos (em ordem de maior prioridade para menor):
     - parse_factor(): Calcula operações unárias + expressões entre aspas
     - parse_term(): Calcula o próximo termo (multiplicação e divisão)
     - parse_expression(): Calcula soma e subtração de um termo
     - run(code): Inicializa o tokenizer e inicia o cálculo
    '''
    tokenizer = None

    @staticmethod
    def parse_factor() -> Node:
        if Parser.tokenizer.next.type == TokenType.INT:
            factor = Parser.tokenizer.next.value
            Parser.tokenizer.select_next()
            node = IntVal(factor, [])
            return node
        elif Parser.tokenizer.next.type == TokenType.MINUS:
            Parser.tokenizer.select_next()
            factor = Parser.parse_factor()
            node = UnOp('-', [factor])
            return node
        elif Parser.tokenizer.next.type == TokenType.PLUS:
            Parser.tokenizer.select_next()
            factor = Parser.parse_factor()
            node = UnOp('+', [factor])
            return node
        elif Parser.tokenizer.next.value == '(':
            Parser.tokenizer.select_next()
            expression = Parser.parse_expression()
            if Parser.tokenizer.next.value == ')':
                Parser.tokenizer.select_next()
                return expression
            else:
                raise ValueError(
                    f'PARSE FACTOR ERROR: Problema de fechamento de aspas em {Parser.tokenizer.position}')

    @staticmethod
    def parse_term() -> Node:
        '''
        Consome tokens calculando termo de multiplicação/divisão
        '''

        factor = Parser.parse_factor()

        while Parser.tokenizer.next.value == '*' or Parser.tokenizer.next.value == '/':
            if Parser.tokenizer.next.value == '*':
                Parser.tokenizer.select_next()
                children = Parser.parse_factor()
                factor = BinOp(value='*', children=[factor, children])
            elif Parser.tokenizer.next.value == '/':
                Parser.tokenizer.select_next()
                children = Parser.parse_factor()
                factor = BinOp(value='/', children=[factor, children])

        return factor

    @staticmethod
    def parse_expression():
        '''
        Consome tokens calculando termo de adição/subtração
        '''

        term = Parser.parse_term()
        while Parser.tokenizer.next.value == '-' or Parser.tokenizer.next.value == '+':
            if Parser.tokenizer.next.value == '-':
                Parser.tokenizer.select_next()
                children = Parser.parse_term()
                term = BinOp(value='-', children=[term, children])
            elif Parser.tokenizer.next.value == '+':
                Parser.tokenizer.select_next()
                children = Parser.parse_term()
                term = BinOp(value='+', children=[term, children])

        return term

    @staticmethod
    def run(code: str) -> Node:
        '''
        Monta a árvore binária (Abstract Syntax Tree)
        '''
        Parser.tokenizer = Tokenizer(source=code)
        Parser.tokenizer.select_next()
        ast = Parser.parse_expression()
        if Parser.tokenizer.next.type != TokenType.EOF:
            raise ValueError("Não consumiu toda a expressão")
        return ast


if __name__ == '__main__':
    with open(file=sys.argv[1], mode="r") as file:
        code = file.read()
    clean_code = PrePro.filter(source=code)
    root = Parser.run(clean_code)
    print(root.evaluate())
