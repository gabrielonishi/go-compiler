# Go Compiler

Projeto individual de um compilador para a disciplina Lógica da Computação, do 7° semestre de engenharia de computação. C

![git status](http://3.129.230.99/svg/gabrielonishi/go-compiler/)

### Adicionando String

Mudar Assign e  parse_statement

![mudanca.png](mudanca.png)

Passos para aplicação:

No Tokenizer:
 - se caractere for ":
    - criar variavel var
    - enquanto não for "
        - adicionar caractere em var
    - criar Token(value=var, type=STRING)

Em nodes:
 - Criar Nó StringVal:
    - value = var (string)
    - children = []
    - evaluate = return self.value

No parser:
 - No método parse_statement
    - Se Println
        - Se próximo valor for do tipo STRING
            - Criar Nó StringVal(value=next.value, [])
        - Caso contrário, tratar normalmente

 - Em assign
    - Depois de receber variável
    - Depois de =
    - Se próximo valor.type = STRING
        - Criar nó StringVal
        - Criar Assignment(value=None, children=[variable, StringVal])


