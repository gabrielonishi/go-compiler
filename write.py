class ProgramWriter():
    '''
    Classe responsável por abrir, escrever e fechar o
    arquivo assembly
    '''
    
    program_name = "program.txt"
    
    @staticmethod
    def set_program_name(new_program_name:str):
        ProgramWriter.program_name = new_program_name

    @staticmethod
    def erase_document():
        with open(ProgramWriter.program_name, "w"):
            pass

    @staticmethod
    def write_line(code:str):
        with open(ProgramWriter.program_name, "a") as file:
            file.write(code)
            file.write("\n")