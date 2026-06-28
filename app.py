from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)

app.secret_key = "expense_tracker_secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(20), nullable=False)

expense_list = list()

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        event = request.form["event_name"]
        price = float(request.form["price"])
        date = request.form["date"]

        new_expense = Expense(
            event=event,
            amount=price,
            date=date
        )

        db.session.add(new_expense)
        db.session.commit()

        flash("Expense added successfully!", "success")

        return redirect(url_for("viewExpense"))

    return render_template("add.html")

    

@app.route("/expense")
def viewExpense():

    search = request.args.get("search", "")
    sort = request.args.get("sort", "")

    query = Expense.query

    # Search
    if search:
        query = query.filter(
            Expense.event.ilike(f"%{search}%")
        )

    # Sorting
    if sort == "date_desc":
        query = query.order_by(desc(Expense.date))

    elif sort == "date_asc":
        query = query.order_by(Expense.date)

    elif sort == "amount_desc":
        query = query.order_by(desc(Expense.amount))

    elif sort == "amount_asc":
        query = query.order_by(Expense.amount)

    elif sort == "event_asc":
        query = query.order_by(Expense.event)

    elif sort == "event_desc":
        query = query.order_by(desc(Expense.event))

    expenses = query.all()

    total = sum(expense.amount for expense in expenses)

    category_summary = {}

    for expense in expenses:

        if expense.event in category_summary:
            category_summary[expense.event] += expense.amount
        else:
            category_summary[expense.event] = expense.amount

    return render_template(
        "expenses.html",
        expenses=expenses,
        total=total,
        total_transactions=len(expenses),
        category_summary=category_summary,
        search=search,
        sort=sort
    )

@app.route("/delete/<int:id>")
def deleteExpense(id):

    expense = Expense.query.get_or_404(id)

    db.session.delete(expense)
    db.session.commit()

    flash("Expense deleted successfully!", "danger")

    return redirect(url_for("viewExpense"))

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def editExpense(id):

    expense = Expense.query.get_or_404(id)

    if request.method == "POST":

        expense.event = request.form["event_name"]
        expense.amount = float(request.form["price"])
        expense.date = request.form["date"]

        db.session.commit()

        flash("Expense updated successfully!", "warning")

        return redirect(url_for("viewExpense"))

    return render_template(
        "edit.html",
        expense=expense
    )

with app.app_context():
    db.create_all()

app.run(debug=True)