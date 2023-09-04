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

    OPERATORS = ['-', '+', '*', '/']

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
                f"Caractere {self.source[self.position]} não esperado na posição {self.position}")


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
    def parse_term() -> int:
        '''
        Consome tokens calculando termo de multiplicação/divisão
        '''
        term = 0
        if Parser.tokenizer.next.type == TokenType.INT:
            term = Parser.tokenizer.next.value
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == TokenType.INT:
                raise ValueError('Erro de dois números consecutivos')
            while (Parser.tokenizer.next.type == TokenType.DIV or Parser.tokenizer.next.type == TokenType.MULT):
                if Parser.tokenizer.next.value == '*':
                    Parser.tokenizer.select_next()
                    if Parser.tokenizer.next.type == TokenType.INT:
                        term *= Parser.tokenizer.next.value
                    else:
                        raise ValueError(
                            f'Caractere {Parser.tokenizer.next.value} não esperado em position = {Parser.tokenizer.position}')
                if Parser.tokenizer.next.value == '/':
                    Parser.tokenizer.select_next()
                    if Parser.tokenizer.next.type == TokenType.INT:
                        term //= Parser.tokenizer.next.value
                    else:
                        raise ValueError(
                            f'Caractere {Parser.tokenizer.next.value} não esperado em position = {Parser.tokenizer.position}')
                Parser.tokenizer.select_next()
            return term
        raise ValueError(
            f'Primeiro caractere {Parser.tokenizer.next.value} precisa ser do tipo INT, mas é do tipo {Parser.tokenizer.next.type}')

    @staticmethod
    def parse_expression() -> int:
        '''
        Consome tokens calculando termo de adição/subtração
        '''
        result = 0

        while Parser.tokenizer.next.type != TokenType.EOF:
            result = Parser.parse_term()
            while Parser.tokenizer.next.value == '-' or Parser.tokenizer.next.value == '+':
                if Parser.tokenizer.next.value == '-':
                    Parser.tokenizer.select_next()
                    if Parser.tokenizer.next.type == TokenType.INT:
                        result -= Parser.parse_term()
                    else:
                        raise ValueError(
                            f'Caractere {Parser.tokenizer.next.value} não esperado em position = {Parser.tokenizer.position}')
                elif Parser.tokenizer.next.value == '+':
                    Parser.tokenizer.select_next()
                    if Parser.tokenizer.next.type == TokenType.INT:
                        result += Parser.parse_term()
                    else:
                        raise ValueError(
                            f'Caractere {Parser.tokenizer.next.value} não esperado em position = {Parser.tokenizer.position}')
        return result

    @staticmethod
    def run(code: str) -> int:
        Parser.tokenizer = Tokenizer(source=code)
        Parser.tokenizer.select_next()
        result = Parser.parse_expression()
        return result


if __name__ == '__main__':
    print(Parser.run(sys.argv[1]))
