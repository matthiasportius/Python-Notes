<!-- Just a test comment -->
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

There are **two types of objects**:
* mutable
  * list, set, dict
* immutable
  * int, str, bool, ...

If you try to modify immutable objects you get a new objects. This can be easily shown
via the [`id()`](https://docs.python.org/3/library/functions.html#id)
function which returns the identity of an object (adress of the object in memory).
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

For mutable objects the identity stays the same, as can be tested with:
```python
l = [1, 2, 3]
print(l, id(l))

l.append(4)
print(l, id(l))
```

Actually the underlying implementation of variables and such is a `PyObject`.
In short: [What is a `PyObject`?](https://stackoverflow.com/a/27683778)

Each of these objects contains at least **three types of data**:
* reference count
* type
* value


### Namespaces

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
which checks if two names refer to the same object: `y is x` returns `True`


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


## Pass by assignement


## Returning values
