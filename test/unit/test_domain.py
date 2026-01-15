
import pytest
from decimal import Decimal

from capstone_app.domain import LineItem, subtotal, apply_discount, total_with_tax, DomainError


@pytest.mark.unit
def test_subtotal_sums_line_items():
    items = [
        LineItem("A", 2, Decimal("10.00")),
        LineItem("B", 1, Decimal("5.50")),
    ]
    assert subtotal(items) == Decimal("25.50")


@pytest.mark.unit
def test_subtotal_rejects_non_positive_qty():
    with pytest.raises(DomainError):
        subtotal([LineItem("A", 0, Decimal("10.00"))])


@pytest.mark.unit
@pytest.mark.parametrize(
    "total,coupon,expected",
    [
        (Decimal("100.00"), None, Decimal("100.00")),
        (Decimal("100.00"), "SAVE10", Decimal("90.00")),
        (Decimal("99.99"), "SAVE20", Decimal("99.99")),
        (Decimal("100.00"), "SAVE20", Decimal("80.00")),
    ],
)
def test_apply_discount_rules(total, coupon, expected):
    assert apply_discount(total, coupon=coupon) == expected


@pytest.mark.unit
def test_total_with_tax_by_state():
    assert total_with_tax(Decimal("100.00"), state="NY") == Decimal("108.88")
    assert total_with_tax(Decimal("100.00"), state="CA") == Decimal("107.25")
