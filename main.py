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

EOF, Start, ArithmeticExpression, Term, USub, Factor, Base, Plus, Sub, Prod, Div, Rem, Pow, ParenL, ParenR, Number = range(16)

arith = AttributeGrammar(
    [Plus, Sub, Prod, Div, Rem, Pow, ParenL, ParenR, Number],
    [
        (Start, [ArithmeticExpression],
         lambda s: Token(0, 0, _type=Start, lexeme=s[0].lexeme)),

        # ArithmeticExpression
        (ArithmeticExpression, [ArithmeticExpression, Plus, Term],
         lambda s: Token(0, 0, _type=ArithmeticExpression, lexeme=s[0].lexeme + s[2].lexeme)),

        (ArithmeticExpression, [ArithmeticExpression, Sub, Term],
         lambda s: Token(0, 0, _type=ArithmeticExpression, lexeme=s[0].lexeme - s[2].lexeme)),

        (ArithmeticExpression, [Term],
         lambda s: Token(0, 0, _type=ArithmeticExpression, lexeme=s[0].lexeme)),

        # Term
        (Term, [Term, Prod, USub],
         lambda s: Token(0, 0, _type=Term, lexeme=s[0].lexeme * s[2].lexeme)),

        (Term, [Term, Div, USub],
         lambda s: Token(0, 0, _type=Term, lexeme=s[0].lexeme / s[2].lexeme)),

        (Term, [Term, Rem, USub],
         lambda s: Token(0, 0, _type=Term, lexeme=s[0].lexeme % s[2].lexeme)),

        (Term, [USub],
         lambda s: Token(0, 0, _type=Term, lexeme=s[0].lexeme)),

        # USub
        (USub, [Factor],
         lambda s: Token(0, 0, _type=USub, lexeme=s[0].lexeme)),

        (USub, [Sub, Factor],
         lambda s: Token(0, 0, _type=USub, lexeme=-s[1].lexeme)),

        # Factor
        (Factor, [Base],
         lambda s: Token(0, 0, _type=Factor, lexeme=s[0].lexeme)),

        (Factor, [Base, Pow, Factor],
         lambda s: Token(0, 0, _type=Factor, lexeme=s[0].lexeme ** s[2].lexeme)),

        # Base
        (Base, [Number],
         lambda s: Token(0, 0, _type=Base, lexeme=s[0].lexeme)),

        (Base, [ParenL, ArithmeticExpression, ParenR],
         lambda s: Token(0, 0, _type=Base, lexeme=s[1].lexeme))
    ], eof_symbol=EOF)

parse = build_slr_parser(arith, by=lambda t: t.type)

code = '1 + 2 ^ 2 * 2 ^ (1 + 1 - 1)'

# noinspection PyUnresolvedReferences
tokens = [
    Token(0, 0, _type=Number, lexeme=1),
    Token(0, 0, _type=Plus, lexeme=0),
    Token(0, 0, _type=Number, lexeme=2),
    Token(0, 0, _type=Pow, lexeme=0),
    Token(0, 0, _type=Number, lexeme=2),
    Token(0, 0, _type=Prod, lexeme=0),
    Token(0, 0, _type=Number, lexeme=2),
    Token(0, 0, _type=Pow, lexeme=0),
    Token(0, 0, _type=ParenL, lexeme=0),
    Token(0, 0, _type=Number, lexeme=1),
    Token(0, 0, _type=Plus, lexeme=0),
    Token(0, 0, _type=Number, lexeme=1),
    Token(0, 0, _type=Sub, lexeme=0),
    Token(0, 0, _type=Number, lexeme=1),
    Token(0, 0, _type=ParenR, lexeme=0),
    Token(0, 0, _type=EOF, lexeme=0),
]

print(parse(tokens).lexeme)
