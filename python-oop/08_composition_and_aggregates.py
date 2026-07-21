"""Composition: an order owns its line items and protects its invariants."""

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum


class OrderStatus(Enum):
    CREATED = "created"
    SUBMITTED = "submitted"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class OrderItem:
    product_id: str
    quantity: int
    unit_price: Decimal

    @property
    def subtotal(self) -> Decimal:
        return self.unit_price * self.quantity


@dataclass
class Order:
    order_id: str
    customer_id: str
    _items: list[OrderItem] = field(default_factory=list, repr=False)
    _status: OrderStatus = field(default=OrderStatus.CREATED, repr=False)

    @property
    def items(self) -> tuple[OrderItem, ...]:
        return tuple(self._items)

    @property
    def status(self) -> OrderStatus:
        return self._status

    @property
    def total(self) -> Decimal:
        return sum((item.subtotal for item in self._items), Decimal("0"))

    def add_item(self, product_id: str, quantity: int, unit_price: Decimal) -> None:
        if self._status is not OrderStatus.CREATED:
            raise ValueError("only new orders can be changed")
        if quantity <= 0 or unit_price < 0:
            raise ValueError("quantity must be positive and price cannot be negative")
        self._items.append(OrderItem(product_id, quantity, unit_price))

    def submit(self) -> None:
        if not self._items:
            raise ValueError("an order must contain at least one item")
        self._status = OrderStatus.SUBMITTED


def main() -> None:
    order = Order("ORD-1", "CUST-123")
    order.add_item("BOOK", 2, Decimal("12.50"))
    order.add_item("PEN", 1, Decimal("2.00"))
    print(f"Order total: ${order.total:.2f}")
    order.submit()
    print(f"Status: {order.status.value}")


if __name__ == "__main__":
    main()
