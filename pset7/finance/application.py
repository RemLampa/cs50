from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    """User Dashboard"""
    
    # get user_id
    user_id = session.get("user_id")
    
    # get user's remaining funds
    rows = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)
    wallet = rows[0]["cash"]
    
    stocks = get_stocks(db, user_id)
    
    total_value = 0
    
    if stocks:
        for stock in stocks:
            total_value = total_value + stock["value"]
    
    portfolio_value = wallet + total_value
    
    return render_template("index.html", wallet=wallet, stocks=stocks, total_value=total_value, portfolio_value=portfolio_value)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    
    # get user id
    user_id = session.get("user_id")
    
    # get user's remaining funds
    rows = db.execute("SELECT cash FROM users WHERE id = :id", id=session.get("user_id"))
    wallet = rows[0]["cash"]
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        symbol = request.form.get("symbol")
        
        # ensure stock symbol was submitted
        if not symbol:
            flash("Please enter a stock symbol.", "danger")
            return render_template("buy.html", wallet=wallet)
        
        stock_quote = lookup(symbol.upper())
        
        # ensure stock symbol is valid
        if stock_quote is None:
            flash("Please enter a valid stock symbol.", "danger")
            return render_template("buy.html", wallet=wallet)
            
        # ensure number of shares is a positive integer
        try:
            shares = int(request.form.get("shares"))
            
            if shares <= 0:
                raise Exception()
        except:
            flash("Please enter valid number of shares.", "danger")
            return render_template("buy.html", wallet=wallet)
        
        # get total purchase cost
        total_cost = shares * stock_quote["price"]
        
        # ensure funds are sufficient
        if total_cost > wallet:
            flash("You have insufficient funds.", "danger")
            return render_template("buy.html", wallet=wallet)
        
        # find stock under user's account
        rows = db.execute("SELECT * FROM stocks WHERE symbol = :symbol AND owner_id = :owner_id",
            symbol=stock_quote["symbol"],
            owner_id=user_id)
        
        # if user already has shares of purchased stock, update
        if len(rows) == 1:
            total_shares = rows[0]["shares"] + shares
            db.execute("UPDATE stocks SET shares = :total_shares WHERE id = :id",
                total_shares=total_shares,
                id=rows[0]["id"])
        # else, add stock in user's account
        else:
            db.execute("INSERT INTO stocks(symbol, owner_id, shares) VALUES(:symbol, :owner_id, :shares)",
                symbol=stock_quote["symbol"],
                owner_id=user_id,
                shares=shares)
        
        # subtract purchase cost from wallet
        wallet = wallet - total_cost
        
        # update user wallet in database
        rows = db.execute("UPDATE users SET cash = :wallet WHERE id = :id", wallet=wallet, id=user_id)
        
        # insert into transaction history
        rows = db.execute("""
            INSERT INTO logs(user_id, stock, shares, price, value, transaction_type)
            VALUES(:user_id, :stock, :shares, :price, :value, :transaction)
            """,
            user_id=user_id,
            stock=stock_quote["symbol"],
            shares=shares,
            price=stock_quote["price"],
            value=total_cost,
            transaction="buy")
        
        return render_template("buy.html", quote=stock_quote, shares=shares, cost=total_cost, wallet=wallet)
    
    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html", wallet=wallet)

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    
    user_id = session.get("user_id")
    
    logs = db.execute("SELECT * FROM logs WHERE user_id = :user_id ORDER BY timestamp DESC", user_id=user_id)
    
    return render_template("history.html", logs=logs)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            flash("Please provide a username.", "danger")
            return render_template("login.html")

        # ensure password was submitted
        if not request.form.get("password"):
            flash("Please provide a password.", "danger")
            return render_template("login.html")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            flash("Invalid username/password.", "danger")
            return render_template("login.html")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user        
        try:
            dest_url = url_for(request.args.get("next"))
        except:
            dest_url = url_for("index")

        return redirect(dest_url)

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        symbol = request.form.get("symbol")
        
        if not symbol:
            flash("Please enter a stock symbol.", "danger")
            return render_template("quote.html")
        
        stock_quote = lookup(symbol.upper())
        
        if stock_quote is None:
            flash("Invalid stock symbol.", "danger")
            return render_template("quote.html")

        return render_template("quote.html", quote=stock_quote)
    
    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # if user is already logged in
    if session.get("user_id"):
        return redirect(url_for("index"))
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")
        
        # ensure username was submitted
        if not username:
            flash("Please provide username.", "danger")
            return render_template("register.html")

        # ensure password was submitted
        if not password:
            flash("Please provide a password.", "danger")
            return render_template("register.html")
            
        # ensure password confirmation was submitted
        if not confirm_password:
            flash("Please confirm your password.", "danger")
            return render_template("register.html")
            
        # ensure passwords must match
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("register.html")
            
        # check if user exists
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        
        if len(rows) > 0:
            flash("Username already exists.", "danger")
            return render_template("register.html")
            
        # encrypt password
        hashed_password = pwd_context.hash(password)
        
        # create new user
        try:
            db.execute("INSERT INTO users(username, hash) VALUES(:username, :password)",
                username=username,
                password=hashed_password)
        
            return render_template("register.html", registered=True)
        except:
            return apology("registration error")
        
    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")    

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    
    # get user_id and total available cash
    user_id = session.get("user_id")
    wallet = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)[0]["cash"]
    
    if request.method == "GET":
        stocks = get_stocks(db, user_id)
        
        return render_template("sell.html", stocks=stocks, wallet=wallet)

    if request.method == "POST":
        sell_form = request.form
        
        # flag to track if a sale has occured
        sale_occured = False
        
        for item in sell_form.items():
            stocks = get_stocks(db, user_id)
            
            stock_id = item[0]
            stock_query = db.execute("SELECT id, symbol, shares FROM stocks WHERE id = :stock_id", stock_id=stock_id)[0]
            stock = get_stock_info(stock_query)
            
            # ensure number of shares is not negative
            try:
                shares_to_sell = int(item[1])
                
                if shares_to_sell < 0:
                    raise Exception()
            except:
                flash("Please enter valid number of shares for " + stock["symbol"] + ".", "danger")
                continue
                
            # no sale here
            if shares_to_sell == 0:
                continue

            # ensure user has enough number of shares
            if stock["shares"] < shares_to_sell:
                flash("You have entered a number greater than your actual shares for " + stock["symbol"] + ".", "danger")
                continue
            
            # update number of shares of the stock
            stock["shares"] = stock["shares"] - shares_to_sell
            query = db.execute("UPDATE stocks SET shares = :shares WHERE id = :stock_id", shares=stock["shares"], stock_id=stock_id)
                
            # update user wallet in database
            sale_value = shares_to_sell * stock["price"]
            wallet = wallet + sale_value
            query = db.execute("UPDATE users SET cash = :wallet WHERE id = :id", wallet=wallet, id=user_id)
            
            # insert into transaction history
            rows = db.execute("""
                INSERT INTO logs(user_id, stock, shares, price, value, transaction_type)
                VALUES(:user_id, :stock, :shares, :price, :value, :transaction)
                """,
                user_id=user_id,
                stock=stock["symbol"],
                shares=shares_to_sell,
                price=stock["price"],
                value=sale_value,
                transaction="sell")

            
            # sale successful, update flag
            sale_occured = True

            share_text = "share" if shares_to_sell ==1 else "shares"

            flash("Successfully sold "
                + str(shares_to_sell)
                + " " + share_text + " of "
                + stock["symbol"]
                + " for "
                + str(usd(sale_value))
                + ".",
                "success")
        
        if sale_occured:
            # get updated stock list
            stocks = get_stocks(db, user_id)
        else:
            flash("Please enter the number of shares of the stock/s you want to sell.", "danger")
            
        return render_template("sell.html", stocks=stocks, wallet=wallet)
        
