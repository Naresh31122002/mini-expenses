from utils import calculate_total


def test_calculate_total():
    expenses = [
        {"amount": 100},
        {"amount": 200}
    ]

    assert calculate_total(expenses) == 300


def test_empty_expenses():
    assert calculate_total([]) == 0