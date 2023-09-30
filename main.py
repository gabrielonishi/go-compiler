import sys

import nodes, tokens, parse

if __name__ == '__main__':

    if(len(sys.argv) == 1):
        raise ValueError("ERRO: É necessário mandar um arquivo com extensão .go para compilar!")
    
    file = sys.argv[1]
    extension = file.split(".")[1]
    if extension != "go":
        raise ValueError("ERRO: O arquivo compilado deve ter extensão .go!")

    with open(file=file, mode="r") as f:
        code = f.read()

    clean_code = tokens.PrePro.filter(source=code)
    root = parse.Parser.run(clean_code)
    symbol_table = nodes.SymbolTable()
    root.evaluate(symbol_table=symbol_table)
