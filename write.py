class ProgramWriter():
    '''
    Classe responsável por abrir, escrever e fechar o
    arquivo assembly
    '''
    
    PROGRAM_NAME = "program.txt"
    is_new_file = True

    @staticmethod
    def write_program(code:str):
        if(ProgramWriter.is_new_file):
            ProgramWriter.is_new_file = False
            with open(ProgramWriter.PROGRAM_NAME, "w"):
                pass

        with open(ProgramWriter.PROGRAM_NAME, "a") as file:
            file.write(code)