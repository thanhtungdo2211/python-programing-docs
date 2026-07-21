"""Instance attributes, class attributes, class methods, and static methods."""


class Employee:
    company_name = "TechCorp"
    _employee_count = 0

    def __init__(self, name: str, role: str, salary: int) -> None:
        if salary < 0:
            raise ValueError("salary cannot be negative")
        self.name = name
        self.role = role
        self.salary = salary
        type(self)._employee_count += 1

    def summary(self) -> str:
        return f"{self.name} ({self.role}) earns ${self.salary:,}."

    @classmethod
    def company_summary(cls) -> str:
        return f"{cls.company_name} employs {cls._employee_count} people."

    @staticmethod
    def is_high_salary(salary: int, threshold: int = 50_000) -> bool:
        return salary > threshold


def main() -> None:
    employees = (Employee("Alice", "Developer", 70_000), Employee("Bob", "Designer", 45_000))
    for employee in employees:
        print(employee.summary())
        print(f"High salary: {Employee.is_high_salary(employee.salary)}")
    print(Employee.company_summary())


if __name__ == "__main__":
    main()
