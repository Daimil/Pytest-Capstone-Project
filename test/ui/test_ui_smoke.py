
import pytest

@pytest.mark.ui
def test_checkout_ui_smoke(page, live_server_url):
    # open app
    page.goto(live_server_url + "/")

    # Set inputs (testid selectors are stable)
    page.get_by_test_id("coupon").select_option("SAVE20")
    page.get_by_test_id("state").select_option("NY")
    page.get_by_test_id("qty").fill("2")
    page.get_by_test_id("price").fill("60")

    page.get_by_test_id("run").click()

    # Assert outcome: total should exist and include discounted 96.00
    out = page.get_by_test_id("out")
    out.wait_for()
    txt = out.inner_text()
    assert '"discounted": "96.00"' in txt
