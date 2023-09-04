'''
Roteiro 1 - Simple Calculator v1.0
'''

import typing
import sys
from enum import Enum, auto


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

    Métodos:
    __init__(source): Inicializa o tokenizer a partir de uma expressão
    select_next(): Devolve o próximo token da expressão, alterando a posição de análise
    '''

    OPERATORS = ['-', '+', '*', '/', '(', ')']

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
            self.position += 1
        elif self.source[self.position].isdigit():
            this_value = ''
            while self.position != len(self.source) and self.source[self.position].isdigit():
                this_value += self.source[self.position]
                self.position += 1
            self.next = Token(value=int(this_value), type=TokenType.INT)
        elif self.source[self.position].isspace():
            self.position += 1
            Parser.tokenizer.select_next()
        else:
            raise ValueError(
                f"Erro Tokenizer: Caractere {self.source[self.position]} não esperado na posição {self.position}")


class Parser:
    '''
    Classe estática que analisa a estrutura da expressão e realiza operações.

    Métodos:
     - parse_term(): Calcula o próximo termo (multiplicação e divisão)
     - parse_expression(): Calcula soma e subtração de um termo
     - run(code): Inicializa o tokenizer e inicia o cálculo
    '''
    tokenizer = None

    @staticmethod
    def parse_factor() -> int:
        if Parser.tokenizer.next.type == TokenType.INT:
            factor = Parser.tokenizer.next.value
            Parser.tokenizer.select_next()
            return factor
        elif Parser.tokenizer.next.type == TokenType.MINUS:
            Parser.tokenizer.select_next()
            factor = Parser.parse_factor()
            return -factor
        elif Parser.tokenizer.next.type == TokenType.PLUS:
            Parser.tokenizer.select_next()
            factor = Parser.parse_factor()
            return +factor
        elif Parser.tokenizer.next.value == '(':
            Parser.tokenizer.select_next()
            expression = Parser.parse_expression()
            if Parser.tokenizer.next.value == ')':
                Parser.tokenizer.select_next()
                return expression
            else:
                raise ValueError(
                    f'Problema de fechamento de aspas em {Parser.tokenizer.position}')
        else:
            raise ValueError(
                f'Caractere {Parser.tokenizer.next.value} não esperado na posição {Parser.tokenizer.position}')

    @staticmethod
    def parse_term() -> int:
        '''
        Consome tokens calculando termo de multiplicação/divisão
        '''
        
        factor = Parser.parse_factor()

        while Parser.tokenizer.next.value == '*' or Parser.tokenizer.next.value == '/':
            if Parser.tokenizer.next.value == '*':
                Parser.tokenizer.select_next()
                factor *= Parser.parse_factor()
            elif Parser.tokenizer.next.value == '/':
                Parser.tokenizer.select_next()
                factor /= Parser.parse_factor()

        return factor

    @staticmethod
    def parse_expression():
        '''
        Consome tokens calculando termo de adição/subtração
        '''


        result = Parser.parse_term()
        while Parser.tokenizer.next.value == '-' or Parser.tokenizer.next.value == '+':
            if Parser.tokenizer.next.value == '-':
                Parser.tokenizer.select_next()
                result -= Parser.parse_term()
            elif Parser.tokenizer.next.value == '+':
                Parser.tokenizer.select_next()
                result += Parser.parse_term()

        return result

    @staticmethod
    def run(code: str) -> None:
        Parser.tokenizer = Tokenizer(source=code)
        Parser.tokenizer.select_next()
        result = Parser.parse_expression()
        if Parser.tokenizer.next.type != TokenType.EOF:
            raise ValueError("Não consumiu toda a expressão")

        print(result)

if __name__ == '__main__':
    Parser.run(sys.argv[1])
