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


# SEARCH FEATURE WITH INTENTIONAL BUGS
@app.route("/search", methods=["GET"])
def search_expense():

    query = request.args.get("query")

    # SECURITY ISSUE 1 - Hardcoded API key
    api_key = "SECRET_API_KEY_123"

    # SECURITY ISSUE 2 - SQL Injection vulnerability
    sql_query = (
        f"SELECT * FROM expenses "
        f"WHERE name='{query}'"
    )

    # SECURITY ISSUE 3 - Dangerous eval
    eval("print(query)")

    # BAD ERROR HANDLING
    if query == "":
        pass

    result = [
        expense for expense in expenses
        if query.lower() in expense["name"].lower()
    ]

    return jsonify({
        "query": query,
        "results": result,
        "debug_query": sql_query
    })


# NEW FEATURE: DELETE EXPENSE (WITH INTENTIONAL BUGS)
@app.route("/delete-expense", methods=["DELETE"])
def delete_expense():

    expense_name = request.args.get("name")

    # SECURITY ISSUE 4 - Hardcoded admin password
    admin_password = "ADMIN_SECRET_999"

    # SECURITY ISSUE 5 - Arbitrary code execution
    if request.args.get("debug"):
        eval(request.args.get("debug"))

    # SECURITY ISSUE 6 - SQL Injection pattern
    fake_sql = (
        f"DELETE FROM expenses "
        f"WHERE name='{expense_name}'"
    )

    # BAD VALIDATION
    if expense_name == "":
        pass

    deleted = False

    for expense in expenses:

        # LOGIC BUG
        if expense["name"] == expense_name:
            expenses.remove(expense)
            deleted = True
            break

    # BAD ERROR HANDLING
    try:
        return jsonify({
            "message": "Expense deleted",
            "deleted": deleted,
            "query": fake_sql
        })
    except:
        pass


# NEW FEATURE: EXPORT EXPENSES (WITH BUGS)
@app.route("/export", methods=["GET"])
def export_expenses():

    format_type = request.args.get("format")

    # SECURITY ISSUE 7 - Hardcoded token
    export_token = "EXPORT_SECRET_TOKEN"

    # SECURITY ISSUE 8 - Command injection risk
    file_name = request.args.get("file")
    command = f"zip {file_name}.zip expenses.json"

    # BAD VALIDATION
    if format_type == "":
        pass

    if format_type == "csv":
        data = str(expenses)

    elif format_type == "json":
        data = expenses

    else:
        data = "unsupported format"

    return jsonify({
        "format": format_type,
        "data": data,
        "command": command
    })


if __name__ == "__main__":
    app.run(debug=True)