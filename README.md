# Calculator App

A Python calculator application with a well-structured, modular architecture.

## Project Structure

```
calculator-app-assignment4/
├── app/
│   ├── __init__.py
│   ├── calculator/
│   │   └── __init__.py       # Calculator class and management
│   ├── calculation/
│   │   └── __init__.py       # Individual calculation handling
│   └── operation/
│       └── __init__.py       # Arithmetic operations
├── tests/
│   └── __init__.py           # Unit tests
├── .gitignore
├── requirements.txt
└── README.md
```

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

## Running Tests

```bash
pytest
```

## Running Tests with Coverage

```bash
pytest --cov=app
```
