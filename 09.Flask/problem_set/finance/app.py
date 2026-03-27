import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
# 1. Get the user's current cash
    user_rows = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash = user_rows[0]["cash"]

    # 2. Get consolidated shares owned by the user
    # We only want stocks where the total sum of shares is greater than 0
    portfolio = db.execute("""
        SELECT symbol, SUM(shares) as total_shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING total_shares > 0
    """, session["user_id"])

    # 3. Enrich the portfolio data with current prices from lookup
    total_holdings_value = 0
    for stock in portfolio:
        quote = lookup(stock["symbol"])
        stock["name"] = quote["name"]
        stock["price"] = quote["price"]
        stock["total"] = stock["price"] * stock["total_shares"]
        total_holdings_value += stock["total"]

    # 4. Calculate grand total (cash + all stock values)
    grand_total = cash + total_holdings_value

    return render_template("index.html",
                           portfolio=portfolio,
                           cash=cash,
                           grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        stock_symbol = request.form.get("symbol")
        shares_raw = request.form.get("shares")
        stock_info = lookup(stock_symbol)
        if not stock_info:
            return apology("Your stock symbol is incorrect!")

        if not shares_raw or not shares_raw.isdigit():
            return apology("You must enter a positive whole number")

        num_shares = int(shares_raw)
        if not isinstance(num_shares, int):
            return apology("Input valid number of shares!")

        # print(isinstance(num_shares, int))
        price = stock_info["price"]
        cash_avai = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]['cash']
        # print(cash_avai)
        total_cost = price * num_shares
        if cash_avai < total_cost:
            return apology("You don't have enough money")
        else:
            db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                       session["user_id"], stock_symbol, num_shares, price)
            db.execute("UPDATE users SET cash = cash - ? WHERE id = ?",
                       total_cost, session["user_id"])

            return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Query database for all of the user's transactions
    transactions = db.execute("""
        SELECT symbol, shares, price, timestamp
        FROM transactions
        WHERE user_id = ?
        ORDER BY timestamp DESC
    """, session["user_id"])

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        stock_sym = request.form.get("symbol")
        stock_info = lookup(stock_sym)
        if not stock_info:
            return apology("Your stock symbol is incorrect!")
        else:
            name, price, symbol = stock_info["name"], stock_info["price"], stock_info["symbol"]

            return render_template("quoted.html", name=name, price=price, symbol=symbol)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return apology("Please fill the username")
        else:

            try:
                password = request.form.get("password")
                password_retype = request.form.get("confirmation")

                if not password or password != password_retype:
                    return apology("Password is not valid")
                else:
                    db.execute("INSERT INTO users (username, hash) VALUES (?, ?);",
                               username, generate_password_hash(password))
                    return redirect("/")
            except ValueError:
                return apology("Duplicated username")
    else:
        return render_template("register.html")
    # return apology("TODO")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        num_shares = request.form.get("shares")
        stock_info = lookup(symbol)

        price = stock_info["price"]

        avai_stock = db.execute("""
            SELECT symbol, SUM(shares) AS total_shares
            FROM transactions
            WHERE user_id = ?
            AND symbol = ?
            GROUP BY symbol
            """, session["user_id"], symbol)
        print(avai_stock)
        num_shares = int(num_shares)
        if not avai_stock or avai_stock[0]["total_shares"] < num_shares:
            return apology("Not enough shares")
        else:
            total_value = num_shares * price
            db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                       session["user_id"], symbol, - num_shares, price)
            db.execute("UPDATE users SET cash = cash + ? WHERE id = ?",
                       total_value, session["user_id"])
            return redirect("/")

    else:
        list_stock = db.execute("""
            SELECT symbol
            FROM transactions
            WHERE user_id = ?
            GROUP BY symbol
            HAVING SUM(shares) > 0
            """, session["user_id"])
        return render_template("sell.html", list_stock=list_stock)
