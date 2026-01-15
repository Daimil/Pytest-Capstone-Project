
import pytest

@pytest.mark.perf
def test_checkout_endpoint_benchmark(benchmark, api_client):
    payload = {
        "coupon": "SAVE10",
        "state": "NY",
        "items": [{"sku": "SKU-1", "qty": 2, "price": "60.00"}],
    }

    def run():
        r = api_client.post("/checkout", json=payload)
        assert r.status_code == 200

    benchmark(run)
