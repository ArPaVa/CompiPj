import regex
import utils

def tokenize(regular_grammar, code:str):
    print(regular_grammar)
    lexer = regex.regex(regular_grammar)
    token_list = []
    column = 1
    line = 1
    while len(code):
        jump = len(code)
        code = code.lstrip(' ')
        
        if not len(code): break

        if  code[0] == '\n': 
            code = code[1:]
            line += 1
            column = 1
            continue

        jump = jump - len(code)
        column += jump                      
        match_result = lexer.match(code)


        if match_result [0]:
            
            jump = match_result [1]
            token_type = utils.terminal_tokens.get(match_result[2],None)
            lexeme = match_result[2]
            if token_type == None:
                if match_result[2][0]=='"':
                    token_type = utils.TType.string_chain
                elif match_result[2][0].isdigit():
                    token_type = utils.TType.number
                else:
                    token_type = utils.TType.identifier


            token_list.append(utils.Token(line, column, token_type, lexeme))
            column += jump
            code = code[jump:]
        #else:
        #     nextchar = code[0]
        #     if nextchar == "\"": # beginning a string
        #         stringchain =""
        #         i = 1
        #         while i < len(code) and code[i] != "\"":
        #             stringchain += code[i]
        #             i+=1
        #         if i >= len(code):
        #             raise Exception()
        #         token_list.append(utils.Token(line, column, utils.TType.string, stringchain))
        #         column += i+1
        #         code = code [i+1:]
        #     elif nextchar.isalpha() or nextchar == '_': # beginning a identifier
        #         ident = ""
        #         i = 0
        #         while i < len(code) and (code[i].isalnum() or code[i] == '_'):
        #             ident += code[i]
        #             i+=1
        #         if i >= len(code):
        #             raise Exception()
        #         token_list.append(utils.Token(line, column, utils.TType.identifier, ident))
        #         column += i
        #         code = code [i:]
        #     elif nextchar.isdigit(): # beginning a number
        #         number_s = ""
        #         i = 0
        #         decimal = False
        #         while i < len(code) and (code[i].isdigit() or (code[i] == '.' and not decimal)):
        #             if code[i] == '.':
        #                 decimal = True
        #             number_s += code[i]
        #             i+=1
        #         if i >= len(code):
        #             raise Exception()
        #         number = float(number_s) if '.' in number_s else int(number_s)
        #         token_list.append(utils.Token(line, column, utils.TType.number, number))
        #         column += i
        #         code = code [i:]
        #     else: 
        #         raise Exception()

        # print(token_list)
    
    # TODO return if ok or if error, and which error
    return token_list

def hulk_regular_expressions() -> str:
    terminals_list = utils.generate_hulk_terminals 
    reg_expressions = "|".join(terminals_list)
    return reg_expressions

#codigo = ' 34 +15; \n print(a); \n   let abc= (  345.678.45    )    =    {  }    '
codigo = ' 34 + 15;'

print(tokenize(hulk_regular_expressions(), codigo))