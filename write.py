class ProgramWriter():
    '''
    Classe responsável por abrir, escrever e fechar o
    arquivo assembly
    '''
    @staticmethod
    def write_program(code:str):
        with open("program.asm", "w") as file:
            file.write(code)
            