'''
ROTEIRO ZERO - Lógica da Computação

Recebe como argumento uma cadeia de somas e subtrações de números
inteiros de múltiplos dígitos. Ao final exibe o resultado da operação.
'''

import sys


alphabet = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ', '    ', '\n', '\t', '-', '+']
operators = ['-', '+']
algarisms = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
blank_chars = ['\n', '\t', ' ']

def main(expression):

    if len(sys.argv) != 2:
        raise ValueError('Entrada não esperada')
    
    tokens = lexical(expression)
    syntax(tokens)
    result = operation(tokens)

    return(result)

def lexical(expression:str) -> str:
    tokens = list()
    last_token = ''

    for character in expression:
        if character not in alphabet:
            raise ValueError(f'Erro Léxico: Caractere não esperado')
        if character not in blank_chars:
            if character not in operators:
                last_token += character
            else:
                if len(last_token)>0:
                    tokens.append(last_token)
                tokens.append(character)
                last_token = ''

    if last_token[-1] in alphabet:
        tokens.append(last_token)
    
    # Exceção: primeiro número negativo
    if tokens[0] == '-' and tokens[1][0] in algarisms:
        tokens = [tokens[0] + tokens[1]] + tokens[2:]
    
    return tokens

# Análise sintática
def syntax(tokens):
    
    # Exceção: string vazia
    if len(tokens) == 0:
        raise ValueError('Erro: Entrada não esperada')
    
    # Exceção: última string não pode ser operador

    if tokens[-1] in operators:
        raise ValueError('Erro sintático: cálculo não pode acabar com um operador')

    last_token = tokens[0]

    for token in tokens[1:]:
        if (last_token[-1] in operators and token in operators) or (last_token in algarisms and token in algarisms):
            raise ValueError('Erro sintático: Dois operadores ou números seguidos')
        last_token = token

def operation(tokens):

    last_number = int(tokens[0])
    last_operator = ''

    for token in tokens[1:]:
        if token in operators:
            last_operator = token
        else:
            if last_operator == '-':
                last_number = last_number - int(token)
            elif last_operator == '+':
                last_number = last_number + int(token)

    return last_number

if __name__ == '__main__':
    result = main(expression=sys.argv[1])
    print(result)
