'''
ROTEIRO ZERO - Lógica da Computação

Recebe como argumento uma cadeia de somas e subtrações de números
inteiros de múltiplos dígitos. Ao final exibe o resultado da operação.
'''

import sys

expression = sys.argv[1]

alphabet = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ', '-', '+']
operators = ['-', '+']

# Análise Léxica

tokens = []

token = ''
for character in expression:
    if character not in alphabet:
        print(f'ERRO: Caractere {token} não esperado')
        exit()
    if not character == ' ':
        if not character in operators:
            token += character
        else:
            tokens.append(token)
            tokens.append(character)
            token = ''

tokens.append(token)
print(tokens)

# Análise Sintática

for token in 
