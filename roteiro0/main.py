'''
ROTEIRO ZERO - Lógica da Computação

Recebe como argumento uma cadeia de somas e subtrações de números
inteiros de múltiplos dígitos. Ao final exibe o resultado da operação.
'''

import sys

alphabet = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ', '\n', '\t', '-', '+']
algarisms = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
blank_chars = [' ', '\n', '\t']
operators = ['-', '+']

def main(expression:str) -> int:
    alphabet_check(expression)
    tokens = tokenize(expression)
    syntax_check(tokens)
    result = operate(tokens)

    return result

def alphabet_check(expression:str)->None:
    '''
    Verifica se existe algum caractere não esperado
    '''
    for character in expression:
        if character not in alphabet:
            raise ValueError(f'Erro Léxico: Caractere {character} não esperado')
        
def tokenize(expression:str) -> str:
    '''
    Divide a expressão em tokens
    '''

    last_token = ''
    tokens = list()
    for character in expression:
        if character in operators:
            if len(last_token)>0:
                tokens.append(last_token)
                last_token=''
            tokens.append(character)
        elif character in algarisms:
            last_token += character
        else:
            if len(last_token)>0:
                tokens.append(last_token)
                last_token=''
    
    if len(last_token)>0:
        tokens.append(last_token)
        last_token=''

    # Exceção: primeiro número negativo
    if tokens[0] == '-' and tokens[1][0] in algarisms:
        tokens = [tokens[0] + tokens[1]] + tokens[2:]
    
    return tokens

def syntax_check(tokens:str) -> None:
    '''
    Verifica se a sintaxe faz sentido. Interrompe se:
     - Houver dois números consecutivos (ex: '1 + 1  2')
     - Houver dois operadores consecutivos (ex: '1 ++ 1')
     - Enunciado acabar com operador (ex: '1 + 1 -')
     - Enunciado não começar com um número (ex: +)
    '''
    last_token = tokens[0]

    for token in tokens[1:]:
        if last_token[-1] in algarisms and token[-1] in algarisms:
            raise ValueError('Erro de Sintaxe: Dois números consecutivos')
        elif last_token[-1] in operators and token[-1] in operators:
            raise ValueError('Erro de Sintaxe: Dois operadores consecutivos')
        last_token = token
    
    if last_token in operators:
        raise ValueError('Erro de Sintaxe: Último caractere não pode ser uma operação')

    if tokens[0] not in algarisms:
        raise ValueError('Erro de Sintaxe: Operação deve começar com um número')

def operate(tokens:str) -> int:
    result_pile = int(tokens[0])
    last_operator = ''
    for token in tokens:
        if token in operators:
            last_operator = token
        elif last_operator == '-':
            result_pile -= int(token)
            last_operator = ''
        elif last_operator == '+':
            result_pile += int(token)
            last_operator = ''
    return result_pile

if __name__ == '__main__':
    print(main(expression=sys.argv[1]))
    