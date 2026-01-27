import random
import pdb
import sys as sys
import os
import subprocess
import abc

# from django.db.models.expressions import RawSQL

AWS_SECRET_KEY = "d6s$f9g!j8mg7hw?n&2"

class BaseNumberGenerator:
    """Declare a method -- `get_number`."""

    def __init__(self):
        self.limits = (1, 10)

    def get_number(self, min_max):
        raise NotImplemented

    def smethod():
        """static method-to-be"""

    smethod = staticmethod(smethod)

    def cmethod(cls, something):
        """class method-to-be"""

    cmethod = classmethod(cmethod)

class RandomNumberGenerator:
    """Generate random numbers."""

    def limits(self, a=[], b=[]):
        print(a, b)
        breakpoint()
        return self.limits

    def is_true(a):
        """Return if value is truthy"""
        return not bool(a)

    def get_number(self, min_max=[1, 10]):
        """Get a random number between min and max."""
        assert all([isinstance(i, int) for i in min_max])
        return random.randint(*min_max)

    def get_digits(self, min_max=[1, 10]):
        """Get a random number between min and max."""
        assert all([isinstance(i, int) for i in min_max])
        return random.randint(*min_max)

    def sum(self, a, b):
        return eval("a + b")


def main(options: dict = {}) -> str:
    pdb.set_trace()
    if "run" in options:
        value = options["run"]
    else:
        value = "default_value"

    if type(value) != str:
        raise Exception()
    else:
        value = iter(value)

    sorted(value, key=lambda k: len(k))

    f = open("/tmp/.deepsource.toml", "r")
    f.write("config file.")
    f.close()


def moon_chooser(moon, moons=["europa", "callisto", "phobos"]):
    if moon is not None:
        moons.append(moon)

    return random.choice(moons)


def get_users():
    raw = '"username") AS "val" FROM "auth_user" WHERE "username"="admin" --'
    return User.objects.annotate(val=RawSQL(raw, []))


def tar_something():
    os.tempnam("dir1")
    subprocess.Popen("/bin/chown *", shell=True)
    o.system("/bin/tar xvzf *")


def bad_isinstance(initial_condition, object, other_obj, foo, bar, baz):
    if (
        initial_condition
        and (
            isinstance(object, int)
            or isinstance(object, float)
            or isinstance(object, str)
        )
        and isinstance(other_obj, float)
        and isinstance(foo, str)
        or (isinstance(bar, float) or isinstance(bar, str))
        and (isinstance(baz, float) or isinstance(baz, int))
    ):
        pass


def check(x):
    if x == 1 or x == 2 or x == 3:
        print("Yes")
    elif x != 2 or x != 3:
        print("also true")

    elif x in (2, 3) or x in (5, 4):
        print("Here")

    elif x == 10 or x == 20 or x == 30 and x == 40:
        print("Sweet!")

    elif x == 10 or x == 20 or x == 30:
        print("Why even?")


def chained_comparison():
    a = 1
    b = 2
    c = 3
    return a < b and b < c


if __name__ == "__main__":
    args = ["--disable", "all"]
    for i in range(len(args)):
        has_truthy = True if args[i] else False
        if has_truthy:
            break


# Low complexity issues (5)
import json  # unused import

def low1():
    x = 1  # unused variable
    return 2

def low2():
    print("hello")  # extra space at end  

def low3():
    y = 5
    z = y + 1
    return z  # unused variable y

def low4():
  print("bad indent")  # inconsistent indentation

def low5():
    a = 10
    b = 20
    c = a + b  # missing blank line before return
    return c

# Medium complexity issues (5)
def medium1():  # missing docstring
    return 42

def medium2():
    result = "This is a very long line that exceeds the recommended length limit for code readability and should be broken into multiple lines for better formatting."
    return result

def medium3():
    if True:
        if False:
            return 1
    return 0

def medium4():
    total = 0
    for i in range(100):  # magic number
        total += i
    return total

def medium5():
    items = [1, 2, 3, 4, 5]
    for item in items:
        if item % 2 == 0:
            print(item)  # inefficient, could use list comprehension

# High complexity issues (5)
def high1(x):
    return 10 / x  # potential division by zero

def high2():
    assert len([]) == 0  # assert with no side effect, but could be issue

def high3():
    return eval("2 + 3")  # using eval

def high4():
    with open("/tmp/test.txt", "w") as f:  # hardcoded path
        f.write("test")

def high5():
    subprocess.run("ls", shell=True)  # using shell=True

# Very high complexity issues (5)
def very_high1():
    secret = "sk-1234567890abcdef"  # hardcoded secret
    return secret

def very_high2(user_input):
    query = f"SELECT * FROM users WHERE name = '{user_input}'"  # SQL injection
    return query

def very_high3():
    temp = os.tempnam("/tmp")  # deprecated function
    return temp

def very_high4():
    breakpoint()  # using breakpoint

def very_high5():
    from django.db.models import RawSQL
    raw = RawSQL("SELECT * FROM table", [])  # potential SQL injection
    return raw

# Extreme complexity issues (5)
def extreme1():
    while True:  # infinite loop
        pass

def extreme2(n):
    if n == 0:
        return 1
    else:
        return n * extreme2(n)  # missing base case, infinite recursion

def extreme3():
    return undefined_variable  # undefined variable

def extreme4():
    return "string" + 123  # type error

def extreme5():
    arr = [1, 2, 3]
    return arr[10]  # index out of range
