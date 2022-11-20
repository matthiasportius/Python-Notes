# python has no pointers (=variables that hold memory adresses of another variable)
# Pythons object model: everythin in python is an object
# proof:
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

# each object contains at least three types of data: reference count, type, value
# there are two types of objects: mutable(list, set, dict) and immutable
x = 5
s = "hi"
print(x, id(x))
print(s, id(s))
# if you try to modify immutable objects (like int or str) you get new object
x += 1
s += "world"
print(x, id(x))
print(s, id(s))
# this also shows when directly modifying immutable objects like str:
try:
    s[0] = "A"
except TypeError:
    print("str is immutable")

# for mutable objects the id stays the same:
l = [1, 2, 3]
print(l, id(l))
l.append(4)
l[0] = 0
print(l, id(l))

# in python one does not create "variables" but "names"
# what does this mean?
# when i do:
x = 1
# i do these steps:
# 1 create a PyObject in C (as a C struct)
# 2 Set the typecode to integer for the PyObject
# 3 set value to 1 for the PyObject
# 4 create a "name" called "x"
# point x to the new PyObject
# increase  the refcount of the PyObject by 1

# so x is only a "name" pointing to the real object with type, value and refcount
# so x does not directly "own" any memory adress like variables in C, the PyObject does
# so when I do this:
x = 3
# then I do:
# 1 create a new PyObject
# 2 Set the typecode to integer for the PyObject
# 3 set value to 3 for the PyObject
# 4 point x to the new PyObject
# 5 increase  the refcount of the new PyObject by 1
# 6 decrease  the refcount of the old PyObject by 1 (if ref count is 0 it gets cleaned up by the garbage collector)
y = x
# this would not create a new objectm just a new name that points to the
# existing PyObject, increasing its refcount by 1
# is checks if these two refer to the same object:
y is x  # returns True

# interned objects: Python pre-creates a certain subset of objexts in memory 
# and keps them in the global namespace to use
# which objects depends on implementation of Python
# e.g. CPython 3.7: integers from -5 to 256 and
# strings with less than 20 characters that contain ASCII ketters, digits or underscores only
# this way python prevents memory allocation calls for likely and consistently used objects
# best friends: id() and is to check equality!
x = 100
y = 100
x is y  # returns True
z = 90 + 10
x is z  # returns True also

# (to get something like a pointer (something pointing at same memory location)
# one can use mutable objects like dicts or lists
# one way to get mutable objects is also via creation of a class
# with properties the values of the class can be accessed) -> maybe not so important

# NAMESPACES
# in step for previously, the assignement statement x = 1 creates
# a symbolic name "x" which can be used to reference the PyObject
# such names are collected in the "namespace" together with their reference objects
# it is a dictionary with keys (object names) and values (objects themselve)
# 4 types of namespaces: built-in, global, enclosing, local with different lifetimes
# many namespaces will exist at any given time
# built in namespace: names of all of Pythons built-in objects
# are always available when Python is running
# until interpreter terminates
# listeable with:
# dir(__builtins__)
# global namespace: all names defined at level of main program (created when main is started)
# also created for any module that program loads with import
# until interpreter terminates
# local namespace: local to a function, created when function executes
# enclosing namespace: in the enclosing function
# until function terminates
# if Python searches for a name it does in following order in namespaces:
# local -> enclosing -> global -> built-in (thats how concept of scope is created)
# namespaces are really implemented as a dictionary:
globals()  # reference to current global namespace
locals()  # same as globals but for local namespace

# sys.getrefcount("1") shows how assignement of x icreases and decreases count 

# function arguments in python are local variables assigned to each value that 
# was passes to the function
# you just override them with another assignement like x += 1 because thats how 
# python works, as seeable with id()
# once the local space of the function is exited, the x of the global namespace
# is used again and the x of the function is deleted


