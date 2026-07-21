"""Abstract base classes provide an explicit interface for implementations."""

from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    @abstractmethod
    def charge(self, amount: int) -> str:
        """Charge an amount and return a transaction ID."""

    @abstractmethod
    def refund(self, transaction_id: str, amount: int) -> bool:
        """Refund part or all of a transaction."""


class CreditCardProcessor(PaymentProcessor):
    def charge(self, amount: int) -> str:
        return f"CC-{amount}"

    def refund(self, transaction_id: str, amount: int) -> bool:
        print(f"Refunded ${amount:,} from {transaction_id}.")
        return True


class PayPalProcessor(PaymentProcessor):
    def charge(self, amount: int) -> str:
        return f"PAYPAL-{amount}"

    def refund(self, transaction_id: str, amount: int) -> bool:
        print(f"Refunded ${amount:,} from {transaction_id}.")
        return True


def checkout(total: int, processor: PaymentProcessor) -> str:
    transaction_id = processor.charge(total)
    print(f"Payment approved: {transaction_id}")
    return transaction_id


def main() -> None:
    transaction = checkout(500, CreditCardProcessor())
    CreditCardProcessor().refund(transaction, 100)


if __name__ == "__main__":
    main()
