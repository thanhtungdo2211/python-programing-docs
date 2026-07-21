"""Cooperative multiple inheritance using mixins and ``super()``."""


class AudibleMixin:
    def make_sound(self) -> str:
        return "woof"


class OwnedMixin:
    def __init__(self, owner: str, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.owner = owner


class Dog(AudibleMixin, OwnedMixin):
    def __init__(self, name: str, owner: str, breed: str) -> None:
        super().__init__(owner=owner)
        self.name = name
        self.breed = breed

    def describe(self) -> str:
        return f"{self.name} is a {self.breed} owned by {self.owner}."


def main() -> None:
    dog = Dog("Buddy", "Alice", "Golden Retriever")
    print(dog.describe())
    print(f"It says {dog.make_sound()}.")


if __name__ == "__main__":
    main()
