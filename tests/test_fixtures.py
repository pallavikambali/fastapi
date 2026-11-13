import pytest


class Calculator:
    def add(self, a, b):
        return a + b


@pytest.fixture
def calculator():
    return Calculator()


@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (4, 5, 9),
    (10, 20, 30),
    (1, 1, 2)
])
def test_add(calculator, a, b, expected):
    assert calculator.add(a, b) == expected
