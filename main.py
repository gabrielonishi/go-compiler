import sys

import nodes, tokens, parse, write

if __name__ == '__main__':


    if(len(sys.argv) != 2):
        raise ValueError("É necessário enviar um arquivo de entrada")  
          
    filename = sys.argv[1].split('.')[0]
    in_filename = filename + '.go'
    out_filename = filename + '.asm'

    try:
        with open(file=in_filename, mode="r") as f:
            code = f.read()
    except FileNotFoundError:
        print("Arquivo enviado não existe")

    write.ProgramWriter.start(out_filename)

    clean_code = tokens.PrePro.filter(source=code)
    root = parse.Parser.run(clean_code)
    symbol_table = nodes.SymbolTable()
    root.evaluate(symbol_table=symbol_table)
    write.ProgramWriter.end()
