'''
Roteiro 1 - Simple Calculator v1.0
'''

import typing
import sys

class Token:
    def __init__(self, value: typing.Union[int, str], type:str) -> None:
        self.value = value
        self.type = type

class Tokenizer:
    def __init__(self, source:str) -> None:
        self.source = source
        self.position = 0
        self.next = None

    def selectNext(self) -> None:
        '''Lê o próximo token e atualiza o atributo next'''

        alphabet = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ', '\n', '\t', '-', '+']
        algarisms = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        
        next_is_blank = True
        while next_is_blank:
            next_is_blank = False
            if len(self.source) == self.position:
                self.next = Token(value='"', type='EOF')
            elif self.source[self.position] in alphabet:
                if self.source[self.position] == '-':
                    self.next = Token(value='-', type='MINUS')
                    self.position += 1
                elif self.source[self.position] == '+':
                    self.next = Token(value='+', type='PLUS')
                    self.position += 1
                elif self.source[self.position] in algarisms:
                    this_value = ""
                    while self.position != len(self.source) and self.source[self.position] in algarisms:
                        this_value += self.source[self.position]
                        self.position += 1
                    self.next = Token(value=int(this_value), type='INT')
                else: 
                    # É um caractere em branco
                    self.position += 1
                    next_is_blank = True
            else:
                raise ValueError(f'Caractere não esperado na posição {self.position}')

class Parser:
    tokenizer = None

    @staticmethod
    def parseExpression():
        '''
        Consome tokens do Tokenizer e analisa se a sintaxe está aderente à gramática proposta
        '''
        result = 0
        if Parser.tokenizer.next.type == 'INT':
            result = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            while(Parser.tokenizer.next.type == 'MINUS' or Parser.tokenizer.next.type == 'PLUS'):
                if Parser.tokenizer.next.value == '+':
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == 'INT':
                        result += Parser.tokenizer.next.value
                    else:
                        raise ValueError(f'Caractere {Parser.tokenizer.next.value} não esperado em position = {Parser.tokenizer.position}')
                if Parser.tokenizer.next.value == '-':
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == 'INT':
                        result -= Parser.tokenizer.next.value
                    else:
                        raise ValueError(f'Caractere {Parser.tokenizer.next.value} não esperado em position = {Parser.tokenizer.position}')
                Parser.tokenizer.selectNext()
            return result
        raise ValueError(f'Primeiro caractere {Parser.tokenizer.next.value} precisa ser do tipo INT, mas é do tipo {Parser.tokenizer.next.type}')
    
    @staticmethod
    def run(code:str):
        Parser.tokenizer = Tokenizer(code)
        Parser.tokenizer.selectNext()
        result = Parser.parseExpression()
        if Parser.tokenizer.next.type == 'EOF':
            return result
        else:
            raise ValueError('Fim não esperado')
        # if Parser.tokenizer.next.type == 'EOF':
        #     return Parser.parseExpression()
        # else:
        #     raise ValueError('Fim não esperado')

if __name__ == '__main__':
    print(Parser.run(sys.argv[1]))