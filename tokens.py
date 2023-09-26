import typing
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
    OPEN_PARENTHESIS = auto()
    CLOSE_PARENTHESIS = auto()
    OPEN_BRACKET = auto()
    CLOSE_BRACKET = auto()
    LINEFEED = auto()
    ATTRIBUTE = auto()
    PRINT = auto()
    IDENTIFIER = auto()
    GREATERTHAN = auto()
    LESSERTHAN = auto()
    NOT = auto()
    OR = auto()
    AND = auto()
    EQUALITY = auto()
    SCANLN = auto()
    IF = auto()
    FOR = auto()
    ELSE = auto()
    COLON = auto()

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
Println(x)en da expressão, alterando a posição de análise
    '''

    OPERATORS = ['-', '+', '*', '/', '(', ')', '=', '\n', '&', '|', '>', '<', '!', '{', '}', ';']
    RESERVED_KEYWORDS = ['Println', 'Scanln', 'if', 'else', 'for']

    def __init__(self, source: str) -> None:
        self.source = source
        self.position = 0
        self.next = None

    def select_next(self) -> None:
        '''Lê o próximo token e atualiza o atributo next'''
        if len(self.source) == self.position:
            self.next = Token(value='EOF', type=TokenType.EOF)
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
                self.next = Token(value='(', type=TokenType.OPEN_PARENTHESIS)
            elif self.source[self.position] == ')':
                self.next = Token(value=')', type=TokenType.CLOSE_PARENTHESIS)
            elif self.source[self.position] == '\n':
                self.next = Token(value='\n', type=TokenType.LINEFEED)
            elif self.source[self.position] == '>':
                self.next = Token(value='>', type=TokenType.GREATERTHAN)
            elif self.source[self.position] == '<':
                self.next = Token(value='<', type=TokenType.LESSERTHAN)
            elif self.source[self.position] == '!':
                self.next = Token(value='!', type=TokenType.NOT)
            elif self.source[self.position] == '{':
                self.next = Token(value='{', type=TokenType.OPEN_BRACKET)
            elif self.source[self.position] == '}':
                self.next = Token(value='}', type=TokenType.CLOSE_BRACKET)
            elif self.source[self.position] == ';':
                self.next = Token(value=';', type=TokenType.COLON)
            elif self.source[self.position] == '=':
                if self.source[self.position + 1] == '=':
                    self.next = Token(value='==', type=TokenType.EQUALITY)
                    self.position+=1
                else:
                    self.next = Token(value='=', type=TokenType.ATTRIBUTE)
            elif self.source[self.position] == '&':
                if self.source[self.position + 1] == '&':
                    self.next = Token(value='&&', type = TokenType.AND)
                    self.position+=1
                else:
                    raise ValueError("ERRO EM Tokenizer.select_next(): '&' não é um operador válido. Você quis dizer '&&'?")
            elif self.source[self.position] == '|':
                if self.source[self.position + 1] == '|':
                    self.next = Token(value='||', type = TokenType.OR)
                    self.position+=1
                else:
                    raise ValueError("ERRO EM Tokenizer.select_next(): '|' não é um operador válido. Você quis dizer '||'?")
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
            if (this_identifier in Tokenizer.RESERVED_KEYWORDS):
                if this_identifier == 'Println':
                    self.next = Token(value='Println', type=TokenType.PRINT)
                elif this_identifier == 'Scanln':
                    self.next = Token(value='Scanln', type=TokenType.SCANLN)
                elif this_identifier == 'if':
                    self.next = Token(value='if', type=TokenType.IF)
                elif this_identifier == 'for':
                    self.next = Token(value='for', type =TokenType.FOR)
                elif this_identifier == 'else':
                    self.next = Token(value='else', type=TokenType.ELSE)
            else:
                self.next = Token(value=this_identifier,
                                  type=TokenType.IDENTIFIER)
        elif self.source[self.position].isspace():
            self.position += 1
            self.select_next()
        else:
            raise ValueError(
                f"TOKENIZER ERRO: Caractere {self.source[self.position]} não esperado na posição {self.position}")
