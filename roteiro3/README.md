# Roteiro 3

### Objetivos do Roteiro
1. Implementar operadores unários.
2. Implementar parênteses.

### Tarefas do Roteiro:
1. Atualizar o Diagrama Sintático e a EBNF no GitHub.
2. Implementar as melhorias conforme o DS atualizado.
3. Prestar muita atenção nos lugares onde será necessário alterar.
4. Dica: posicionar no primeiro token logo no run(). Só chamar o selectNext() quando consumir um token

### Diagrama Sintático (v1.2)

![Diagrama sintático](./diagrama-roteiro2.png)

### EBNF

```
EXPRESSION = TERM, {("+" | "-" ), TERM} ;
TERM = NUMBER, {("*" | "/"), NUMBER} ;
NUMBER = DIGIT, {DIGIT} ;
DIGIT = 0 | 1 | ... | 9 ;
```

### Rodando o Programa

``` bash
python main.py '1+1'
```

**Base de Testes**:
```bash
>> (3 + 2) /5
>> +--++3
>> 3 - -2/4
>> 4/(1+1)*2
>> (2*2
```


