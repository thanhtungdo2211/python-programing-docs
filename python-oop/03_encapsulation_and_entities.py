"""Encapsulation with properties and identity-based entity equality."""

from dataclasses import dataclass


@dataclass(eq=False)
class User:
    """A user is identified by ID, even when other fields change."""

    user_id: int
    name: str
    _email: str

    @property
    def email(self) -> str:
        return self._email

    def change_email(self, new_email: str) -> None:
        if "@" not in new_email:
            raise ValueError("email must contain '@'")
        self._email = new_email

    def __eq__(self, other: object) -> bool:
        return isinstance(other, User) and self.user_id == other.user_id

    def __hash__(self) -> int:
        return hash(self.user_id)


def main() -> None:
    first = User(1, "Alex", "alex@example.com")
    same_identity = User(1, "Alex Updated", "new@example.com")
    print(first == same_identity)
    first.change_email("alex.updated@example.com")
    print(first.email)


if __name__ == "__main__":
    main()
