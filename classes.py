"""
Test file for PYL-W0223 false positives.

PYL-W0223 (abstract-method) should NOT be raised when a base class method
is not decorated with @abc.abstractmethod but merely raises NotImplementedError
as an informal convention. Pylint incorrectly treats these as abstract methods
and flags subclasses that don't override them.
"""

import abc

print(abcd)
breakpoint()

# Case 1: Informal abstract method using NotImplementedError (no ABC)
# Pylint should NOT flag subclasses for not overriding these.
class InformalBase:
    def do_something(self):
        raise NotImplementedError

    def do_another_thing(self):
        raise NotImplementedError("Subclasses should implement this")

    def concrete_method(self):
        return 42


class InformalChild(InformalBase):
    """Only overrides one method. Should NOT trigger PYL-W0223."""

    def do_something(self):
        return "done"


# Case 2: ABC base with a mix of real abstract methods and informal ones
class MixedBase(abc.ABC):
    @abc.abstractmethod
    def must_implement(self):
        """This is truly abstract."""

    def optional_hook(self):
        """This is an informal hook, not abstract."""
        raise NotImplementedError

    def another_hook(self):
        raise NotImplementedError("Override if needed")


class MixedChild(MixedBase):
    """Implements the real abstract method but not the informal hooks.
    Should NOT trigger PYL-W0223 for optional_hook or another_hook."""

    def must_implement(self):
        return "implemented"


# Case 3: Multi-level inheritance with informal abstract
class GrandparentBase:
    def overridable(self):
        raise NotImplementedError


class ParentMiddle(GrandparentBase):
    """Does not override overridable. Should NOT trigger PYL-W0223."""
    pass


class GrandChild(ParentMiddle):
    """Also does not override overridable. Should NOT trigger PYL-W0223."""
    pass


# Case 4: Real abstract method - PYL-W0223 SHOULD fire here (true positive)
class TrueAbstractBase(abc.ABC):
    @abc.abstractmethod
    def required_method(self):
        pass


class IncompleteChild(TrueAbstractBase):
    """Does NOT implement required_method. PYL-W0223 is valid here."""
    pass
