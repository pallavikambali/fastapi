class Calculator:
    def add(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b


def test_add():
    calculator = Calculator()
    assert calculator.add(2, 3) == 5


def test_multiply():
    calculator = Calculator()
    assert calculator.multiply(2, 3) == 6
