import sys

expression = sys.argv[1]

alfabeto = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ', '-', '+']

# Análise Léxica

regular_expression = ''
for token in expression:
    if token not in alfabeto:
        print(f'ERRO: Caractere {token} não esperado')
        exit()
    if not token == ' ':
        regular_expression += token
    last_token = token
print(regular_expression)