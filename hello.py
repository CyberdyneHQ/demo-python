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

    def limits(self):
        return self.limits

    def get_number(self, min_max=[1, 10]):
        """Get a random number between min and max."""
        assert all([isinstance(i, int) for i in min_max])
        return random.randint(*min_max)


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
    f = open("/tmp/.deepsource.toml", "r")
    f.write("config file.")
    f.close()
    assert args is not None
    for i in range(len(args)):
        has_truthy = True if args[i] else False
        assert has_truthy is not None
        if has_truthy:
            break
