import sys

import nodes
import tokens


class PrePro():
    '''
    Data pre-process: Faz o pré-processameto dos dados, removendo comentários
    '''

    @staticmethod
    def clean_comments(source: str) -> str:
        '''
        Remove comentários multiline e inline
        '''
        clean_raw = ''
        i = 0
        while i < len(source):
            if source[i:i+2] == '//':
                while source[i] != '\n':
                    i += 1
            elif source[i:i+2] == '/*':
                while source[i:i+2] != '*/':
                    i += 1
                # Tem que limpar * e /
                i += 2
            else:
                clean_raw += source[i]
                i += 1
        return clean_raw

    @staticmethod
    def clean_breaks(clean_raw: str) -> str:
        '''
        Remove quebras de linha sem código e garante '\n' no final das linhas de código
        '''
        lines = clean_raw.splitlines()
        clean_lines = [line.strip() for line in lines if line.strip()]
        break_ends = [line + '\n' for line in clean_lines]
        clean_code = ''.join(break_ends)
        return clean_code

    @staticmethod
    def filter(source: str) -> str:
        '''
        Filtra comentários e garante formatação
        '''

        clean_raw = PrePro.clean_comments(source)
        clean_code = PrePro.clean_breaks(clean_raw)
        return clean_code


class Parser:
    '''
    Classe estática que analisa a estrutura da expressão e realiza operações.
    Análise sintática do programa
    '''
    tokenizer = None
    
    @staticmethod
    def parse_program() -> nodes.Node:
        statements = list()
        while(Parser.tokenizer.next.type != tokens.TokenType.EOF):
            statement = Parser.parse_statement()
            statements.append(statement)
        return nodes.Program(value=None, children=statements)
            

    @staticmethod
    def parse_block() -> nodes.Node:
        if Parser.tokenizer.next.type == tokens.TokenType.OPEN_BRACKET:
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == tokens.TokenType.LINEFEED:
                Parser.tokenizer.select_next()
                block = nodes.Block(value=None, children=[])
                statements = list()
                while (Parser.tokenizer.next.type != tokens.TokenType.CLOSE_BRACKET):
                    statement = Parser.parse_statement()
                    statements.append(statement)
                block = nodes.Block(value=None, children=statements)
                
                if Parser.tokenizer.next.type == tokens.TokenType.CLOSE_BRACKET:
                    Parser.tokenizer.select_next()
                    return block
                else:
                    raise ValueError("ERRO EM Parser.parse_block(): Não fechou bloco com '}'")
            else:
                raise ValueError("ERRO EM Parser.parse_block(): É necessário um linebreak depois de '{'")
        else:
            raise ValueError("ERRO EM Parser.parse_block(): É necessário começar um novo bloco com '{'")

    @staticmethod
    def parse_statement() -> nodes.Node:

        if Parser.tokenizer.next.type == tokens.TokenType.PRINT:
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == tokens.TokenType.OPEN_PARENTHESIS:
                Parser.tokenizer.select_next()
                expression = Parser.parse_bool_expression()
                if Parser.tokenizer.next.type == tokens.TokenType.CLOSE_PARENTHESIS:
                    Parser.tokenizer.select_next()
                else:
                    raise ValueError(
                        "ERRO EM parse_statement(): Não fechou parênteses para print")
            else:
                raise ValueError(
                    "ERRO EM parse_statement(): Não abriu parênteses para print")
            statement = nodes.Print(value=None, children=[expression])
        
        elif(Parser.tokenizer.next.type == tokens.TokenType.IF):
            Parser.tokenizer.select_next()
            condition = Parser.parse_bool_expression()
            if_block = Parser.parse_block()
            if Parser.tokenizer.next.type == tokens.TokenType.ELSE:
                Parser.tokenizer.select_next()
                else_block = Parser.parse_block()
                statement = nodes.If(value=None, children=[condition, if_block, else_block])
            else:
                statement = nodes.If(value=None, children=[condition, if_block])
            
        elif(Parser.tokenizer.next.type == tokens.TokenType.FOR):
            Parser.tokenizer.select_next()
            iteration_variable = Parser.assign()
            if Parser.tokenizer.next.type != tokens.TokenType.COLON:
                raise ValueError("Esperava-se ';' após inicialização de variável do loop for")
            Parser.tokenizer.select_next()
            condition = Parser.parse_bool_expression()
            if Parser.tokenizer.next.type != tokens.TokenType.COLON:
                raise ValueError("Esperava-se ';' após condição do loop for")
            Parser.tokenizer.select_next()
            increment = Parser.assign()
            for_loop = Parser.parse_block()
            statement = nodes.For(value=None, children=[iteration_variable, condition, increment, for_loop])
        else:
            statement = Parser.assign()
 
        if Parser.tokenizer.next.type == tokens.TokenType.LINEFEED:
            Parser.tokenizer.select_next()
        else:
            raise ValueError(
                f'ERRO EM parse_statement(): Valor {Parser.tokenizer.next.value} não esperado na posição {Parser.tokenizer.position}'
            )
        return statement

    @staticmethod
    def parse_bool_expression() -> nodes.Node:
        bool_expression = Parser.parse_bool_term()

        while Parser.tokenizer.next.type == tokens.TokenType.OR:
            Parser.tokenizer.select_next()
            other_bool_term = Parser.parse_relation_expression()
            bool_expression = nodes.BinOp(value='||', children=[bool_expression, other_bool_term])
        
        return bool_expression

    @staticmethod
    def parse_bool_term() -> nodes.Node:
        bool_term = Parser.parse_relation_expression()
        while Parser.tokenizer.next.type == tokens.TokenType.AND:
            Parser.tokenizer.select_next()
            other_relation_expression = Parser.parse_relation_expression()
            bool_term = nodes.BinOp(value='&&', children=[bool_term, other_relation_expression])
        return bool_term

    @staticmethod
    def parse_relation_expression() -> nodes.Node:
        relation_expression = Parser.parse_expression()
        
        POSSIBLE_OPERATIONS = [tokens.TokenType.EQUALITY, tokens.TokenType.GREATERTHAN, tokens.TokenType.LESSERTHAN]
        while Parser.tokenizer.next.type in POSSIBLE_OPERATIONS:
            if Parser.tokenizer.next.type == tokens.TokenType.EQUALITY:
                Parser.tokenizer.select_next()
                other_expression = Parser.parse_expression()
                relation_expression = nodes.BinOp(value='==', children=[relation_expression, other_expression])
            elif Parser.tokenizer.next.type == tokens.TokenType.GREATERTHAN:
                Parser.tokenizer.select_next()
                other_expression = Parser.parse_expression()
                relation_expression = nodes.BinOp(value='>', children=[relation_expression, other_expression])
            elif Parser.tokenizer.next.type == tokens.TokenType.LESSERTHAN:
                Parser.tokenizer.select_next()
                other_expression = Parser.parse_expression()
                relation_expression = nodes.BinOp(value='<', children=[relation_expression, other_expression])
        return relation_expression

    @staticmethod
    def parse_expression():
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
        elif Parser.tokenizer.next.type == tokens.TokenType.NOT:
            Parser.tokenizer.select_next()
            factor = Parser.parse_factor()
            node = nodes.UnOp('!', children=[factor])
            return node
        elif Parser.tokenizer.next.type == tokens.TokenType.OPEN_PARENTHESIS:
            Parser.tokenizer.select_next()
            expression = Parser.parse_bool_expression()
            if Parser.tokenizer.next.type == tokens.TokenType.CLOSE_PARENTHESIS:
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
        elif Parser.tokenizer.next.type == tokens.TokenType.SCANLN:
            Parser.tokenizer.select_next()
            if(Parser.tokenizer.next.type != tokens.TokenType.OPEN_PARENTHESIS):
                raise ValueError('ERRO EM Parser.parse_factor: Não abriu parênteses depois de Scanln')
            Parser.tokenizer.select_next()
            if(Parser.tokenizer.next.type != tokens.TokenType.CLOSE_PARENTHESIS):
                raise ValueError('ERRO EM Parser.parse_factor: Não fechou parênteses após Scanln')
            Parser.tokenizer.select_next()
            node = nodes.Scanln(value=None, children=[])
            return node
            
    
    @staticmethod
    def assign() -> nodes.Node:
        if Parser.tokenizer.next.type == tokens.TokenType.IDENTIFIER:
            variable = Parser.tokenizer.next.value
            identifier = nodes.Identifier(value=variable, children=[])
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == tokens.TokenType.ATTRIBUTE:
                Parser.tokenizer.select_next()
                bool_expression = Parser.parse_bool_expression()
                return nodes.Assignment(value=None, children=[identifier, bool_expression])
            else:
                raise ValueError('ERRO EM Parser.assign(): Não passou um operador "="')
        else:
            raise ValueError('ERRO EM Parser.assign(): Próximo token deveria ser um identifier, mas não é')
        
    @staticmethod
    def run(code: str) -> nodes.Node:
        '''
        Monta a árvore binária (Abstract Syntax Tree)
        '''
        Parser.tokenizer = tokens.Tokenizer(source=code)
        Parser.tokenizer.select_next()
        ast = Parser.parse_program()
        if Parser.tokenizer.next.type != tokens.TokenType.EOF:
            raise ValueError("Não consumiu toda a expressão")
        return ast


if __name__ == '__main__':
    with open(file=sys.argv[1], mode="r") as file:
        code = file.read()
    clean_code = PrePro.filter(source=code)
    # Parser.tokenizer = tokens.Tokenizer(clean_code)
    # Parser.tokenizer.select_next()
    # print(Parser.tokenizer.next.value, Parser.tokenizer.next.type)
    # Parser.tokenizer.select_next()
    # print(Parser.tokenizer.next.value, Parser.tokenizer.next.type)
    # Parser.tokenizer.select_next()
    # print(Parser.tokenizer.next.value, Parser.tokenizer.next.type)
    # Parser.tokenizer.select_next()
    # print(Parser.tokenizer.next.value, Parser.tokenizer.next.type)
    # Parser.tokenizer.select_next()
    # print(Parser.tokenizer.next.value, Parser.tokenizer.next.type)
    # Parser.tokenizer.select_next()
    # print(Parser.tokenizer.next.value, Parser.tokenizer.next.type)
    root = Parser.run(clean_code)
    symbol_table = nodes.SymbolTable()
    root.evaluate(symbol_table=symbol_table)
