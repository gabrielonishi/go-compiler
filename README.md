# Simple Calculator

Projeto individual de um compilador para a disciplina Lógica da Computação, do 7° semestre de engenharia de computação.

![git status](http://3.129.230.99/svg/gabrielonishi/comp-log-compiler/)

### Diagrama Sintático (v2.0)

![Diagrama sintático](./diagrama-roteiro3.png)

### EBNF (v2.0)

```
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = ("+" | "-") FACTOR | "(" EXPRESSION ")" | NUMBER ;
NUMBER = DIGIT, {DIGIT} ;
DIGIT = 0 | 1 | ... | 9 ;
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

