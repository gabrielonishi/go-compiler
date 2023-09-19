import sys

import nodes
import tokens


class PrePro():
    '''
    Data pre-process: Faz o pré-processameto dos dados, removendo comentários
    '''

    @staticmethod
    def filter(source: str):
        clean_code = ''
        i = 0
        while i < len(source):
            if source[i:i+2] == '//':
                while i < len(source) and source[i] != '\n':
                    i += 1
            elif source[i:i+2] == '/*':
                # espera dar source[i] == '*' and source[i+1] == '/'
                while i < len(source) and source[i:i+1] == '*/':
                    i += 1
            else:
                clean_code += source[i]
            i += 1
        return clean_code


class Parser:
    '''
    Classe estática que analisa a estrutura da expressão e realiza operações.
    Análise sintática do programa
    '''
    tokenizer = None

    @staticmethod
    def parse_block() -> nodes.Node:
        statements = list()
        while (Parser.tokenizer.next.type != tokens.TokenType.EOF):
            statement = Parser.parse_statement()
            statements.append(statement)
        return nodes.Block(value=None, children=statements)

    @staticmethod
    def parse_statement() -> nodes.Node:
        if Parser.tokenizer.next.type == tokens.TokenType.LINEFEED:
            statement = nodes.NoOp(value=None, children=[])
            Parser.tokenizer.select_next()
            return statement
        elif Parser.tokenizer.next.type == tokens.TokenType.IDENTIFIER:
            variable = Parser.tokenizer.next.value
            identifier = nodes.Identifier(value=variable, children=[])
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == tokens.TokenType.ATTRIBUTE:
                Parser.tokenizer.select_next()
                expression = Parser.parse_expression()
                statement = nodes.Assignment(
                    value=None, children=[identifier, expression])
                return statement
            else:
                raise ValueError(
                    f'ERRO EM Parser.parse_statement: Identifier {identifier} não seguido de = na posição {Parser.tokenizer.position}')
        elif Parser.tokenizer.next.type == tokens.TokenType.PRINT:
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.value == '(':
                Parser.tokenizer.select_next()
                expression = Parser.parse_expression()
                if Parser.tokenizer.next.value == ')':
                    Parser.tokenizer.select_next()
                else:
                    raise ValueError(
                        "ERRO EM parse_statement(): Não fechou parênteses para print")
            else:
                raise ValueError(
                    "ERRO EM parse_statement(): Não abriu parênteses para print")
            statement = nodes.Print(value=None, children=[expression])
            return (statement)
        else:
            raise ValueError(
                f'ERRO EM parse_statement(): Valor {Parser.tokenizer.next.value} não esperado na posição {Parser.tokenizer.position}')

    @staticmethod
    def parse_expression():
        '''
        Consome tokens calculando termo de adição/subtração
        '''

        term = Parser.parse_term()
        while Parser.tokenizer.next.value == '-' or Parser.tokenizer.next.value == '+':
            if Parser.tokenizer.next.value == '-':
                Parser.tokenizer.select_next()
                children = Parser.parse_term()
                term = nodes.BinOp(value='-', children=[term, children])
            elif Parser.tokenizer.next.value == '+':
                Parser.tokenizer.select_next()
                children = Parser.parse_term()
                term = nodes.BinOp(value='+', children=[term, children])

        return term

    @staticmethod
    def parse_term() -> nodes.Node:
        '''
        Consome tokens calculando termo de multiplicação/divisão
        '''

        factor = Parser.parse_factor()

        while Parser.tokenizer.next.value == '*' or Parser.tokenizer.next.value == '/':
            if Parser.tokenizer.next.value == '*':
                Parser.tokenizer.select_next()
                children = Parser.parse_factor()
                factor = nodes.BinOp(value='*', children=[factor, children])
            elif Parser.tokenizer.next.value == '/':
                Parser.tokenizer.select_next()
                children = Parser.parse_factor()
                factor = nodes.BinOp(value='/', children=[factor, children])

        return factor

    @staticmethod
    def parse_factor() -> nodes.Node:
        if Parser.tokenizer.next.type == tokens.TokenType.INT:
            factor = Parser.tokenizer.next.value
            Parser.tokenizer.select_next()
            node = nodes.IntVal(factor, [])
            return node
        elif Parser.tokenizer.next.type == tokens.TokenType.MINUS:
            Parser.tokenizer.select_next()
            factor = Parser.parse_factor()
            node = nodes.UnOp('-', [factor])
            return node
        elif Parser.tokenizer.next.type == tokens.TokenType.PLUS:
            Parser.tokenizer.select_next()
            factor = Parser.parse_factor()
            node = nodes.UnOp('+', [factor])
            return node
        elif Parser.tokenizer.next.value == '(':
            Parser.tokenizer.select_next()
            expression = Parser.parse_expression()
            if Parser.tokenizer.next.value == ')':
                Parser.tokenizer.select_next()
                return expression
            else:
                raise ValueError(
                    f'PARSE FACTOR ERROR: Problema de fechamento de aspas em {Parser.tokenizer.position}')
        elif Parser.tokenizer.next.type == tokens.TokenType.IDENTIFIER:
            variable = Parser.tokenizer.next.value
            Parser.tokenizer.select_next()
            factor = nodes.Identifier(value=variable, children=[])
            return factor

    @staticmethod
    def run(code: str) -> nodes.Node:
        '''
        Monta a árvore binária (Abstract Syntax Tree)
        '''
        Parser.tokenizer = tokens.Tokenizer(source=code)
        Parser.tokenizer.select_next()
        ast = Parser.parse_block()
        if Parser.tokenizer.next.type != tokens.TokenType.EOF:
            raise ValueError("Não consumiu toda a expressão")
        return ast


if __name__ == '__main__':
    with open(file=sys.argv[1], mode="r") as file:
        code = file.read()
    clean_code = PrePro.filter(source=code)
    Parser.tokenizer = tokens.Tokenizer(clean_code)
    root = Parser.run(clean_code)
    symbol_table = nodes.SymbolTable()
    root.evaluate(symbol_table=symbol_table)
