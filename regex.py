import string

from automata import char, char_range, build_recognizer
from parsing import AttributeGrammar, build_slr_parser

special = '|*+?[]-\\()'
regular = set(string.printable).difference(special)

regex_grammar = AttributeGrammar(
    string.printable,
    [
        ('Start', ['Expression']),
        ('Expression', ['Expression', '|', "Subexpression"], lambda s: s[0] | s[2]),
        ('Expression', ['Subexpression'], lambda s: s[0]),
        ('Subexpression', ['Subexpression', 'SubexpressionItem'], lambda s: s[0] + s[1]),
        ('Subexpression', ['SubexpressionItem'], lambda s: s[0]),
        ('SubexpressionItem', ['Match', '*'], lambda s: s[0].star()),
        ('SubexpressionItem', ['Match', '+'], lambda s: s[0] + s[0].star()),
        ('SubexpressionItem', ['Match', '?'], lambda s: s[0].opt()),
        ('SubexpressionItem', ['Match'], lambda s: s[0]),
        ('Match', ['CharacterGroup'], lambda s: s[0]),
        ('Match', ['Character'], lambda s: s[0]),
        ('Match', ['(', 'Expression', ')'], lambda s: s[1]),
        ('CharacterGroup', ['[', 'CharacterGroupItems', ']'], lambda s: s[1]),
        ('CharacterGroupItems', ['CharacterGroupItems', 'CharacterGroupItem'], lambda s: s[0] | s[1]),
        ('CharacterGroupItems', ['CharacterGroupItem'], lambda s: s[0]),
        ('CharacterGroupItem', ['CharacterRange'], lambda s: s[0]),
        ('CharacterGroupItem', ['Character'], lambda s: s[0]),
        ('CharacterRange', ['Character', '-', 'Character'], lambda s: char_range(s[0], s[2])),
        ('Character', ['EscapeSequence'], lambda s: s[0]),
        ('Character', ['Char'], lambda s: s[0])]
    + [('Char', [ch], lambda s: char(s[0])) for ch in regular]
    + [('EscapeSequence', ['\\', ch], lambda s: char(s[1])) for ch in special])

regex_parse = build_slr_parser(regex_grammar)


# noinspection PyPep8Naming
class regex:

    def __init__(self, pattern):
        self.pattern = pattern
        self.nfa = regex_parse(list(pattern) + [0])
        self.recognize = build_recognizer(self.nfa)

    def __repr__(self):
        return f'r\'{self.pattern}\''

    def match(self, input_string):
        match, index = self.recognize(list(input_string) + [0])
        return match, index, input_string[:index]
