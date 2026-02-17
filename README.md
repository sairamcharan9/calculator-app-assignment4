# Calculator App

A professional-grade, command-line calculator application built in Python with a modular architecture, interactive REPL interface, and 100% test coverage.

## Features

- **Interactive REPL** — Read-Eval-Print Loop for continuous calculations
- **Four arithmetic operations** — `add`, `subtract`, `multiply`, `divide`
- **Calculation history** — View, track, and clear past calculations
- **Robust error handling** — Combines LBYL and EAFP patterns for comprehensive input validation
- **Design patterns** — Factory and Strategy patterns for clean, extensible code
- **Decimal precision** — Uses Python's `Decimal` type for accurate arithmetic
- **100% test coverage** — Enforced via CI pipeline

## Project Structure

```
calculator-app-assignment4/
├── app/
│   ├── __init__.py               # Package docstring
│   ├── calculator/
│   │   └── __init__.py           # Calculator REPL & input processing
│   ├── calculation/
│   │   └── __init__.py           # Calculation, CalculationFactory, CalculationHistory
│   └── operation/
│       └── __init__.py           # Arithmetic functions (add, subtract, multiply, divide)
├── tests/
│   ├── __init__.py
│   ├── test_operations.py        # Unit tests for arithmetic operations
│   ├── test_calculations.py      # Unit tests for Calculation, Factory, and History
│   └── test_calculator.py        # Unit tests for Calculator REPL logic
├── .github/
│   └── workflows/
│       └── python-app.yml        # GitHub Actions CI pipeline
├── main.py                       # Application entry point
├── pytest.ini                    # Pytest configuration
├── requirements.txt              # Python dependencies
├── .gitignore
└── README.md
```

## Architecture

The application follows a modular, layered design:

| Module | Responsibility |
|---|---|
| `app.operation` | Pure arithmetic functions (`add`, `subtract`, `multiply`, `divide`) |
| `app.calculation` | `Calculation` data model, `CalculationFactory` (Factory/Strategy patterns), `CalculationHistory` |
| `app.calculator` | `Calculator` class with REPL interface, input parsing, LBYL validation, and EAFP error handling |
| `main` | Entry point that instantiates and runs the calculator |

### Design Patterns

- **Factory Pattern** — `CalculationFactory.create()` maps operation name strings to `Calculation` instances
- **Strategy Pattern** — Operations are stored as callables in a dictionary, allowing easy extension
- **LBYL** (Look Before You Leap) — Input format is validated before processing
- **EAFP** (Easier to Ask Forgiveness than Permission) — Invalid numbers and division-by-zero are caught via exception handling

## Setup

### 1. Clone the repository

```bash
git clone git@github.com:sairamcharan9/calculator-app-assignment4.git
cd calculator-app-assignment4
```

### 2. Create and activate a virtual environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Start the calculator

```bash
python main.py
```

### REPL commands

| Command | Description | Example |
|---|---|---|
| `add <a> <b>` | Addition | `add 5 3` → `5 + 3 = 8` |
| `subtract <a> <b>` | Subtraction | `subtract 10 4` → `10 - 4 = 6` |
| `multiply <a> <b>` | Multiplication | `multiply 6 7` → `6 * 7 = 42` |
| `divide <a> <b>` | Division | `divide 20 4` → `20 / 4 = 5` |
| `history` | Show calculation history | |
| `clear` | Clear calculation history | |
| `help` or `?` | Show help message | |
| `exit` | Quit the calculator | |

### Example session

```
================================
   Welcome to the Calculator!
================================
Type 'help' for available commands.
Type 'exit' to quit.

>>> add 10 5
Result: 10 + 5 = 15

>>> multiply 3 7
Result: 3 * 7 = 21

>>> divide 20 4
Result: 20 / 4 = 5

>>> history
=== Calculation History ===
  1. 10 + 5 = 15
  2. 3 * 7 = 21
  3. 20 / 4 = 5

Total: 3 calculation(s)

>>> exit
Goodbye!
```

## Running Tests

```bash
# Run all tests with verbose output
pytest

# Run tests with coverage report
pytest --cov=app

# Run tests with coverage and enforce 100% threshold
pytest --cov=app --cov-fail-under=100
```

## Continuous Integration

The project uses **GitHub Actions** (`.github/workflows/python-app.yml`) to automatically:

1. Run all tests on every push and pull request to `main`
2. Generate a coverage report
3. **Enforce 100% code coverage** — the build fails if coverage drops below 100%
