class ProgramWriter():
    '''
    Classe responsável por abrir, escrever e fechar o
    arquivo assembly
    '''
    
    PROGRAM_NAME = "program.txt"
    is_new_file = True

    @staticmethod
    def erase_document():
        ProgramWriter.is_new_file = False
        with open(ProgramWriter.PROGRAM_NAME, "w"):
            pass

    @staticmethod
    def write_line(code:str):
        if(ProgramWriter.is_new_file):
            ProgramWriter.erase_document()

        with open(ProgramWriter.PROGRAM_NAME, "a") as file:
            file.write(code)
            file.write("\n")