<!-- Add links to relevant .py files as crossreff to headers -->
# Python-Notes

This repository is a collection of intermediate Python concepts which I am currently studying.
It shall provide a succinct compilation of (in my mind) important concepts and features
of the programming language Python.


## The Zen of Python

If in doubt at any point, always remember the **Zen of Python**.
Just [`import this`](https://peps.python.org/pep-0020/).
You are of course also free to use this [file](zen_of_python.py).


## Pythons object model

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

Actually the underlying implementation of variables and such is a [**`PyObject`**](https://stackoverflow.com/a/27683778),
which is also why Python has no pointers like C.
Each of these objects contains at least **three types of data**:
* reference count
* type
* value
<!-- Add schema of a PyObject with its name here -->


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
When I do: `x = 1` these steps are performed:
1. Create a [`PyObject`](https://docs.python.org/3/c-api/structures.html#c.PyObject) in C (as a C `struct`)
2. Set the type of the `PyObject` to integer
3. Set the value of the `PyObject` to `1`
4. Create a *name* called `x`
5. Point `x` to the new `PyObject`
6. Increase the reference count of the `PyObject`by 1

So `x` is only a *name* pointing to the "real" object with type, value and refcount.
That means `x` does not directly "own" any memory adress like a variable in C.
The PyObject does.

So what happens when I re-assign the variable `x = 3` is:
1. Create a new PyObject
2. Set the type of the `PyObject` to integer
3. Set the value of the `PyObject` to `3`
4. Point the *name* `x` to the new PyObject
5. Increase the reference count of the new `PyObject`by 1
6. Decrease the reference count of the old `PyObject`by 1
   * If the reference count is 0 the object gets cleaned up by the garbage collector

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

NOTE: If you are using VSCode to check this, you might get different results. Try using the Python Terminal itself.
<!-- Why is that? -->
<!-- if i assign a name to a immutable object which already exists at a memory location it seems to be retrieved in VSCode --> 


## Pass by assignement

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

So how do you pass by reference in Python? Easy, just return one or multiple arguments (default: returned as tuple, but also list or dict possible). 
```python
def main()
    x = 0
    s, x = f("Hello", x)
    print(f"{s} {x}")
    s, x = f("Hello", x)
    print(f"{s} {x}")

def f(a, x): 
    return f"{a} World!", x+1
```


## Pythons object model

**bold text** __bold text__
*italic* _italic_
~~strikethrough~~
<sub>Subscript</sub>
<sup>Superscript</sup>
> Quoted text
`code` or `command`
```
code block
```
[inline link](URL) e.g. (object_model.py)
* unordered list item 1
* 2
* 3

1. ordered list item 1
   * unordered 1.1
     * unordered 1.1.1
2. 2
3. 3


## Returning values
