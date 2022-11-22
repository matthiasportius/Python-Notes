import sys

# proof that everything in Python is an object:
class EverythingIsObject():
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


EverythingIsObject.test()



class ModifyObjects():
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


ModifyObjects.modify_immutable()
ModifyObjects.modify_mutable()


# Why does that not work in VSCode but in the Python Terminal?
class InternedObjects():
    x = 100
    y = 100
    a = 1000000
    b = 1000000

    @classmethod
    def test(cls):
        print(f"x = 100 {'is' if cls.x is cls.y else 'is not'} y = 100")
        print(f"a = 1000000 {'is' if cls.a is cls.b else 'is not'} y = 1000000")


InternedObjects.test()


# NAMESPACES
dir(__builtins__)
globals()  
locals()


class RefCount():
    def refcount():
        x = 5
        print(f"x = 5, refcount={sys.getrefcount(x)}")
        y = x
        print(f"y = x, refcount={sys.getrefcount(x)}")

RefCount.refcount()
