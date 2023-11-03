from enum import Enum, auto

class VarType(Enum):
    '''
    Armazena os tipos de dados possíveis até agora
    '''
    INT = auto()
    STRING = auto()

class SymbolTable():
    '''
    Serve como memória do compilador, associando idenitfier à
    variáveis na forma de tupla

    variável = (value, type, position), em que:
     - value: valor da variável
     - type: tipo da variável, segundo classe VarType
     - position: distância do reg EBP (base da pilha)

    self.symbol_table = 
    {
        identifier1 = (value1, type1, position1), 
        identifier2 = (value2, type2, position2),
        ...
    }
    '''

    position = 0

    def __init__(self) -> None:
        self.symbol_table = {}

    def get_by_identifier(self, identifier: str) -> tuple:
        '''
        Retorna uma tupla identificada por um identifier, se existir

        Argumentos:
         - identifier (str): identificador (Identifier.value, NÃO um nó Identifier)
        '''

        if identifier not in self.symbol_table:
            raise ValueError(
                f'ERRO EM SymbolTable: Variável {self.identifier} sem atribuição')

        return self.symbol_table[identifier]

    def set_by_identifier(self, identifier: str, value, var_type: VarType) -> None:
        '''
        Modifica valores da symbol table a partir de um identifier. Precisa
        receber valor e tipo da variável

        Retorna: posição da variável na pilha (para uso do Assembly)

        Argumentos:
         - identifier (str): identificador (Identifier.value, NÃO um nó Identifier)
         - value: valor a ser colocado na symbol table
         - var_type (VarType): tipo da variável
        '''
        if identifier not in self.symbol_table:
            raise ValueError("Tenta mudar variável antes de declará-la")
        last_value, last_type, position = self.symbol_table[identifier]

        if last_type != var_type:
            raise ValueError("Tenta mudar tipo de variável")

        self.symbol_table[identifier] = (value, var_type, position)

        return position

    def create_empty(self, identifier: str, declared_var_type: VarType) -> None:
        '''
        Instancia variável na symbol table quando um valor não é passado. Variável não 
        pode ter sido declarada antes no código.
        Ocorre quando temos algo no código .go como: `var x string`

        Argumentos:
         - identifier(str): identificador (Identifier.value, NÃO um nó Identifier)
         - declared_var_type(VarType): tipo da variável especificada
        '''
        if identifier in self.symbol_table:
            raise ValueError("Não se pode criar um mesmo identifier 2 vezes")
        
        position = SymbolTable.update_EBP_distance()

        self.symbol_table[identifier] = (None, declared_var_type, position)

    def create(self, identifier: str, variable: tuple, declared_var_type: VarType) -> None:
        '''
        Instancia variável na symbol table quando o valor é passado. Varipavel não
        pode ter sido declarada antes no código.
        Ocorre quando temos algo no código .go como: `var x string = 5`

        Retorna: posição da variável na pilha (para uso do Assembly)

        Argumentos:
         - identifier(str): identificador (Identifier.value, NÃO um nó Identifier)
         - variable(tuple): tupla representando a variável -> variable = (variable_value, variable_type)
         - declared_var_type(VarType): tipo da variável especificada
        '''

        variable_value, variable_type = variable
        position = SymbolTable.update_EBP_distance()

        if variable_type != declared_var_type:
            raise ValueError(
                "Tipo declarado da variável é diferente do tipo da variável")
        self.symbol_table[identifier] = (variable_value, variable_type, position)

        return position

    @staticmethod
    def update_position():
        # Valor fixo em 4 por que só usamos ariáveis de tamanho DWORD
        SymbolTable.position += 4
        return SymbolTable.position