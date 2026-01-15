
import pytest

@pytest.mark.api
def test_health(api_client):
    r = api_client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


@pytest.mark.api
def test_checkout_save20_requires_threshold(api_client):
    payload = {
        "coupon": "SAVE20",
        "state": "NY",
        "items": [{"sku": "SKU-1", "qty": 1, "price": "99.99"}],
    }
    r = api_client.post("/checkout", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["discounted"] == "99.99"


@pytest.mark.api
def test_checkout_save20_applies_over_100(api_client):
    payload = {
        "coupon": "SAVE20",
        "state": "NY",
        "items": [{"sku": "SKU-1", "qty": 2, "price": "60.00"}],
    }
    r = api_client.post("/checkout", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["subtotal"] == "120.00"
    assert data["discounted"] == "96.00"
