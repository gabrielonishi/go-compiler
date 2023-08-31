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
    def __init__(self, value: typing.Union[int, str], type:TokenType) -> None:
        self.value = value
        self.type = type

class Tokenizer:
    '''
    Transforma uma sequência de caracteres em tokens
    '''

    OPERATORS = ['-', '+', '*', '/']
    
    def __init__(self, source:str) -> None:
        self.source = source
        self.position = 0
        self.next = None

    def select_next(self) -> None:
        '''Lê o próximo token e atualiza o atributo next'''

        if len(self.source) == self.position:
            self.next = Token(value='"', type=TokenType.EOF)
        elif self.source[self.position] in Tokenizer.OPERATORS:
            match self.source[self.position]:
                case '-':
                    self.next = Token(value='-', type=TokenType.MINUS)
                case '+':
                    self.next = Token(value='+', type=TokenType.PLUS)
                case '*':
                    self.next = Token(value='*', type=TokenType.MULT)
                case '/':
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
            raise ValueError(f"Caractere {self.source[self.position]} não esperado na posição {self.position}")

class Parser:
    '''
    Classe estática que analisa a estrutura da expressão e realiza operações.
    '''
    tokenizer = None

    @staticmethod
    def parse_term():
        '''
        Consome tokens calculando termo de multiplicação/divisão
        ''' 
        term = 0
        if Parser.tokenizer.next.type == TokenType.INT:
            term = Parser.tokenizer.next.value
            Parser.tokenizer.select_next()
            while(Parser.tokenizer.next.type == TokenType.DIV or Parser.tokenizer.next.type == TokenType.MULT):
                if Parser.tokenizer.next.value == '*':
                    Parser.tokenizer.select_next()
                    if Parser.tokenizer.next.type == TokenType.INT:
                        term *= Parser.tokenizer.next.value
                    else:
                        raise ValueError(f'Caractere {Parser.tokenizer.next.value} não esperado em position = {Parser.tokenizer.position}')
                if Parser.tokenizer.next.value == '/':
                    Parser.tokenizer.select_next()
                    if Parser.tokenizer.next.type == TokenType.INT:
                        term //= Parser.tokenizer.next.value
                    else:
                        raise ValueError(f'Caractere {Parser.tokenizer.next.value} não esperado em position = {Parser.tokenizer.position}')
                Parser.tokenizer.select_next()
            return term
        raise ValueError(f'Primeiro caractere {Parser.tokenizer.next.value} precisa ser do tipo INT, mas é do tipo {Parser.tokenizer.next.type}')

    @staticmethod
    def parse_expression():
        '''
        Consome tokens do Tokenizer e analisa se a sintaxe está aderente à gramática proposta
        '''
        result = 0

        while Parser.tokenizer.next.type != TokenType.EOF:
            result = Parser.parse_term()
            while Parser.tokenizer.next.value == '-' or Parser.tokenizer.next.value == '+':
                if Parser.tokenizer.next.value == '-':
                    Parser.tokenizer.select_next()
                    result -= Parser.parse_term()
                if Parser.tokenizer.next.value == '+':
                    Parser.tokenizer.select_next()
                    result += Parser.parse_term()
        return result
    
    @staticmethod
    def run(code:str):
        Parser.tokenizer = Tokenizer(source=code)
        Parser.tokenizer.select_next()
        result = Parser.parse_expression()
        return result
        # if Parser.tokenizer.next.type == TokenType.EOF:
        #     return result
        # else:
        #     raise ValueError('Fim não esperado')

if __name__ == '__main__':
    print(Parser.run(sys.argv[1]))