import os
import threading
import time

import pytest
from fastapi.testclient import TestClient

from capstone_app.api import app


# ----------------------------
# Common / API fixtures
# ----------------------------

@pytest.fixture(scope="session")
def api_client():
    """FastAPI TestClient (in-process) for API tests."""
    return TestClient(app)


# ----------------------------
# UI test server fixture
# ----------------------------

@pytest.fixture(scope="session")
def live_server_url():
    """
    Starts a local Uvicorn server in a background thread for Playwright UI tests.
    Uses an ephemeral port picked by uvicorn. Returns the base URL.
    """
    import socket
    import uvicorn

    # pick a free port
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    host, port = sock.getsockname()
    sock.close()

    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
    server = uvicorn.Server(config=config)

    t = threading.Thread(target=server.run, daemon=True)
    t.start()

    # wait for startup
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            import httpx
            r = httpx.get(f"http://127.0.0.1:{port}/health", timeout=0.5)
            if r.status_code == 200:
                break
        except Exception:
            time.sleep(0.1)

    yield f"http://127.0.0.1:{port}"

    server.should_exit = True
