# Import libraries
"""This is a simple CRUD application using Flask and SQLite3."""
from flask import Flask, redirect, request, render_template, url_for

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation: List all transactions
@app.route('/')
def get_transactions():
    """This function returns the list of transactions."""
    return render_template('transactions.html', transactions=transactions)

# Create operation: Display add transaction form
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    """add_transaction function adds a new transaction to the list of transactions."""
    if request.method == 'POST':
        transaction = {
        'id': len(transactions) + 1,
        'date': request.form['date'],
        'amount': float(request.form['amount'])
        }
        transactions.append(transaction)
        return redirect(url_for('get_transactions'))
    return render_template("form.html")

# Update operation
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    """edit_transaction function edits a transaction from the list of transactions."""
    if request.method == 'POST':
        date = request.form['date']
        amount = float(request.form['amount'])

        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = amount
                break
        return redirect(url_for('get_transactions'))

    for transaction in transactions:
        if transaction['id'] == transaction_id:
            return render_template("edit.html", transaction=transaction)

# Delete operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    """delete_transaction function deletes a transaction from the list of transactions."""
    # Create a copy of the list to iterate over
    transactions_copy = list(transactions)

    for transaction in transactions_copy:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            break
    return redirect(url_for('get_transactions'))

# Search operation
@app.route("/search", methods=["GET", "POST"])
def search_transactions():
    """search_transactions function searches for a transaction from the list of transactions."""
    transactions_copy = list(transactions)
    filtered_transactions = []

    if request.method == 'POST':
        min_amount = float(request.form['min_amount'])
        max_amount = float(request.form['max_amount'])

        for transaction in transactions_copy:
            if min_amount <= transaction['amount'] <= max_amount:
                filtered_transactions.append(transaction)
        return render_template("transactions.html", transactions=filtered_transactions)
    return render_template("search.html")

# @app.route("/")
# def total_balance():
#     """total_balance function calculates the total balance of the transactions."""
#     total_balance = 0
#     for transaction in transactions:
#         total_balance += transaction['amount']
#     # return f"Total Balance: {total_balance}"
#     return render_template(
#         "transactions.html", 
#         total_balance=total_balance,
#     )

@app.route("/balance")
def total_balance():
    """total_balance function calculates the total balance of the transactions."""
    # Calculate the total balance by summing the amount values of all transactions
    total_balance = sum(transaction['amount'] for transaction in transactions)

    # Return the total balance as a string
    return render_template(
        "transactions.html", 
        transactions=transactions, 
        total_balance=total_balance
    )

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
