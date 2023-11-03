class ProgramWriter():
    '''
    Classe responsável por abrir, escrever e fechar o
    arquivo assembly
    '''
    
    program_name = None
    HEADER_DOC_NAME = "program_header.txt"
    FOOTER_DOC_NAME = "program_footer.txt"

    @staticmethod 
    def start(output_program_name:str = "program.asm"):
        ProgramWriter.program_name = output_program_name

        with open(ProgramWriter.HEADER_DOC_NAME, "r") as header_file:
            header_content = header_file.read()
        
        with open(ProgramWriter.program_name, "w") as program_file:
            program_file.write(header_content)

    @staticmethod
    def write_line(code:str):
        with open(ProgramWriter.program_name, "a") as file:
            file.write(code)
            file.write("\n")

    @staticmethod
    def end():
        with open(ProgramWriter.FOOTER_DOC_NAME, "r") as footer_file:
            footer_content = footer_file.read()

        with open(ProgramWriter.program_name, "a") as file:
            file.write("\n")
            file.write(footer_content)
        