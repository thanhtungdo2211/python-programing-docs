"""Single, hierarchical, and multilevel inheritance."""

from dataclasses import dataclass


@dataclass
class Person:
    name: str
    age: int

    @classmethod
    def from_birth_year(cls, name: str, birth_year: int, current_year: int = 2026):
        return cls(name, current_year - birth_year)

    def describe(self) -> str:
        return f"{self.name}, age {self.age}"


@dataclass
class Employee(Person):
    employee_id: str = ""
    role: str = ""

    def describe(self) -> str:
        return f"{super().describe()}, employee {self.employee_id}, {self.role}"


@dataclass
class Manager(Employee):
    department: str = ""

    def describe(self) -> str:
        return f"{super().describe()}, manages {self.department}"


@dataclass
class Student(Person):
    student_id: str = ""
    major: str = ""

    def describe(self) -> str:
        return f"{super().describe()}, student {self.student_id}, {self.major}"


def main() -> None:
    people: list[Person] = [
        Employee("Alice", 30, "E-123", "Developer"),
        Manager("Morgan", 35, "M-456", "Engineering Manager", "Engineering"),
        Student("Sam", 21, "S-789", "Mathematics"),
    ]
    for person in people:
        print(person.describe())


if __name__ == "__main__":
    main()
