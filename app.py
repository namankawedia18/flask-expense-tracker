from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import date, timedelta

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

    quick = request.args.get("quick", "")

    from_date = request.args.get("from_date", "")
    to_date = request.args.get("to_date", "")

    query = Expense.query

    today = date.today()

    if quick == "today":

        query = query.filter(
            Expense.date == str(today)
        )

    elif quick == "week":

        week_start = today - timedelta(days=today.weekday())

        query = query.filter(
            Expense.date >= str(week_start)
        )

    elif quick == "month":

        month_start = today.replace(day=1)

        query = query.filter(
            Expense.date >= str(month_start)
        )

    elif quick == "year":

        year_start = date(today.year, 1, 1)

        query = query.filter(
            Expense.date >= str(year_start)
        )

    if from_date:
        query = query.filter(Expense.date >= from_date)

    if to_date:
        query = query.filter(Expense.date <= to_date)

    # -------------------------
    # Search
    # -------------------------

    if search:
        query = query.filter(
            Expense.event.ilike(f"%{search}%")
        )

    # -------------------------
    # Sorting
    # -------------------------

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

    # -------------------------
    # Dashboard Statistics
    # -------------------------

    total = sum(expense.amount for expense in expenses)

    total_transactions = len(expenses)

    category_summary = {}

    for expense in expenses:

        if expense.event in category_summary:
            category_summary[expense.event] += expense.amount
        else:
            category_summary[expense.event] = expense.amount

    chart_labels = list(category_summary.keys())
    chart_values = list(category_summary.values())

    # -------------------------
    # Monthly Summary
    # -------------------------

    monthly_summary = {}

    for expense in expenses:

        month = expense.date[:7]      # Example: 2026-06

        if month in monthly_summary:

            monthly_summary[month] += expense.amount

        else:

            monthly_summary[month] = expense.amount


    month_labels = list(monthly_summary.keys())

    month_values = list(monthly_summary.values())

    highest_expense = max(
        (expense.amount for expense in expenses),
        default=0
    )

    average_expense = (
        total / total_transactions
        if total_transactions > 0
        else 0
    )

    total_categories = len(category_summary)

    if category_summary:
        biggest_category = max(
            category_summary,
            key=category_summary.get
        )
    else:
        biggest_category = "N/A"

    return render_template(
        "expenses.html",
        expenses=expenses,
        total=total,
        total_transactions=total_transactions,
        category_summary=category_summary,
        search=search,
        sort=sort,
        chart_labels=chart_labels,
        chart_values=chart_values,
        month_labels=month_labels,
        month_values=month_values,
        highest_expense=highest_expense,
        average_expense=average_expense,
        total_categories=total_categories,
        biggest_category=biggest_category,
        from_date=from_date,
        to_date=to_date
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