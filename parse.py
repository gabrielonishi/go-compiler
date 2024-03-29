import nodes
import tokens


class Parser:
    '''
    Classe estática que analisa a estrutura da expressão e realiza operações.
    Análise sintática do programa
    '''
    tokenizer = None

    @staticmethod
    def parse_program() -> nodes.Node:
        statements = list()
        while (Parser.tokenizer.next.type != tokens.TokenType.EOF):
            statement = Parser.parse_statement()
            statements.append(statement)
        return nodes.Program(value=None, children=statements)

    @staticmethod
    def parse_block() -> nodes.Node:
        if Parser.tokenizer.next.value != "{":
            raise ValueError(
                "ERRO EM Parser.parse_block(): É necessário começar um novo bloco com '{'")
        Parser.tokenizer.select_next()
        if Parser.tokenizer.next.type != tokens.TokenType.LINEFEED:
            raise ValueError(
                "ERRO EM Parser.parse_block(): É necessário um linebreak depois de '{'")
        Parser.tokenizer.select_next()
        block = nodes.Block(value=None, children=[])
        statements = list()
        while Parser.tokenizer.next.value != "}":
            statement = Parser.parse_statement()
            statements.append(statement)
        block = nodes.Block(value=None, children=statements)
        if Parser.tokenizer.next.value != "}":
            raise ValueError(
                "ERRO EM Parser.parse_block(): Não fechou bloco com '}'")
        Parser.tokenizer.select_next()
        return block

    @staticmethod
    def parse_statement() -> nodes.Node:

        if Parser.tokenizer.next.type == tokens.TokenType.PRINT:
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.value != "(":
                raise ValueError(
                    "ERRO EM parse_statement(): Não abriu parênteses para print")
            Parser.tokenizer.select_next()
            expression = Parser.parse_bool_expression()
            if Parser.tokenizer.next.value != ")":
                raise ValueError(
                    "ERRO EM parse_statement(): Não fechou parênteses para print")
            Parser.tokenizer.select_next()
            statement = nodes.Print(value=None, children=[expression])

        elif (Parser.tokenizer.next.type == tokens.TokenType.IF):
            Parser.tokenizer.select_next()
            condition = Parser.parse_bool_expression()
            if_block = Parser.parse_block()
            if Parser.tokenizer.next.type == tokens.TokenType.ELSE:
                Parser.tokenizer.select_next()
                else_block = Parser.parse_block()
                statement = nodes.If(value=None, children=[
                                     condition, if_block, else_block])
            else:
                statement = nodes.If(value=None, children=[
                                     condition, if_block])

        elif (Parser.tokenizer.next.type == tokens.TokenType.FOR):
            Parser.tokenizer.select_next()
            iteration_variable = Parser.assign()
            if Parser.tokenizer.next.type != tokens.TokenType.SEMICOLON:
                raise ValueError(
                    "Esperava-se ';' após inicialização de variável do loop for")
            Parser.tokenizer.select_next()
            condition = Parser.parse_bool_expression()
            if Parser.tokenizer.next.type != tokens.TokenType.SEMICOLON:
                raise ValueError("Esperava-se ';' após condição do loop for")
            Parser.tokenizer.select_next()
            increment = Parser.assign()
            for_loop = Parser.parse_block()
            statement = nodes.For(value=None, children=[
                                  iteration_variable, condition, increment, for_loop])
        
        elif (Parser.tokenizer.next.type == tokens.TokenType.VAR_DECLARATION):
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type != tokens.TokenType.IDENTIFIER:
                raise ValueError("Erro em parse.parse_statement(): É necessário identifier depois de 'var'")
            identifier = Parser.tokenizer.next.value
            identifier_node = nodes.Identifier(value=identifier, children=[])
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type != tokens.TokenType.VAR_TYPE:
                raise ValueError("Erro em parse.parse_statement(): É necessário especificar tipo ao criar variável")
            var_type = Parser.tokenizer.next.value
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == tokens.TokenType.ATTRIBUTE:
                Parser.tokenizer.select_next()
                bool_expression = Parser.parse_bool_expression()
                statement = nodes.VarDec(value=var_type, children=[identifier_node, bool_expression])
            else:
                statement = nodes.VarDec(value=var_type, children=[identifier_node])
        else:
            statement = Parser.assign()
        if Parser.tokenizer.next.type == tokens.TokenType.LINEFEED:
            Parser.tokenizer.select_next()
        else:
            raise ValueError(
                f'ERRO EM parse_statement(): Valor {repr(Parser.tokenizer.next.value)} não esperado na posição {Parser.tokenizer.position}'
            )
        return statement

    @staticmethod
    def parse_bool_expression() -> nodes.Node:
        bool_expression = Parser.parse_bool_term()

        while Parser.tokenizer.next.value == "||":
            Parser.tokenizer.select_next()
            other_bool_term = Parser.parse_relation_expression()
            if other_bool_term is None:
                raise ValueError(
                    'ERRO EM parse_bool_expression: É preciso uma ou mais expressões para fazer uma comparação!')
            bool_expression = nodes.BinOp(
                value='||', children=[bool_expression, other_bool_term])
        return bool_expression

    @staticmethod
    def parse_bool_term() -> nodes.Node:
        bool_term = Parser.parse_relation_expression()
        while Parser.tokenizer.next.value == "&&":
            Parser.tokenizer.select_next()
            other_relation_expression = Parser.parse_relation_expression()
            if other_relation_expression is None:
                raise ValueError(
                    'ERRO EM parse_bool_expression: É preciso uma ou mais expressões para fazer uma comparação!')
            bool_term = nodes.BinOp(value='&&', children=[
                                    bool_term, other_relation_expression])
        return bool_term

    @staticmethod
    def parse_relation_expression() -> nodes.Node:
        expression = Parser.parse_expression()

        while Parser.tokenizer.next.type == tokens.TokenType.NUMERIC_COMPARISON:
            operation = Parser.tokenizer.next.value
            if operation == "==":
                Parser.tokenizer.select_next()
                other_expression = Parser.parse_expression()
                expression = nodes.BinOp(
                    value='==', children=[expression, other_expression])
            elif operation == ">":
                Parser.tokenizer.select_next()
                other_expression = Parser.parse_expression()
                expression = nodes.BinOp(
                    value='>', children=[expression, other_expression])
            elif operation == "<":
                Parser.tokenizer.select_next()
                other_expression = Parser.parse_expression()
                expression = nodes.BinOp(
                    value='<', children=[expression, other_expression])
        return expression

    @staticmethod
    def parse_expression():
        term = Parser.parse_term()
        while Parser.tokenizer.next.type == tokens.TokenType.FIRST_ORDER_OPERATIONS:
            operation = Parser.tokenizer.next.value
            if operation == '-':
                Parser.tokenizer.select_next()
                other_term = Parser.parse_term()
                term = nodes.BinOp(value='-', children=[term, other_term])
            elif operation == '+':
                Parser.tokenizer.select_next()
                other_term = Parser.parse_term()
                term = nodes.BinOp(value='+', children=[term, other_term])
            elif operation == '.':
                Parser.tokenizer.select_next()
                other_term = Parser.parse_term()
                term = nodes.BinOp(value='.', children=[term, other_term])
        return term

    @staticmethod
    def parse_term() -> nodes.Node:
        factor = Parser.parse_factor()
        while Parser.tokenizer.next.type == tokens.TokenType.SECOND_ORDER_OPERATIONS:
            operation = Parser.tokenizer.next.value 
            if operation == '*':
                Parser.tokenizer.select_next()
                other_factor = Parser.parse_factor()
                factor = nodes.BinOp(value='*', children=[factor, other_factor])
            elif operation == '/':
                Parser.tokenizer.select_next()
                other_factor = Parser.parse_factor()
                factor = nodes.BinOp(value='/', children=[factor, other_factor])
        return factor

    @staticmethod
    def parse_factor() -> nodes.Node:
        if Parser.tokenizer.next.type == tokens.TokenType.INT:
            factor = Parser.tokenizer.next.value
            Parser.tokenizer.select_next()
            node = nodes.IntVal(factor, [])
            return node
        elif Parser.tokenizer.next.type == tokens.TokenType.STRING:
            string = Parser.tokenizer.next.value
            Parser.tokenizer.select_next()
            node = nodes.StringVal(string, [])
            return node
        elif Parser.tokenizer.next.value == "-":
            Parser.tokenizer.select_next()
            factor = Parser.parse_factor()
            node = nodes.UnOp('-', [factor])
            return node
        elif Parser.tokenizer.next.value == "+":
            Parser.tokenizer.select_next()
            factor = Parser.parse_factor()
            node = nodes.UnOp('+', [factor])
            return node
        elif Parser.tokenizer.next.type == tokens.TokenType.NOT:
            Parser.tokenizer.select_next()
            factor = Parser.parse_factor()
            node = nodes.UnOp('!', children=[factor])
            return node
        elif Parser.tokenizer.next.value == "(":
            Parser.tokenizer.select_next()
            expression = Parser.parse_bool_expression()
            if Parser.tokenizer.next.value == ")":
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
            if Parser.tokenizer.next.value != "(":
                raise ValueError(
                    'ERRO EM Parser.parse_factor: Não abriu parênteses depois de Scanln')
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.value != ")":
                raise ValueError(
                    'ERRO EM Parser.parse_factor: Não fechou parênteses após Scanln')
            Parser.tokenizer.select_next()
            node = nodes.Scanln(value=None, children=[])
            return node

    @staticmethod
    def assign() -> nodes.Node:
        if Parser.tokenizer.next.type != tokens.TokenType.IDENTIFIER:
            raise ValueError(
                'ERRO EM Parser.assign(): Próximo token deveria ser um identifier, mas não é')
        variable = Parser.tokenizer.next.value
        identifier_node = nodes.Identifier(value=variable, children=[])
        Parser.tokenizer.select_next()
        if Parser.tokenizer.next.type != tokens.TokenType.ATTRIBUTE:
            raise ValueError(
                'ERRO EM Parser.assign(): Não passou um operador "="')
        Parser.tokenizer.select_next()
        bool_expression = Parser.parse_bool_expression()
        return nodes.Assignment(value=None, children=[identifier_node, bool_expression])

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
