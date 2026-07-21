"""The basics: define a class, create objects, and call methods."""

from dataclasses import dataclass


@dataclass
class Dog:
    """A small immutable-data example with a behavior method."""

    name: str
    species: str = "dog"

    def speak(self) -> str:
        return f"{self.name} says woof!"


def main() -> None:
    for dog in (Dog("Rex"), Dog("Luna")):
        print(f"{dog.name} is a {dog.species}.")
        print(dog.speak())


if __name__ == "__main__":
    main()
