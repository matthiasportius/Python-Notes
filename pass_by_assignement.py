# you just override the values with another assignement like x += 1 because thats how 
# python works, as seeable with id()
# pass: provide argument to a function
# by reference: argument is a reference to a variable that already exists in memory
# How do you pass by reference in python? 
# Just return 1 or multiple arguments
def main():
    counter = 0
    greeting, counter = greet("Alice", counter)
    print(f"{greeting}\nCounter is {counter}")
    greeting, counter = greet("Bob", counter)
    print(f"{greeting}\nCounter is {counter}")

def greet(name, counter):
    # returned as tuple by default
    return f"Hi, {name}!", counter+1

# by value: argument becomes independent copy of original value
# by assignement:

def main() -> None:
    n = 100
    print(f"Initial adress of n: {id(n)}")
    increment(n)
    print(f"   Final adress of n: {id(n)}")

def increment(x: int) -> None:
    # x is same as n, x is a variable to which the value of n (at its memory location) is assigned
    print(f"Initial adress of x: {id(x)}")
    x += 1
    # x is different from n after reassignement, x is re-bound to the new value (which is different memory location)
    print(f"   Final adress of x: {id(x)}")


if __name__ == "__main__":
    main()


# if i do x = 2 and a memory location with value 2 (the "object") already exists
# then its retrieved, otherwise its created
# "object", because everythin in python is an object
# each object contains three types of date: reference count, type, value
# the "reference counter" of this object is incremented
# (reference counter: how many references/names point to same object)
