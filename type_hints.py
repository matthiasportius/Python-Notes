from typing import Final
x: int = 1
x: float = 1.0
x: str = "1"
x: bool = True
CONSTX: Final[int] = 3  # constant (readonly) variable


x: list[int] = [1]
x: set[int] ={1, 2}
x: dict[str, float] = {"one": 1.0}
x: tuple[int, str, float] = (1, "one", 1.0)  # tuple of fixed size
x: tuple[int, ...] = (1, 1, 1)  # tuple of variable size

# On Python 3.8 and earlier:
from typing import List, Set, Dict, Tuple
x: List[int] = [1]
x: Set[int] = {1, 2}
x: Dict[str, float] = {"one": 1.0}
x: Tuple[int, str, float] = (1, "1", 1.0)
x: Tuple[int, ...] = (1, 1, 1)


# If multiple types are possible use "|"
from typing import Union
x: list[int | str] = [1, "1", "1"]

# Before Python 3.10:
x: list[Union[int, str]] = [1, "one", "one"]


# If a value could also be None use Optional
# Optional is same as X | None or Union[X | None]
from typing import Optional
x: Optional[str] = 1 if ... else None


# Functions
def f(x: int = 1, y: str = "1") -> str:
    return str(x) + y

def f(a: Union[str, list[str]],
      b: Optional[list[str]],
      c: str,
      d: bool,
      e: int
      ) -> bool:
    ...

from typing import Callable
x: Callable[[int, str], str] = f

# generator function yielding ints is just a function 
# returning an iterator of ints:
from typing import Iterator
def f(x: int) -> Iterator[int]:
    for i in range(x):
        yield i

# if each positional arg and keyword arg is an int:
def f(*args: int, **kwargs: int) -> int:
    pass


# Classes
from typing import ClassVar
class C:
    c_attr: ClassVar[int] = 2       # class variable

    def __init__(self, x: int, s: str) -> None:
        self.l: list[int, str] = [x, s]  # instance variable

x: C = C()


# if type is not known or is dynamic
from typing import Any
x: Any = []
x = 1
x = "1"