@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """Change password"""

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        old_password = request.form.get("old-password")
        new_password = request.form.get("new-password")
        confirm_password = request.form.get("confirm-password")
        
        # ensure old_password was submitted
        if not old_password:
            flash("Please enter your old password.", "danger")
            return render_template("password.html")
            
        user_id = session.get("user_id")
        rows = db.execute("SELECT hash FROM users WHERE id = :user_id", user_id=user_id)
        # ensure old password is the same as in database
        if not pwd_context.verify(old_password, rows[0]["hash"]):
            flash("The old password you entered is invalid.", "danger")
            return render_template("password.html")

        # ensure new password was submitted
        if not new_password:
            flash("Please provide a new password.", "danger")
            return render_template("password.html")
            
        # ensure password confirmation was submitted
        if not confirm_password:
            flash("Please confirm your password.", "danger")
            return render_template("password.html")
            
        # ensure passwords must match
        if new_password != confirm_password:
            flash("New passwords do not match.", "danger")
            return render_template("password.html")

        # encrypt new password
        hashed_password = pwd_context.hash(new_password)
        
        # update the password in database
        try:
            db.execute("UPDATE users SET hash = :hashed_password WHERE id = :user_id",
                hashed_password=hashed_password,
                user_id=user_id)
        
            return render_template("password.html", success=True)
        except:
            return apology("change password error")
        
    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("password.html")