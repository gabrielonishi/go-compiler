import typing
from enum import Enum, auto

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
    def filter(source: str) -> str:
        '''
        Filtra comentários e garante formatação
        '''

        clean_code = PrePro.clean_comments(source)
        print(clean_code)
        return clean_code