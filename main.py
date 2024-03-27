from enum import Enum

import regex
from parsing import AttributeGrammar, build_slr_parser
from utils import Token

re = regex.regex('hey+')

# print(re.nfa.powerset_construction())
print(re.match('heyyyyyyyyyyyyyyyyy'))
print(re.match('heyyyuyyyyyyyyyyyyy'))
print(re.match('heuyyyyyyyyyyyyyyyy'))

re = regex.regex('blue|red')

print(re.match('blue'))
print(re.match('red'))

re = regex.regex('He is a fine man you know!!( Or is he\\?)?')

print(re.match('He is a fine man you know!!'))
print(re.match('He is a fine man you know!! Or is he?'))

re = regex.regex('((pi+|pika+|pikachu)( *)?)+')

print(re.match('pika pika piii pikachu pi pikaaaaaaaaa pikachu pika pii'))

re = regex.regex('[a-zA-Z]+')

print(re.match('kajsdkajsdkajsnkjnKBJGVYACSYAVysGVAsgVYAgsvUAGVsUTA'))

re = regex.regex('[0-9]+')

print(re.match('123'))

re = regex.regex('\\**')

print(re.match('**************************'))
print(re.match(''))

re = regex.regex('listen carefully ([A-Z][a-zA-Z]*) (cough!? ?)* the secret code is ([a-zA-Z0-9\\*\\+=,.!\\?]+)')

print(re.match('listen carefully Natasha cough! cough cough! the secret code is l!ea$v,em.ea9384lone'))

##########################

TokenType = Enum('TokenType', [
    # Non-terminals
    'Start', 'ArithmeticExpression', 'Term', 'USub', 'Factor', 'Base', 'PossibleArguments',
    # Terminals
    'Plus', 'Sub', 'Prod', 'Div', 'Rem', 'Pow', 'ParenL', 'ParenR',
    # Terminals in this context
    'Number',
    # Extra
    'EOF'
])

# noinspection PyUnresolvedReferences
arith = AttributeGrammar(
    [TokenType.Plus, TokenType.Sub, TokenType.Prod, TokenType.Div, TokenType.Rem, TokenType.Pow, TokenType.ParenL,
     TokenType.ParenR, TokenType.Number],
    [
        (TokenType.Start, [TokenType.ArithmeticExpression],
         lambda s: Token(0, 0, _type=TokenType.Start, lexeme=s[0].lexeme)),

        # ArithmeticExpression
        (TokenType.ArithmeticExpression, [TokenType.ArithmeticExpression, TokenType.Plus, TokenType.Term],
         lambda s: Token(0, 0, _type=TokenType.ArithmeticExpression, lexeme=s[0].lexeme + s[2].lexeme)),

        (TokenType.ArithmeticExpression, [TokenType.ArithmeticExpression, TokenType.Sub, TokenType.Term],
         lambda s: Token(0, 0, _type=TokenType.ArithmeticExpression, lexeme=s[0].lexeme - s[2].lexeme)),

        (TokenType.ArithmeticExpression, [TokenType.Term],
         lambda s: Token(0, 0, _type=TokenType.ArithmeticExpression, lexeme=s[0].lexeme)),

        # Term
        (TokenType.Term, [TokenType.Term, TokenType.Prod, TokenType.USub],
         lambda s: Token(0, 0, _type=TokenType.Term, lexeme=s[0].lexeme * s[2].lexeme)),

        (TokenType.Term, [TokenType.Term, TokenType.Div, TokenType.USub],
         lambda s: Token(0, 0, _type=TokenType.Term, lexeme=s[0].lexeme / s[2].lexeme)),

        (TokenType.Term, [TokenType.Term, TokenType.Rem, TokenType.USub],
         lambda s: Token(0, 0, _type=TokenType.Term, lexeme=s[0].lexeme % s[2].lexeme)),

        (TokenType.Term, [TokenType.USub],
         lambda s: Token(0, 0, _type=TokenType.Term, lexeme=s[0].lexeme)),

        # USub
        (TokenType.USub, [TokenType.Factor],
         lambda s: Token(0, 0, _type=TokenType.USub, lexeme=s[0].lexeme)),

        (TokenType.USub, [TokenType.Sub, TokenType.Factor],
         lambda s: Token(0, 0, _type=TokenType.USub, lexeme=-s[1].lexeme)),

        # Factor
        (TokenType.Factor, [TokenType.Base],
         lambda s: Token(0, 0, _type=TokenType.Factor, lexeme=s[0].lexeme)),

        (TokenType.Factor, [TokenType.Base, TokenType.Pow, TokenType.Factor],
         lambda s: Token(0, 0, _type=TokenType.Factor, lexeme=s[0].lexeme ** s[2].lexeme)),

        # Base
        (TokenType.Base, [TokenType.Number],
         lambda s: Token(0, 0, _type=TokenType.Base, lexeme=s[0].lexeme)),

        (TokenType.Base, [TokenType.ParenL, TokenType.ArithmeticExpression, TokenType.ParenR],
         lambda s: Token(0, 0, _type=TokenType.Base, lexeme=s[1].lexeme))
    ], eof_symbol=TokenType.EOF)

parse = build_slr_parser(arith, by=lambda t: t.type)

code = '1 + 2 ^ 2 * 2 ^ (1 + 1 - 1)'

# noinspection PyUnresolvedReferences
tokens = [
    Token(0, 0, _type=TokenType.Number, lexeme=1),
    Token(0, 0, _type=TokenType.Plus, lexeme=0),
    Token(0, 0, _type=TokenType.Number, lexeme=2),
    Token(0, 0, _type=TokenType.Pow, lexeme=0),
    Token(0, 0, _type=TokenType.Number, lexeme=2),
    Token(0, 0, _type=TokenType.Prod, lexeme=0),
    Token(0, 0, _type=TokenType.Number, lexeme=2),
    Token(0, 0, _type=TokenType.Pow, lexeme=0),
    Token(0, 0, _type=TokenType.ParenL, lexeme=0),
    Token(0, 0, _type=TokenType.Number, lexeme=1),
    Token(0, 0, _type=TokenType.Plus, lexeme=0),
    Token(0, 0, _type=TokenType.Number, lexeme=1),
    Token(0, 0, _type=TokenType.Sub, lexeme=0),
    Token(0, 0, _type=TokenType.Number, lexeme=1),
    Token(0, 0, _type=TokenType.ParenR, lexeme=0),
    Token(0, 0, _type=TokenType.EOF, lexeme=0),
]

print(parse(tokens).lexeme)
