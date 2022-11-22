# yield only returns one value at a time
def main():
    n = int(input("Enter a number: "))
    # implicitly calls __next__ of generator
    for s in count(n):
        print(s)

    walrus()


def count(n):
    for i in range(n):
        yield "🐑" * i


# assign variables within expressions
def walrus():
    print(w := "walrus")
    print("The variable can be used again, see:", w)


if __name__ == "__main__":
    main()
