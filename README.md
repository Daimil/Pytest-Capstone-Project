# Pytest Capstone Project (API + UI + Performance + Mutation)

This capstone is a **realistic, portfolio-quality** pytest automation project that covers:

- ✅ Unit tests (fast, deterministic)
- ✅ API tests (FastAPI TestClient; no external server required)
- ✅ UI tests (Playwright running against a local FastAPI server)
- ✅ Performance checks (pytest-benchmark for baseline/regression detection)
- ✅ Mutation testing (mutmut to evaluate test effectiveness)
- ✅ CI pipeline (GitHub Actions + markers + parallelism)

---

## 1) Prerequisites

- Python 3.11+ recommended
- pip / venv

---

## 2) Setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

pip install -r requirements.txt
playwright install
```

---

## 3) Run tests locally

### Unit tests
```bash
pytest -m unit
```

### API tests
```bash
pytest -m api
```

### UI tests (Playwright)
```bash
pytest -m ui
```

### Run everything (except slow)
```bash
pytest -m "not slow"
```

### Parallel execution
```bash
pytest -n auto -m "not slow"
```

---

## 4) Performance benchmarking (baseline + compare)

Create/refresh baseline:

```bash
pytest -m perf --benchmark-only --benchmark-save=baseline
```

Compare against baseline:

```bash
pytest -m perf --benchmark-only --benchmark-compare=baseline
```

Tip: performance tests are sensitive to machine noise. Prefer running them in CI with consistent runners.

---

## 5) Mutation testing (mutmut)

Mutation testing is expensive; run it **selectively** on business logic:

```bash
mutmut run --paths-to-mutate src/capstone_app/domain.py
mutmut results
```

Open an individual mutant:

```bash
mutmut show <mutant_id>
```

---

## 6) Project structure

```
.
├─ src/capstone_app/
│  ├─ __init__.py
│  ├─ domain.py            # core business rules (mutation target)
│  └─ api.py               # FastAPI app
├─ web/
│  └─ index.html           # tiny UI page for Playwright tests
├─ tests/
│  ├─ conftest.py
│  ├─ unit/
│  ├─ api/
│  ├─ ui/
│  └─ performance/
├─ pytest.ini
├─ requirements.txt
└─ .github/workflows/ci.yml
```

---

## 7) How this capstone demonstrates advanced automation

- **Signal over noise**: markers split test types and keep CI fast.
- **Isolation**: clean fixtures; no shared state.
- **Stability**: UI tests use role/testid selectors and avoid sleeps.
- **Quality gates**: performance checks + (optional) mutation testing.
- **Scale**: xdist parallelism is ready out-of-the-box.

---

## 8) Next upgrade ideas

- Add contract tests (OpenAPI schema validation)
- Add snapshot testing for API responses
- Add Allure reporting
- Add docker-compose dependency simulation for resilience tests
