import sys

import nodes, tokens, parse, write

if __name__ == '__main__':


    if(len(sys.argv) != 3):
        raise ValueError("É necessário enviar um arquivo de entrada e o nome do arquivo de saída")  
          
    file = sys.argv[1]
    output_program_name = sys.argv[2]

    with open(file=file, mode="r") as f:
        code = f.read()

    write.ProgramWriter.start(output_program_name)

    clean_code = tokens.PrePro.filter(source=code)
    root = parse.Parser.run(clean_code)
    symbol_table = nodes.SymbolTable()
    root.evaluate(symbol_table=symbol_table)
    write.ProgramWriter.end()
