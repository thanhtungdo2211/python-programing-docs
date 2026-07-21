from abc import ABC, abstractmethod

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

# Violate Open-Closed Principle
class Discount:
    def apply_discount(self, product, discount_type):
        if discount_type == 'percentage':
            return product.price * 0.9
        elif discount_type == 'fixed':
            return product.price - 10

discount = Discount()
product = Product('Keyboard', 100)
print(discount.apply_discount(product, 'percentage'))
print(discount.apply_discount(product, 'fixed'))

# Don't violate Open-Closed Principle

class Discount(ABC):
    """
    @abstractmethod là một decorator trong Python được sử dụng để đánh dấu 
    một phương thức trong một lớp trừu tượng (abstract class) là phương thức trừu tượng.
    Điều này có nghĩa là phương thức này phải được triển khai (override) trong các lớp con của lớp trừu tượng đó.
    Nếu một lớp con không triển khai phương thức trừu tượng này, Python sẽ không cho phép tạo đối tượng từ lớp con đó.
    """
    @abstractmethod
    def apply_discount(self, product):
        pass

class PercentageDiscount(Discount):
    def apply_discount(self, product):
        return product.price * 0.9

class FixedDiscount(Discount):
    def apply_discount(self, product):
        return product.price - 10

discount = PercentageDiscount()
product = Product('Keyboard', 100)
print(discount.apply_discount(product))

"""
Trong ví dụ vi phạm, khi thêm một loại chiết khấu mới, phải sửa đổi lớp Discount, vi phạm OCP.

Bằng cách sử dụng kế thừa, 
có thể mở rộng thêm loại chiết khấu mà không cần sửa đổi lớp Discount.
"""