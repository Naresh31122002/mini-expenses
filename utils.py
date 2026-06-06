def calculate_total(expenses):
    """
    Calculate total amount of expenses.
    """

    if not expenses:
        return 0

    return sum(expense["amount"] for expense in expenses)