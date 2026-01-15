from __future__ import annotations

from decimal import Decimal
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from .domain import LineItem, subtotal, apply_discount, total_with_tax

app = FastAPI(title="Pytest Capstone App")


class CheckoutItem(BaseModel):
    sku: str
    qty: int = Field(ge=1)
    price: Decimal = Field(ge=0)


class CheckoutRequest(BaseModel):
    items: list[CheckoutItem]
    coupon: str | None = None
    state: str = "NY"


class CheckoutResponse(BaseModel):
    subtotal: Decimal
    discounted: Decimal
    total: Decimal


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/checkout", response_model=CheckoutResponse)
def checkout(req: CheckoutRequest):
    items = [LineItem(sku=i.sku, qty=i.qty, price=i.price) for i in req.items]
    st = subtotal(items)
    discounted = apply_discount(st, coupon=req.coupon)
    total = total_with_tax(discounted, state=req.state)
    return CheckoutResponse(subtotal=st, discounted=discounted, total=total)


@app.get("/", response_class=HTMLResponse)
def home():
    html = Path(__file__).resolve().parents[2] / "web" / "index.html"
    return HTMLResponse(html.read_text(encoding="utf-8"))
