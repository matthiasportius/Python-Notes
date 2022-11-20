def main() -> None:
# ---Pass by assignement:---
    n = 100
    print(f"Initial adress of n: {id(n)}")
    increment(n)
    print(f"   Final adress of n: {id(n)}")

# ---"Pass by reference"---
    counter = 0
    greeting, counter = greet("Alice", counter)
    print(f"{greeting}\nCounter is {counter}")
    greeting, counter = greet("Bob", counter)
    print(f"{greeting}\nCounter is {counter}")

# ---Pass by assignement:---
def increment(x: int) -> None:
    # x is same as n, x is a variable to which the value of n (at its memory location) is assigned
    print(f"Initial adress of x: {id(x)}")
    x += 1
    # x is different from n after reassignement, x is re-bound to the new value (which is different memory location)
    print(f"   Final adress of x: {id(x)}")

# ---"Pass by reference"---
def greet(name, counter):
    # returned as tuple by default
    return f"Hi, {name}!", counter+1


if __name__ == "__main__":
    main()
