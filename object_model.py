# python has no pointers (=variables that hold memory adresses of another variable)

# proof that everything in Python is an object:
class Everything_is_objects():
    @staticmethod
    def foo():
        pass

    @classmethod
    def test(cls):
        # int, bool, list, str, function are all objects in Python!
        l = [1, True, list(), "Hello", cls.foo]

        for o in l:
            print(f"{o} is an {'object' if isinstance(o, object) else 'not an object'}")
        print(end="\n"*2)


Everything_is_objects.test()



class Modify_objects():
    x = 5
    s = "hi"

    # if you try to modify immutable objects (like int or str) you get new objects
    def modify_immutable():    
        x = 5
        s = "hi"
        print("----Before modification----")
        print(f"The adress of x is", id(x))
        print(f"The adress of s is", id(s))
        print()

        x += 1
        s += "world"
        print("----After modification----")
        print(f"The adress of x is", id(x))
        print(f"The adress of s is", id(s), end="\n"*2)

        # immutable objects can therefore not be modifyed
        try:
            s[0] = "A"
        except TypeError:
            print("str is immutable", end="\n"*2)
        print()

    # for mutable objects the id stays the same:
    def modify_mutable():
        l = [1, 2, 3]
        print("----Before modification----")
        print("The id of l is", id(l), end="\n"*2)
        l.append(4)
        l[0] = 0
        print("----After modification----")
        print("The if of l is", id(l), end="\n"*2)
        print()


Modify_objects.modify_immutable()
Modify_objects.modify_mutable()


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


