import pytest

def add(a, b):
    return a + b


@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (4, 5, 9),
    (1, 1, 2),
    (10, 20, 30),
    (5, 5, 10)
])
def test_add(a, b, expected):
    assert add(a, b) == expected
