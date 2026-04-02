# Test cases for FLK-E122: continuation line missing indentation or outdented
#
# E122 is raised when a continuation line (inside brackets/parens/braces or
# after a backslash) has no indentation where indentation is expected.
#
# For multi-line expressions, flake8 reports E122 at the first offending
# continuation line — not on every subsequent line of the same expression.


# ---------------------------------------------------------------------------
# 1. Function call arguments — continuation line at column 0
# ---------------------------------------------------------------------------

# E122 on line below (first continuation line, column 0)
result = dict(key1="value1",
key2="value2",
key3="value3")

# E122 on line below
output = print("hello world",
"foo",
"bar")


# ---------------------------------------------------------------------------
# 2. Function definition parameters — continuation line at column 0
# ---------------------------------------------------------------------------

# E122 on line below
def my_function(param_one, param_two,
param_three, param_four):
    pass


# E122 on line below
def another_function(
param_a,
param_b,
param_c):
    pass


# ---------------------------------------------------------------------------
# 3. List literals — continuation line at column 0
# ---------------------------------------------------------------------------

# E122 on line below
my_list = [
"apple",
"banana",
"cherry",
]

# E122 on line below
nested = [[1, 2, 3],
[4, 5, 6],
[7, 8, 9]]


# ---------------------------------------------------------------------------
# 4. Dictionary literals — continuation line at column 0
# ---------------------------------------------------------------------------

# E122 on line below
config = {
"host": "localhost",
"port": 8080,
"debug": True,
}

# E122 on line below
mapping = {"alpha": 1,
"beta": 2,
"gamma": 3}


# ---------------------------------------------------------------------------
# 5. Tuple literals — continuation line at column 0
# ---------------------------------------------------------------------------

# E122 on line below
coordinates = (
10,
20,
30,
)

# E122 on line below
point = (1,
2,
3)


# ---------------------------------------------------------------------------
# 6. Set literals — continuation line at column 0
# ---------------------------------------------------------------------------

# E122 on line below
unique_ids = {
101,
202,
303,
}


# ---------------------------------------------------------------------------
# 7. Arithmetic / boolean expressions spanning multiple lines
# ---------------------------------------------------------------------------

# E122 on line below (first continuation, no indent)
total = (100 +
200 +
300 +
400)

# E122 on line below
is_valid = (
True or
False or
True)

# E122 on line below
long_condition = (some_value > 0 and
other_value < 100 and
third_value != 0)


# ---------------------------------------------------------------------------
# 8. Chained method calls spanning multiple lines
# ---------------------------------------------------------------------------

# E122 on line below
result = (
"hello world"
.strip()
.upper()
.split())

# E122 on line below
items = (
[1, 2, 3, 4, 5]
[1:3])


# ---------------------------------------------------------------------------
# 9. Imports spanning multiple lines
# ---------------------------------------------------------------------------

# E122 on line below
from os.path import (join,
dirname,
basename,
exists)

# E122 on line below
from collections import (
OrderedDict,
defaultdict,
namedtuple)


# ---------------------------------------------------------------------------
# 10. Decorator arguments spanning multiple lines
# ---------------------------------------------------------------------------

# E122 on line below
@some_decorator(arg1,
arg2,
arg3)
def decorated():
    pass


# ---------------------------------------------------------------------------
# 11. Return statements spanning multiple lines
# ---------------------------------------------------------------------------

def build_response():
    # E122 on line below
    return dict(
status="ok",
data=[],
count=0,
)


def calculate():
    # E122 on line below
    return (
1 +
2 +
3
)


# ---------------------------------------------------------------------------
# 12. Assignments with long right-hand side spanning multiple lines
# ---------------------------------------------------------------------------

# E122 on line below
message = ("This is the first part "
"and this is the second part "
"and this is the third part.")

# E122 on line below
value = (
some_long_variable_name +
another_long_variable_name +
yet_another_variable)


# ---------------------------------------------------------------------------
# 13. Conditional expressions (ternary) spanning multiple lines
# ---------------------------------------------------------------------------

# E122 on line below
label = ("yes"
if condition
else "no")


# ---------------------------------------------------------------------------
# 14. Function call with keyword arguments spanning multiple lines
# ---------------------------------------------------------------------------

# E122 on line below
connection = connect(host="localhost",
port=5432,
user="admin",
password="secret",
database="mydb")

# E122 on line below
response = requests.get(
url,
params={"key": "value"},
headers={"Accept": "application/json"},
timeout=30)


# ---------------------------------------------------------------------------
# 15. Class definition base classes spanning multiple lines
# ---------------------------------------------------------------------------

# E122 on line below
class MyClass(BaseClassOne,
BaseClassTwo,
BaseClassThree):
    pass


# E122 on line below
class AnotherClass(
Mixin,
Base):
    pass


# ---------------------------------------------------------------------------
# 16. Assert statements spanning multiple lines
# ---------------------------------------------------------------------------

# E122 on line below
assert (result == expected and
error is None and
len(items) > 0), "Assertion failed"


# ---------------------------------------------------------------------------
# 17. With statement context managers spanning multiple lines
# ---------------------------------------------------------------------------

# E122 on line below
with open("file1.txt") as f1, open(
"file2.txt") as f2:
    pass


# ---------------------------------------------------------------------------
# 18. Raise statements spanning multiple lines
# ---------------------------------------------------------------------------

def validate(value):
    # E122 on line below
    raise ValueError(
"The provided value is invalid: "
+ str(value))


# ---------------------------------------------------------------------------
# 19. Lambda with long body spanning multiple lines (via assignment)
# ---------------------------------------------------------------------------

# E122 on line below
transform = lambda x: (
x * 2
+ 1)


# ---------------------------------------------------------------------------
# 20. Nested calls where outer call's continuation is at column 0
# ---------------------------------------------------------------------------

# E122 on line below
sorted_data = sorted(
my_list,
key=lambda x: x["name"],
reverse=True)
