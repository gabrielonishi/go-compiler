# Go Compiler

Compiler built from scratch for [Go](https://en.wikipedia.org/wiki/Go_(programming_language)) using Python. Created for Insper Instituto de Ensino e Pesquisa course's on computational logic by [Raul Ikeda](https://www.insper.edu.br/pesquisa-e-conhecimento/docentes-pesquisadores/raul-ikeda-gomes-da-silva/).

### Syntatic Diagram

![Diagrama sintático](./syntactic_diagram.drawio.svg)

### EBNF (v2.1)

```
PROGRAM = { STATEMENT } ;
BLOCK = "{", "\n", { STATEMENT }, "}" ;
STATEMENT = ( λ | ASSIGN | PRINT | IF | FOR | VAR), "\n" ;
ASSIGN = IDENTIFIER, "=", BOOLEAN EXPRESSION ;
PRINT = "Println", "(", BOOLEAN EXPRESSION, ")" ;
IF = "if", BOOLEAN EXPRESSION, BLOCK, { "else", BLOCK } ;
FOR = "for", ASSIGN, ";", BOOLEAN EXPRESSION, ";", ASSIGN, BLOCK ;
VAR = "var", IDENTIFIER, ( "int" | "string" ), ( λ | "=", BOOLEAN EXPRESSION ) ;
BOOLEAN EXPRESSION = BOOLEAN TERM, { "||" BOOLEAN TERM } ;
BOOLEAN TERM = RELATIONAL EXPRESSION, { "&&", RELATIONAL EXPRESSION } ;
RELATIONAL EXPRESSION = EXPRESSION, { ("==" | ">" | "<"), EXPRESSION } ;
EXPRESSION = TERM, { ("+" | "-" | "." ), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = NUMBER | STRING | IDENTIFIER | (("+" | "-" | "!"), FACTOR) | "(", BOOLEAN EXPRESSION, ")" | SCAN ;
SCAN = "Scanln", "(", ")" ;
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
NUMBER = DIGIT, { DIGIT } ;
STRING = ( `"` | `'` ), { λ | LETTER | DIGIT }, ( `"` | `'` ) ;
LETTER = ( a | ... | z | A | ... | Z ) ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
```



