import sys

import nodes, tokens, parse

if __name__ == '__main__':

    debug = False
    file = ''
    if debug:
        file = "entrada.go"
    else:
        if(len(sys.argv) == 1):
            raise ValueError("ERRO: É necessário mandar um arquivo com extensão .go para compilar!")        
        file = sys.argv[1]

    with open(file=file, mode="r") as f:
        code = f.read()

    clean_code = tokens.PrePro.filter(source=code)
    root = parse.Parser.run(clean_code)
    symbol_table = nodes.SymbolTable()
    root.evaluate(symbol_table=symbol_table)
