# python-tdd-bank-account-java

Python 3.12+ port of the [XP Dojo TDD Bank Account Kata](https://github.com/xp-dojo/tdd-bank-account-java).

> 📊 A supporting slide deck (`slides.pptx`) is available in the repository root as a workshop resource.

---

## Driving out a Bank Account with TDD

This session will be fun — that is the primary objective!  We will talk briefly
about why XP practices matter, then write code practising two of the most
fundamental ones:

1. **Test Driven Development**
2. **Pair Programming**

---

## User Requirements

1. I can **Deposit** money to accounts
2. I can **Withdraw** money from accounts
3. I can **Transfer** amounts between accounts (if I have the funds)
4. I can print out an Account **balance slip** (date, time, balance)
5. I can print a **statement** of account activity
6. I can apply **Statement filters** (deposits only, withdrawals only)

---

## Project Layout

```
python-tdd-bank-account-java/
├── pyproject.toml          # project metadata & pytest config
├── src/
│   └── bank/
│       ├── __init__.py
│       └── account.py      # ← STARTER: stub classes (raise NotImplementedError)
├── tests/
│   └── test_account.py     # ← STARTER: skipped tests — remove @skip to begin TDD
└── solution/
    ├── src/
    │   └── bank/
    │       └── account.py  # ← SOLUTION: full implementation
    └── tests/
        └── test_account.py # ← SOLUTION: complete passing tests
```

### Two-State Architecture

| Directory | Purpose |
|-----------|---------|
| `src/` + `tests/` | **Starter** — skeleton code with `NotImplementedError` stubs and `pytest.mark.skip` tests.  Remove a `skip` marker, watch the test fail, then implement just enough to turn it green. |
| `solution/` | **Instructor's walkthrough** — fully implemented logic with all tests passing. |

---

## Getting Started

### Prerequisites

* Python 3.12 or newer
* [pip](https://pip.pypa.io/) (bundled with Python)

### Install Dependencies

```bash
# From the repository root
pip install pytest
```

Or install in editable mode with dev dependencies:

```bash
pip install -e ".[dev]"
```

### Run the Starter Tests

```bash
pytest
```

All tests will be **skipped** (marked `s`) to begin with — that is intentional.
Remove the `@pytest.mark.skip` decorator from one test at a time and follow the
**Red → Green → Refactor** cycle.

### Run the Solution Tests

```bash
pytest solution/tests
```

All solution tests should pass immediately.

---

## TDD Cycle — Red → Green → Refactor

```
Red    → Write a failing test that describes the behaviour you want.
Green  → Write the simplest code that makes the test pass.
Refactor → Clean up the code without breaking the tests.
```

Repeat for every requirement.

---

## Pair Programming

Work in pairs using the **Driver–Navigator** model:

* **Driver** — writes the code, explains their thinking out loud.
* **Navigator** — observes, asks *"why?"*, and thinks about the bigger picture.

Switch roles often!

---

## Running with `pytest` — Useful Flags

| Command | Description |
|---------|-------------|
| `pytest` | Run all starter tests |
| `pytest -v` | Verbose output |
| `pytest -rs` | Show reasons for skipped tests |
| `pytest solution/tests` | Run solution tests |
| `pytest --tb=short` | Shorter tracebacks |

---

## Mutation Testing with mutmut

[mutmut](https://github.com/boxed/mutmut) automatically introduces small code mutations (e.g. flipping `>` to `>=`, changing `+` to `-`) and checks whether your tests catch each one.  A surviving mutant means a test is missing or too weak.

> **Windows note:** mutmut requires WSL on Windows.  Run all commands inside a WSL terminal.

### Install

```bash
pip install -e ".[dev]"
```

### Run

```bash
# Run all mutations against all tests
mutmut run

# Quick run — stop on first surviving mutant
mutmut run --use-coverage
```

### View results

```bash
# Summary: how many mutants killed vs survived
mutmut results

# Show the diff for all surviving mutants
mutmut show

# Show a specific surviving mutant by ID
mutmut show 42

# HTML report (opens in browser)
mutmut html
```

### Configuration

mutmut is pre-configured in `pyproject.toml`:

```toml
[tool.mutmut]
paths_to_mutate = "src/bank/"   # only mutate domain code
tests_dir       = "tests/"
runner          = "python -m pytest -x --tb=no -q"
```

### Interpreting output

| Status | Meaning |
|--------|---------|
| `killed` | ✅ A test caught the mutation — good coverage |
| `survived` | ❌ No test caught it — consider adding an assertion |
| `suspicious` | ⚠️ Test suite timed out or behaved unexpectedly |
| `skipped` | Mutation was not applied (e.g. string/comment changes) |
