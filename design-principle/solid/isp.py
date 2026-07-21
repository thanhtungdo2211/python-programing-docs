from abc import ABC, abstractmethod

# Violate Interface Segregation Principle
class Animal:
    def fly(self):
        pass

    def swim(self):
        pass

animal = Animal()
animal.fly()

# Don't violate Interface Segregation Principle
class CanFly(ABC):
    @abstractmethod
    def fly(self):
        pass

class CanSwim(ABC):
    @abstractmethod
    def swim(self):
        pass

class Bird(CanFly):
    def fly(self):
        print("Flying")

class Fish(CanSwim):
    def swim(self):
        print("Swimming")

bird = Bird()
bird.fly()
fish = Fish()
fish.swim()

"""
Không phải động vật nào cũng có thể bay và bơi, 
nên không nên ép chúng thực hiện các method này.

Tách các interface ra thành các phần nhỏ
để các lớp chỉ phải thực hiện các hành vi mà chúng cần.
"""