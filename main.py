import sys

import nodes, parse, write, pre_processment

if __name__ == '__main__':


    if(len(sys.argv) != 2):
        raise ValueError("É necessário enviar um arquivo de entrada")  
          
    filename = sys.argv[1].split('.')[0]
    in_filename = filename + '.go'
    out_filename = filename + '.asm'
    
    try:
        with open(file=in_filename, mode="r") as f:
            code = f.read()
    except Exception as e:
        raise ValueError("Arquivo enviado não existe")

    write.ProgramWriter.start(out_filename)

    clean_code = pre_processment.PrePro.filter(source=code)
    root = parse.Parser.run(clean_code)
    symbol_table = nodes.SymbolTable()
    root.evaluate(symbol_table=symbol_table)
    write.ProgramWriter.end()
