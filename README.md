# Go Compiler

Projeto individual de um compilador para a disciplina Lógica da Computação, do 7° semestre de engenharia de computação.

### Adicionando operação de adição ou subtração unitária no compilador

A operação de incrementa pode aparecer em duas situações
Para quando o 
 1. Modificar Tokenizer para quando identificar um '+' atualizar position e checar próximo caractere. Caso seja outro '+', atualizar position de novo e criar Token INC, caso contrário criar Token SUM (sem atualizar posição novamente)
 2. Modificar parse 
