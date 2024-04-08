from functools import wraps

from hulk import hulk_parse
from lexer import tokenize
from runtime import default_runtime


def hulk_compile(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        ast = hulk_parse(tokenize(f.__doc__))
        return ast.accept(default_runtime)

    return wrapper


@hulk_compile
def point_and_friends():
    """
        type Point(x, y) {
            x = x;
            y = y;

            getX() => self.x;
            getY() => self.y;

            setX(x) => self.x := x;
            setY(y) => self.y := y;
        }

        type PolarPoint(phi, rho) inherits Point(rho * sin(phi), rho * cos(phi)) {
            rho() => sqrt(self.getX() ^ 2 + self.getY() ^ 2);
        }

        let pt = new PolarPoint(PI/4, sqrt(2)) in
            print(pt.x @@ pt.y)
    """
    pass


@hulk_compile
def vector_and_for():
    """
        type Vector(v) {
            v = v;
            index = -1;
            __getitem__ = self.v.__getitem__;

            size() => self.v.__len__();

            next() {
                self.index := self.index + 1;
                self.index < self.size()
            }

            current() => self.v[self.index];

        }

        let
            v = [1, 2, 3, 4, 5, 6],
            time = import("time")
        in
            for (x in v) {
                # time.sleep(x);
                print(x)
            }
    """
    pass


@hulk_compile
def lords_and_regular_people():
    """
    type Person(firstname, lastname) {
        firstname = firstname;
        lastname = lastname;

        name() => self.firstname @@ self.lastname;
    }
    type Knight(firstname, lastname) inherits Person(firstname, lastname) {
        name() => "Sir" @@ base();
    }

    let p = new Knight("Phil", "Collins") in
        print(p.name())
    """
    pass


@hulk_compile
def ranger():
    """
        type Range(min: Number, max: Number) {
            min = min - 1;
            max = max;

            next() {
                self.min := self. min + 1;
                self.min < self.max
            }

            current() => self.min;
        }

        function range(min, max) => new Range(min, max);


        for (x in range(0, 10)) print(x)
    """
    pass


@hulk_compile
def types_and_sht():
    """
        type A {}
        type B inherits A {}

        protocol Fooer { foo(s: Object): Number; }
        protocol Barer extends Fooer { bar(): Number; }

        type C { bar(): Number => 1; foo(a: Number): Number => 1; }

        {
            print("1 is Number:" @@ (1 is Number));
            print("new A() is A:" @@ (new A() is A));
            print("new B() is A:" @@ (new B() is A));
            print("new C() is Fooer:" @@ (new C() is Fooer))
        }
    """
    pass


@hulk_compile
def hello_world():
    """
        print("Hello World")
    """
    pass


# point_and_friends()
# vector_and_for()
# lords_and_regular_people()
# ranger()
# types_and_sht()
hello_world()
