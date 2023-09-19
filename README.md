# Go Compiler

Projeto individual de um compilador para a disciplina Lógica da Computação, do 7° semestre de engenharia de computação.

![git status](http://3.129.230.99/svg/gabrielonishi/go-compiler/)

### Diagrama Sintático (v2.1)

![Diagrama sintático](./diagrama5.drawio.png)

### Para rodar o programa
```shell
python3.py main.py entrada.go
```

### EBNF (v2.1)

```
BLOCK = { STATEMENT };
STATEMENT = ( λ | ASSIGNMENT | PRINT), "\n" ;
ASSIGNMENT = IDENTIFIER, "=", EXPRESSION ;
PRINT = "Println", "(", EXPRESSION, ")" ;
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = (("+" | "-"), FACTOR) | NUMBER | "(", EXPRESSION, ")" | IDENTIFIER ;
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
NUMBER = DIGIT, { DIGIT } ;
LETTER = ( a | ... | z | A | ... | Z ) ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
```

### Operando com tags

Para criar uma nova tag:

```bash
git tag -a v0.1.1 -m "Mensagem sobre o release"
git push origin v0.1.1
```

Para selecionar a versão (note que não é um branch):
```bash
git checkout v0.1.1
```

