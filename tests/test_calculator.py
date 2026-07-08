from app.tools.calculator import calculator


def test_addition():
    assert calculator("2+3") == "5"


def test_multiplication():
    assert calculator("5*10") == "50"
