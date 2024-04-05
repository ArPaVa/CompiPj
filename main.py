import runner
from hulk import hulk_parse
from lexer import tokenize, Token, Terminal
from scope import RunScope, Attribute, Method, Type, Instance, Context
from m_ast import *
import math
import random

runer = runner.Runner(runner.builting, runner.ctes)

try:
    root = hulk_parse(tokenize("""
                            
    print("Happy Thoughts")


    """))
    
except Exception as er:
    print(f"Parsing error: {er}")

#inheritance     type Point(x,y) {
    # x = x;
    # y = y;

    # getX() => self.x;
    # getY() => self.y;

    # setX(x) => self.x := x;
    # setY(y) => self.y := y;
    # }
    # type PolarPoint inherits Point {
    # rho() => sqrt(self.getX() ^ 2 + self.getY() ^ 2);}
                                   
    # let pt = new PolarPoint(3,4) in
    # print("rho: " @ pt.rho());

#for (x in range(0, 10)) print(x); Runtime error: The function next with 0 parameters is not defined
    
# a:=42; como unico codigo no da error y debería

# si una variable se llama newx da error de parsing
try:
    root.accept(runer)
except Exception as er:
    print(f"Runtime error: {er}")
