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
        if not all([isinstance(i, int) for i in min_max]):
            raise AssertionError()
        return random.randint(*min_max)


import tempfile
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

    with tempfile.TemporaryFile(mode="w+t") as tmp:
        tmp.write("config file.")


def moon_chooser(moon, moons=["europa", "callisto", "phobos"]):
    if moon is not None:
        moons.append(moon)

    return random.choice(moons)


