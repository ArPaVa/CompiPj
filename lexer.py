import regex
import utils

lista = utils.escape_terminal_tokens.keys() 
variablestring = "|".join(lista)
# print(variablestring) 
all_kw = regex.regex(variablestring)
token_list = []
codigo = '    let abc= (  345.678.45    )    =    {  }    '
while len(codigo):

    codigo = codigo.strip()
    result = all_kw.match(codigo)

    if result [0]:
        jump = result [1]
        token_list.append(utils.Token(None, None, utils.terminal_tokens[result[2]], result[2]))
        codigo = codigo[jump:]
    else:
        nextchar = codigo[0]
        if nextchar == "\"": # beginning a string
            stringchain =""
            i = 1
            while i < len(codigo) and codigo[i] != "\"":
                stringchain += codigo[i]
                i+=1
            if i >= len(codigo):
                raise Exception()
            token_list.append(utils.Token(None, None, utils.TokenType.string, stringchain))
            codigo = codigo [i+1:]
        elif nextchar.isalpha() or nextchar == '_': # beginning a identifier
            ident = ""
            i = 0
            while i < len(codigo) and (codigo[i].isalnum() or codigo[i] == '_'):
                ident += codigo[i]
                i+=1
            if i >= len(codigo):
                raise Exception()
            token_list.append(utils.Token(None, None, utils.TokenType.identifier, ident))
            codigo = codigo [i:]
        elif nextchar.isdigit():
            number_s = ""
            i = 0
            decimal = False
            while i < len(codigo) and (codigo[i].isdigit() or (codigo[i] == '.' and not decimal)):
                if codigo[i] == '.':
                    decimal = True
                number_s += codigo[i]
                i+=1
            if i >= len(codigo):
                raise Exception()
            number = float(number_s) if '.' in number_s else int(number_s)
            token_list.append(utils.Token(None, None, utils.TokenType.number, number))
            codigo = codigo [i:]
        else: 
            raise Exception()

    # print(token_list)

# from enum import Enum

# TType = Enum('TType', ['Bleh', 'Bluh', 'Blerg'])

# str2tt = {
#     'bleh': TType.Bleh,
#     'bluh': TType.Bluh,
#     'blerg': TType.Blerg
# }

# regex = '|'.join(str2tt.keys())
# print(regex)