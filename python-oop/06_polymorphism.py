"""Polymorphism: one function can work with many compatible objects."""

from typing import Protocol


class Speaker(Protocol):
    name: str

    def speak(self) -> str: ...


class Dog:
    def __init__(self, name: str) -> None:
        self.name = name

    def speak(self) -> str:
        return f"{self.name} says woof!"


class Cat:
    def __init__(self, name: str) -> None:
        self.name = name

    def speak(self) -> str:
        return f"{self.name} says meow!"


def announce(animal: Speaker) -> None:
    print(animal.speak())


def main() -> None:
    for animal in (Dog("Buddy"), Cat("Whiskers")):
        announce(animal)


if __name__ == "__main__":
    main()
