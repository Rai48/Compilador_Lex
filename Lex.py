import re
import pandas as pd
import os


operators = {'=' : 'Simbolo_Atribuicao',
            '==' : 'Simbolo_Comparacao',
            '+' : 'Simbolo_Op_Adicao',
            '-' : 'Simbolo_Op_Subtracao',
            '/' : 'Simbolo_Op_Divisao',
            '*' : 'Simbolo_Op_Multiplicacao',
            '<' : 'Simbolo_Op_Menorque',
            '>' : 'Simbolo_Op_Maiorque',
            '%' : 'Simbolo_Op_Modulo' }
operators_key = operators.keys()

logical_operators = {'&' : 'Simbolo_Op_E',
                    '|' : 'Simbolo_Op_OU',
                    '~' : 'Simbolo_Op_Negacao',
                    '!' : 'Simbolo_Negacao' }
logical_operators_key = logical_operators.keys()

symbols = {
    '_' : 'Simbolo_Underscore',
    '{' : 'Simbolo_Chave_Abertura',
    '}' : 'Simbolo_Chave_Fecha',
    '[' : 'Simbolo_Colchete_Abertura',
    ']' : 'Simbolo_Colchete_Fecha',
    '(' : 'Simbolo_Parenteses_Abertura',
    ')' : 'Simbolo_Parenteses_Fecha',
    '?' : 'Simbolo_Interrogacao',
    '^' : 'Simbolo_Circunflexo',
}
symbols_key = symbols.keys()


punctuation_symbol = { ':' : 'Dois-Pontos',
                        ';' : 'Ponto-Virgula', 
                        '.' : 'Ponto' , 
                        ',' : 'Virgula' }
punctuation_symbol_key = punctuation_symbol.keys()


keywords = {
    'auto': 'auto',
    'break': 'break',
    'case': 'case',
    'char': 'char',
    'const': 'const',
    'continue': 'continue',
    'default': 'default',
    'do': 'do',
    'double': 'double',
    'else': 'else',
    'enum': 'enum',
    'extern': 'extern',
    'float': 'float',
    'for': 'for',
    'goto': 'goto',
    'if': 'if',
    'int': 'int',
    'long': 'long',
    'register': 'register',
    'return': 'return',
    'short': 'short',
    'signed': 'signed',
    'sizeof': 'sizeof',
    'static': 'static',
    'struct': 'struct',
    'switch': 'switch',
    'typedef': 'typedef',
    'union': 'union',
    'unsigned': 'unsigned',
    'void': 'void',
    'volatile': 'volatile',
    'while': 'while',
    'printf' : 'printf',
    'scanf' : 'scanf'
}
keywords_key = keywords.keys()

identifier_pattern = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')
number_pattern = re.compile(r'^[0-9]+$')
string_pattern = re.compile(r'^\".*\"$|^\'.*\'$', re.UNICODE) 

results = []

with open("C.txt", encoding='utf-8') as file:
    for line_number, line in enumerate(file, start=1):

        line = re.sub(r'//.*?(\n|$)', '\n', line)
        line = re.sub(r'/\*.*?\*/', '', line, flags=re.DOTALL)

        line = re.sub(r'#include.*?\n', '', line)

        token_pattern = re.compile(r'(\".*?\"|\'.*?\'|[a-zA-Z_][a-zA-Z0-9_]*|==|=|\+|\-|\*|\/|<|>|%|&|\||~|!|{|}|[|]|\(|\)|\?|:|;|\.|,|\s+)')
        tokens = token_pattern.findall(line)

        column_number = 1
        for token in tokens:
            token = token.strip()
            if not token:
                column_number += len(token)
                continue

            result = {'Lexema': token, 'Token': None, 'Linha': line_number, 'Coluna': column_number}

            if token in operators_key:
                result['Token'] = 'Identificador de Operador: ' + operators[token]
            elif token in logical_operators_key:
                result['Token'] = 'Operador Lógico: ' + logical_operators[token]
            elif token in keywords_key:
                result['Token'] = 'Palavra-chave: ' + keywords[token]
            elif token in punctuation_symbol_key:
                result['Token'] = 'Símbolo de Pontuação: ' + punctuation_symbol[token]
            elif token in symbols_key:
                result['Token'] = 'Símbolo: ' + symbols[token]
            elif identifier_pattern.match(token):
                result['Token'] = 'Identificador'
            elif number_pattern.match(token):
                result['Token'] = 'Número'
            elif string_pattern.match(token):
                result['Token'] = 'String'
            else:
                result['Token'] = 'Token não faz parte do vocabulário (Erro)'

            results.append(result)
            column_number += len(token) + 1


df = pd.DataFrame(results)

base_filename = "tabela_simbolos"
counter = 1
filename = f"{base_filename}_{counter}.xlsx"


while os.path.exists(filename):
    counter += 1
    filename = f"{base_filename}_{counter}.xlsx"

df.to_excel(filename, index=False)
print("Tabela de símbolos gerada com sucesso!")