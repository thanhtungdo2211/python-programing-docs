"""Managed attributes with properties and explicit domain operations."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


class Percentage:
    """A reusable descriptor that validates percentage attributes."""

    def __set_name__(self, owner: type, name: str) -> None:
        self._storage_name = f"_{name}"

    def __get__(self, instance: object | None, owner: type | None = None) -> float | Percentage:
        if instance is None:
            return self
        return getattr(instance, self._storage_name)

    def __set__(self, instance: object, value: float) -> None:
        if not 0.0 <= value <= 100.0:
            raise ValueError("percentage must be between 0 and 100")
        setattr(instance, self._storage_name, float(value))


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "USD"

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("money cannot be negative")


class Product:
    discount = Percentage()

    def __init__(self, name: str, price: Money, discount: float = 0.0) -> None:
        self.name = name
        self._price = price
        self.discount = discount

    @property
    def price(self) -> Money:
        """Expose price as read-only; changes go through a named operation."""
        return self._price

    @property
    def sale_price(self) -> Money:
        multiplier = Decimal("1") - Decimal(str(self.discount / 100))
        return Money((self.price.amount * multiplier).quantize(Decimal("0.01")), self.price.currency)

    def change_price(self, new_price: Money) -> None:
        """An explicit operation is clearer than a setter when rules may grow."""
        self._price = new_price


def main() -> None:
    product = Product("Mechanical keyboard", Money(Decimal("120.00")), discount=15)
    print(f"List price: {product.price.amount} {product.price.currency}")
    print(f"Sale price: {product.sale_price.amount} {product.sale_price.currency}")


if __name__ == "__main__":
    main()
