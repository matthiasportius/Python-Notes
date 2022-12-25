# Python-Notes

This repository is a collection of intermediate Python concepts which I am currently studying.
It shall provide a succinct compilation of (in my mind) important concepts and features
of the programming language Python.


## The Zen of Python<sub><sup><sup>[[py]](zen_of_python.py)</sup></sup></sup>

If in doubt at any point, always remember the **Zen of Python**.
Just [`import this`](https://peps.python.org/pep-0020/).


## Pythons object model<sub><sup><sup>[[py]](object_model.py)</sup></sup></sup>

**Everything** in Python **is an object**.
You can proof this quite easily:
```python
def foo():
    pass

l = [
    isinstance(1, object), 
    isinstance(True, object),
    isinstance(list(), object),
    isinstance("Hello", object),
    isinstance(foo, object)
    ]

for o in l:
    print(o, end=" ")
print()
```

Actually the underlying implementation of variables and such is a [**`PyObject`**](https://stackoverflow.com/a/27683778).
Each of these `PyObject`s contains at least **three types of data**:
* reference count
* type
* value
<img src="https://github.com/matthiasportius/Python-Notes/blob/master/PyObject_scheme.png" alt="PyObject scheme" align="center" width="65%" title="Schematic representation of data in memory" />
<!-- also possible: 
![PyObject scheme](https://github.com/matthiasportius/Python-Notes/blob/master/PyObject_scheme.png?raw=true)
-->

### Python objects

There are **two types of objects**:
* **mutable**
  * list, set, dict
* **immutable**
  * int, str, bool, ...

If you try to **modify immutable objects** you **get new objects**. This can be easily shown via the [`id()`](https://docs.python.org/3/library/functions.html#id)
function which returns the identity of an object (In CPython: adress of the object in memory).
```python
x = 5
s = "hi"
print(x, id(x))
print(s, id(s))

x += 1
s += "world"
print(x, id(x))
print(s, id(s))
```

For **mutable objects** the **identity stays the same**, as can be tested with:
```python
l = [1, 2, 3]
print(l, id(l))

l.append(4)
print(l, id(l))
```


### Names, not variables

In Python one does not create *variables* but *names*.
This is also part of why Python does not use pointers like C does (although it is more of a design choice that pointers do not exist in Python).
The *name* points to a `PyObject` holding the actual value.
When I do: `x = 1` these steps are performed:
1. Create a [`PyObject`](https://docs.python.org/3/c-api/structures.html#c.PyObject) in C (as a C `struct`)
2. Set the type of the `PyObject` to integer
3. Set the value of the `PyObject` to `1`
4. Create a *name* called `x`
5. Point `x` to the new `PyObject`
6. Increase the reference count of the `PyObject`by 1

Whereas in C `int x = 1` would do:
1. Allocate enough memory for an integer
2. Assign the value `1` to that memory location
3. Indicate that x points to `1`

So in Python, `x` is only a *name* pointing to the "real" object with type, value and refcount.
That means `x` does not directly "own" any memory adress like a variable in C.
The PyObject does.

So what happens when I re-assign the variable `x = 3` in Python is:
1. Create a new PyObject
2. Set the type of the `PyObject` to integer
3. Set the value of the `PyObject` to `3`
4. Point the *name* `x` to the new PyObject
5. Increase the reference count of the new `PyObject`by 1
6. Decrease the reference count of the old `PyObject`by 1
   * If the reference count is 0 the object gets cleaned up by the garbage collector

If i would do `x = 3` in C it would just assign the new value `3` to the *variable* `x` (overwriting the previous value while not changing the memory location).
This is why `x` is __mutable in C__ but __immutable in Python__.

Doing `y = x` would not create a new object, just a new name that points to the 
existing `PyObject`, increasing its refcount by 1.
This can be tested with [`is`](https://stackoverflow.com/a/133024) 
which checks if two names refer to the same object: `y is x` returns `True`.
`sys.getrefcount("1")` before and after the assignement shows the increase of the reference count by 1.


### Namespaces

As described before, `x = 1` creates a *symbolic name* `x` which can be used to reference the `PyObject`.
With that `x` is collected in the __*namespace*__ together with its reference object. 
The *namespace* is implemented as a dictionary with keys (object names) and values (objects).
There are **4 types of namespaces** with different lifetimes:
* **built-in**
  * names of Python's built-in objects 
  * creation: always available when Python is running
  * lifetime: until interpreter terminates
  * `dir(__builtins__)`
* **global**
  * names defined at level of main program
  * creation: when main is started
  * lifetime: until interpreter terminates
  * `globals()`
* **enclosing**
  * names defined in the function enclosing the current function
  * creation: when function executes
  * lifetime: until function terminates
* **local**
  * names defined in the current function, *local to a function*
  * creation: when function executes
  * lifetime: until function terminates
  * `locals()`

Many namespaces will exist at any given time.
If Python searches for a name it does in the following order:
local -> enclosing -> global -> built-in
Thats how **scope** is created.




### Special case: Interned objects

Python pre-creates a certain subset of objects in memory and keeps them in the global *namespace*.
Which depends on the implementation (e.g. CPython 3.7 pre-creates integers from -5 to 256 and strings 
with less than 20 characters that contain ASCII letters, digits or underscores only.
This way, python prevents memory allocation calls for likely and consistently used objects.
We can see this by running the following:
```python
x = 100
y = 100
y is x
z = 90 + 10
z is x
```
All of these return `True, because the object `100` is a *interned object*.
This:
```python
x = 1000000
y = 1000000
x is y
```
would return False, as the value `1000000`is not interned. Here, a new object would be created.

> NOTE: If you are using VSCode to check this, you might get different results. Try using the Python Terminal itself.
<!-- Why is that? -->
<!-- if i assign a name to a immutable object which already exists at a memory location it seems to be retrieved in VSCode --> 


## Pass by assignement<sub><sup><sup>[[py]](pass_by_assignement.py)</sup></sup></sup>

**Pass:** Provide argument to a function  

**Pass by reference:** argument is a reference to a variable that already exists in memory

**Pass by value:** argument becomes independent copy of original value

**Pass by assignement**:
```python
def main():
    x = 100
    print(f"Initial adress of x: {id(x)}")
    increment(x)
    print(f"Final adress of x: {id(x)}")

def increment(y):
    print(f"Initial adress of y: {id(y)}")
    y += 1
    print(f"Final adress of y: {id(y)}")

main()
```
This shows that the memory adress of `y` inside the `increment` function is initially the same as for `x`.
One could maybe think of `y` as initially being `y = x` so `y is x`.
Only after incrementing `y` the adress changes, since a new `PyObject` is created
(as integers are immutable, `101` is created at a new adress). Therefore `y = x` is overridden with `y = 101`
After the `increment` function is terminated, the local `y` name is cleaned up and only the global `x` name is adressed 
(which of course has the same adress as before).


### Pass by reference in Python

So how do you pass by reference in Python? Easy, just return one or multiple arguments.
```python
def main()
    x = 0
    s, x = f("Hello", x)
    print(f"{s} {x}")
    s, x = f("Hello", x)
    print(f"{s} {x}")

def f(a, x): 
    return f"{a} World!", x+1

main()
```
Multiple values are returned as a **tuple** by default but can also be returned as a list or dict by enclosing in `[]` or `{}`, respectively.


## Returning values<sub><sup><sup>[[py]](return_values.py)</sup></sup></sup>

### Generators

Any function containing `yield` is a generator function. (Pythons bytecode compiler detects this and compiles the function specially)
Generators are used if resources of a function become too large. They are kind of a "resumable function", meaning they resumes where they left of.
On reaching `yield` the generators state of execution is suspended and local variables are preserved. In the next call to the generator, its `__next__` method is called and resumes the function. (`__next__` is called implicitly by a for loop, see example)  
Generator functions return a generator object that supports the iterator protocol (instead of a single value like with `return`).

### Walruses
A new feature in Python [3.8](https://docs.python.org/3/whatsnew/3.8.html) to assign variables within expressions. It looks like a walrus `:=`.

## Starting a new project in VSCode

In Terminal:  
`mkdir directory_name` > `cd directory_name` > `code .`  
(or in GUI: **File** > **Open Folder**)  

Select Python Interpreter: `Ctr+Shift+P` > **Python: Select Interpreter**

### Virtual environment

By default, the Python interpreter runs in its global environment. Packages installed always land there, making it too crowded over time. A **Virtual environments** is a folder containing a copy (symlink) of the interpreter. Any packages are installed only in that subfolder.  

GUI: `Ctrl+Shift+P` > **Python: Create Environment** > **Venv**  
Terminal: `python -m venv .venv`  

Select "Yes" in Prompt.  

Terminal: `.venv\scripts\activate`  

If command genereates: "Activate.ps1 is not digitially signed. You cannot run this script on the current system." ("...kann nicht geladen werden, ...") then temporarily change PowerShell execution policy to allow scripts to run.  
You can see the current execution policy with `Get-ExecutionPolicy` and change it with `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`, then run the command and change it back.

Python Interpreter of venv should be selected.  
If not: `Ctr+Shift+P` > **Python: Select Interpreter** and choose venv one.

__Install packages:__ `pip install package` or `python [-m](https://peps.python.org/pep-0338/) pip install package`

__Create a `requirements.txt`:__ `pip freeze > requirements.txt`  
This describes packages installed, so others can easily install them with `pip install -r requirements.txt` (with this, no need to commit venv to source control)

### Enabling source control

&emsp;&emsp;&emsp;TODO

## Type hints

Since [PEP484](https://peps.python.org/pep-0484/) and PEP483 type hints are a way to annotate types. (Easier) Static analysis (analysis of source code without running it) is one benefit of these hints.  
A cheat sheet of these type hints can be found here: [Type hints cheat sheet](type_hints.py)

&emsp;&emsp;&emsp;TODO

## Interesting libraries modules

### [argparse](https://docs.python.org/3/library/argparse.html)

For implementing command-line interfaces
```python
parser = argparse.ArgumentParser(description="Test case")
parser.add_argument("-f", "--flag", default="test" help="A test flag", type="str")
args = parser.parse_args()

print(args.flag)
```

### os 

For working with the operating system.

#### Convert relative to absolute path

This can be done in many ways:
```python
dirname = os.path.dirname(__file__)
full_path = os.path.join(dirname, "relative/path/to/file")

full_path = os.path.abspath("relative/path/to/file"
```
Using absolute paths instead of relative ones ensures portability.

&emsp;&emsp;&emsp;TODO

### pytest

Library to unit test your program.
```python
import pytest
from project import square

def test_square():
    assert square(2) == 4
    assert square(3) == 9
    with pytest.raises(TypeError):
        square("2")
```
For creating a folder full of test files the folder needs an `__init__` file (can be empty), e.g.:  
`mkdir test` > `code test/__init__.py` > `code test/test_file_1` 

### [flask](https://flask.palletsprojects.com/en/2.2.x/)

```python
from flask import Flask

app = Flask(__name__)

@app.rout("/")
def hello_world():
    return "<p>Hello, World!</p>"
```
Instance of `Flask` class `app` will be WSGI application. (WSGI = Web Server Gateway Interface - Specification that describes how server and application communicate)  
Server and application Interfaces are specified in PEP 3333 which tries to standardize both so that any application written to the WSGI specification will run on any server written to the WSGI specification. It is a way to unifying the many web frameworks of Python, increasing compatibility and portability.  


### mypy

Makes sure that all variables are of the right type, by referring to your type hints.

&emsp;&emsp;&emsp;TODO

### requests

&emsp;&emsp;&emsp;TODO

## Best practices

&emsp;&emsp;&emsp;TODO

## Style guides

[PEP8](https://peps.python.org/pep-0008/) describes the Style Guide for Python.  
One thing described here is a maximum line length of 79 characters.  
> The preferred way of wrapping long lines is by using Python’s implied line continuation inside parentheses, brackets and braces. Long lines can be broken over multiple lines by wrapping expressions in parentheses.  

This could be done as follows:
```python
print (
    "This is a line break for a otherwise "
    "very long string which would be "
    "over 79 characters long"
    )
```
Since Python strings will automatically concatenate when not separated by a comma, we do not need a `+` or call `join()`.

&emsp;&emsp;&emsp;TODO <!-- see PEP8 -->

<!-- Other things: Constants capitalized, varibales snake_case, ... -->

## Miscellaneous

#### Eliminating duplicates

```python
numbers = [1,2,4,2,1,5,6,7,1,2,5]
numbers = set(numbers)
```
or
```python
numbers = [1,2,4,2,1,5,6,7,1,2,5]
numbers_set = set()
for number in numbers:
    numbers_set.append(number)
```

#### Unpacking 

Unpacking is:  
`x, y, z = [1, 2, 3]`  
But there are other ways to do so:

`*` unpacks a variable
```python
def total(first, second, third):
    return (first * 11 + second) * 22 + third

values = [10, 5, 3]

print(total(*values))
```
or
```python
list = ["Hi", "I", "am", "a", "list"]
print(*list)
```
If passing the variables in different orders is necessary one could use dictionaries as follows:
```python
def total(first, second, third):
    return (first * 11 + second) * 22 + third

values = {"first": 10, "second": 5, "third": 3}

print(total(**values)
```
Unpacking dictonaries provides both keys and values. One could think of the `**values` 
above being passed to total like `total(first=10, second=5, third=3)`

#### Accepting multiple arguments

In contrast to unpacking, one could also use the same syntax to let a function accept multiple values:  
`def function(*args, **kwargs)`  
with `*args` for accepting multiple positional arguments and `**kwargs` for accepting multiple named arguments.

#### Positional-only and Keyword-only arguments

Positional-only arguments come before a `/`.  
Keyword-only arguments come after a `*`.  
If none of these two are present inside the function definition,
arguments may be passed by position or keyword.
```python
def f(x_pos, /, x_both, *, x_kwd):
  pass
```
Calling the function with `f(x_pos=1, 2, x_kwd=3)`
would give us an error. Same as calling the function
with `f(1, 2, 3)`. The following two calls would be
valid: `f(1, 2, x_kwd=3)` and `f(1, x_both=2, x_kwd=3)`.

<!-- 
Notes:
add two or more spaces after text to get a linebreak 
-->
