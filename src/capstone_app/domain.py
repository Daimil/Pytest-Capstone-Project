from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable


class DomainError(ValueError):
    pass


@dataclass(frozen=True)
class LineItem:
    sku: str
    qty: int
    price: Decimal


def subtotal(items: Iterable[LineItem]) -> Decimal:
    total = Decimal("0")
    for it in items:
        if it.qty <= 0:
            raise DomainError("qty must be positive")
        if it.price < 0:
            raise DomainError("price must be non-negative")
        total += (it.price * Decimal(it.qty))
    return total


def apply_discount(total: Decimal, *, coupon: str | None) -> Decimal:
    """Business rule:
    - 'SAVE10' => 10% off
    - 'SAVE20' => 20% off, only if total >= 100
    - None/unknown => no discount
    """
    if coupon is None:
        return total

    coupon = coupon.strip().upper()
    if coupon == "SAVE10":
        return (total * Decimal("0.90")).quantize(Decimal("0.01"))
    if coupon == "SAVE20":
        if total >= Decimal("100"):
            return (total * Decimal("0.80")).quantize(Decimal("0.01"))
        return total
    return total


def total_with_tax(total: Decimal, *, state: str) -> Decimal:
    state = state.upper().strip()
    if state == "NY":
        rate = Decimal("0.08875")
    elif state == "CA":
        rate = Decimal("0.0725")
    else:
        rate = Decimal("0.05")

    return (total * (Decimal("1.0") + rate)).quantize(Decimal("0.01"))
