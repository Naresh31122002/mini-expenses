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


if __name__ == "__main__":
    app.run(debug=True)