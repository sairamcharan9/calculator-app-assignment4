"""Entry point for the Calculator application."""

from app.calculator import Calculator


def main() -> None:
    """Create a Calculator instance and start the REPL."""
    calculator = Calculator()
    calculator.run()


if __name__ == "__main__":
    main()  # pragma: no cover
