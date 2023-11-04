class PrePro():
    '''
    Data pre-process: Faz o pré-processameto dos dados, removendo comentários
    '''

    @staticmethod
    def clean_comments(source: str) -> str:
        '''
        Remove comentários multiline e inline
        '''
        clean_raw = ''
        i = 0
        while i < len(source):
            if source[i:i+2] == '//':
                while source[i] != '\n':
                    i += 1
                    if i == len(source):
                        break
            elif source[i:i+2] == '/*':
                while source[i:i+2] != '*/':
                    i += 1
                # Tem que limpar * e /
                i += 2
            else:
                clean_raw += source[i]
                i += 1
        return clean_raw

    @staticmethod
    def clean_breaks(clean_raw: str) -> str:
        '''
        Remove quebras de linha sem código e garante '\n' no final das linhas de código
        '''
        lines = clean_raw.splitlines()
        clean_lines = [line.strip() for line in lines if line.strip()]
        break_ends = [line + '\n' for line in clean_lines]
        clean_code = ''.join(break_ends)
        return clean_code

    @staticmethod
    def filter(source: str) -> str:
        '''
        Filtra comentários e garante formatação
        '''
        clean_raw = PrePro.clean_comments(source)
        clean_code = PrePro.clean_breaks(clean_raw)
        return clean_code