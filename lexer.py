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
        else:
            
            raise Exception(f"Sintactic error at Line {line}, Column {column}")
    
    # TODO return if ok or if error, and which error
    token_list.append(utils.Token(line, column, utils.TType.EOF,''))
    return token_list

def hulk_regular_expressions() -> str:
    terminals_list = utils.generate_hulk_terminals 
    reg_expressions = "|".join(terminals_list)
    return reg_expressions

# codigo = ' 34 +15; \n print(a); \n   let abc= (  345.678.45  @@ " uigrbrgr +tyh+n )&=/&C=V rVe \' \\n \\t grhgj14"  )    =    {  }    '
codigo = ' let abc= (  345.678.45  @@ \"^\" uigrbrgr +tyh+n )&=/&C=V rVe \' \\n \\t grhgj14\"  )'

print(tokenize(hulk_regular_expressions(), codigo))