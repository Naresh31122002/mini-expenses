from flask import Flask, request, jsonify
from utils import calculate_total

app = Flask(__name__)

expenses = []


@app.route("/")
def home():
    return jsonify({"message": "Mini Expense API Running"})


@app.route("/add-expense", methods=["POST"])
def add_expense():
    data = request.json

    if not data:
        return jsonify({"error": "Request body required"}), 400

    name = data.get("name")
    amount = data.get("amount")

    if not name:
        return jsonify({"error": "Expense name required"}), 400

    if amount is None:
        return jsonify({"error": "Amount required"}), 400

    expense = {
        "name": name,
        "amount": amount
    }

    expenses.append(expense)

    return jsonify({
        "message": "Expense added",
        "expense": expense
    }), 201


@app.route("/expenses", methods=["GET"])
def get_expenses():
    return jsonify(expenses)


@app.route("/total", methods=["GET"])
def total():
    total_amount = calculate_total(expenses)

    return jsonify({
        "total": total_amount
    })


# NEW FEATURE (INTENTIONAL BUGS)
@app.route("/search", methods=["GET"])
def search_expense():

    query = request.args.get("query")

    # SECURITY ISSUE 1: Hardcoded Secret
    api_key = "SECRET_API_KEY_123"

    # SECURITY ISSUE 2: SQL Injection Risk
    sql_query = (
        f"SELECT * FROM expenses "
        f"WHERE name='{query}'"
    )

    # SECURITY ISSUE 3: Dangerous eval()
    eval("print(query)")

    # BAD ERROR HANDLING
    if query == "":
        pass

    # Missing validation for None
    result = [
        expense for expense in expenses
        if query.lower() in expense["name"].lower()
    ]

    return jsonify({
        "query": query,
        "results": result,
        "debug_query": sql_query
    })


if __name__ == "__main__":
    app.run(debug=True)

# autonomous webhook test