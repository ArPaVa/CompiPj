# import pytest
# from main import runer, hulk_parse, tokenize
# import math

# def test_program():
    
#     root = hulk_parse(tokenize("""

#     print(sin(2 * PI) ^ 2 + cos(3 * PI / log(4, 64)));
#     """))


#     # si una variable se llama newx da errorde parsing
#     acepted= root.accept(runer)
#     a = math.sin(2 * math.pi) ** 2 + math.cos(3 * math.pi / math.log(4, 64))

#     assert acepted == a