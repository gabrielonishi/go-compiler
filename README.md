# Go Compiler

Projeto individual de um compilador para a disciplina Lógica da Computação, do 7° semestre de engenharia de computação. C

### Adicionando operação de potência no compilador

Passos para aplicação:
 1. Colocar caractere `'^'` no tokenizer
 2. Adicionar operação children[0] ** children[2] no evaluate do BinOp
 3. Modificar Parser: 
 - fazer com que parse_term() começe calculando um parse_power_term() 
 - fazer um parse_power_term() em que:     
    - calculamos próximo parse_factor()
    - loopamos enquanto for `'^'`, calculamos próximo factor e criamos nó BinOp com value = '^' e children = [factor1, factor2]
