import sys

from checks import HulkSemanticError, default_semantic_checker, default_type_checker
from hulk import hulk_parse
from lexer import tokenize
from runtime import default_runtime


def run(code, check=True):
    ast = hulk_parse(tokenize(code))

    if check:  # why tho?
        ast.accept(default_semantic_checker)
        ast.accept(default_type_checker)

    return ast.accept(default_runtime)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        while True:
            try:
                result = run(input('hulk> '))
                default_runtime.scope['_'] = result

            except (SyntaxError, HulkSemanticError, KeyError) as err:
                # TODO: pretty print
                print(repr(err))

    with open(sys.argv[1]) as file:
        run(file.read())
