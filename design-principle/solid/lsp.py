from abc import ABC, abstractmethod

# Violate Liskov Substitution Principle
class Bird(ABC):
    @abstractmethod
    def move(self):
        pass

class Sparrow(Bird):
    def move(self):
        print("Flying")

class Ostrich(Bird):
    def move(self):
        print("Running")

# Violate Liskov Substitution Principle
class Bird(ABC):
    @abstractmethod
    def move(self):
        pass

class Sparrow(Bird):
    def move(self):
        print("Flying")

class Ostrich(Bird):
    def move(self):
        print("Running")

"""
Trong ví dụ sai, Ostrich không thể thay thế cho Bird vì nó không thể bay.

Thay vì ép Ostrich bay, ta tạo method move tổng quát để Ostrich có thể thực hiện hành vi chạy.

"""